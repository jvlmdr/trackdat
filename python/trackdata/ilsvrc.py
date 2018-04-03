from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import csv
import fnmatch
import itertools
import os
import xmltodict

from xml.etree import ElementTree as etree

from . import util
from . import dataset


def load_ilsvrc(dir, subset, use_xmltodict=False):
    '''
    Args:
        convert_args: See `convert_track_annotation`
    '''
    if subset == 'train':
        snippets = _load_snippets_train(dir)
    elif subset == 'val':
        snippets = _load_snippets_val(dir)
    else:
        raise ValueError('unknown set: {}'.format(subset))

    track_ids = []
    labels = {}
    video_id_map = {}
    for snippet_id in snippets:
        snippet_labels = _load_snippet_labels(dir, subset, snippet_id,
                                              use_xmltodict=use_xmltodict)
        labels.update(snippet_labels)
        snippet_track_ids = list(sorted(snippet_labels.keys()))
        track_ids.extend(snippet_track_ids)
        video_id_map.update({track_id: snippet_id for track_id in snippet_track_ids})

    return dataset.Dataset(
        track_ids=track_ids,
        labels=labels,
        video_id_map=video_id_map,
        image_files=util.func_dict(snippets, lambda v: _image_file(subset, v)))


def _image_file(subset, snippet_id):
    parts = ['Data', 'VID', subset] + snippet_id.split('/') + ['{:06d}.JPEG']
    return os.path.join(*parts)


def _load_snippets_train(dir, subset='train', num_classes=30):
    # Load training snippets for each class.
    # For the train set, there is a file per class that lists positive and negative snippets.
    class_snippets = [_load_positive_snippets(dir, subset, num)
                      for num in range(1, num_classes + 1)]
    # Take union of all sets.
    snippets = set(itertools.chain.from_iterable(class_snippets))
    return snippets


def _load_positive_snippets(dir, subset, class_num):
    set_file = '{}_{:d}.txt'.format(subset, class_num)
    path = os.path.join(dir, 'ImageSets', 'VID', set_file)
    with open(path, 'r') as f:
        reader = csv.DictReader(f, delimiter=' ', fieldnames=['snippet_id', 'label'])
        rows = list(reader)
    snippets = [r['snippet_id'] for r in rows if r['label'] == '1']
    return snippets


def _load_snippets_val(dir, subset='val'):
    # For the val set, there is a file val.txt that lists all frames of all videos.
    path = os.path.join(dir, 'ImageSets', 'VID', subset + '.txt')
    with open(path, 'r') as f:
        reader = csv.DictReader(f, delimiter=' ', fieldnames=['frame_name', 'frame_index'])
        rows = list(reader)
    # Take unique snippet names.
    snippets = set(_snippet_from_frame_name(r['frame_name']) for r in rows)
    return snippets


def _make_track_id(snippet_id, object_id):
    return '_'.join([snippet_id, 'object', object_id])


def _load_snippet_labels(dir, subset, snippet_id, use_xmltodict=False):
    n = _snippet_length(dir, subset, snippet_id)
    dir_name = os.path.join(dir, 'Annotations', 'VID', subset, snippet_id)

    labels = {}
    for t in range(n):
        annot_file = os.path.join(dir_name, '{:06d}.xml'.format(t))
        if use_xmltodict:
            with open(annot_file, 'r') as f:
                tree = xmltodict.parse(f.read(), force_list={'object'}, dict_constructor=dict)
            annot = tree['annotation']
            imwidth = int(annot['size']['width'])
            imheight = int(annot['size']['height'])
            for obj in annot.get('object', []):
                object_id = obj['trackid']
                track_id = _make_track_id(snippet_id, object_id)
                labels.setdefault(track_id, {})[t] = _rect_from_obj_dict(obj)
        else:
            tree = etree.parse(annot_file)
            annot = tree.getroot()
            if annot.tag != 'annotation':
                raise RuntimeError('root tag is not annotation: {}'.format(annot.tag))
            size = annot.find('size')
            if size is None:
                raise RuntimeError('no size tag')
            imwidth = int(size.find('width').text.strip())
            imheight = int(size.find('height').text.strip())
            for obj in annot.findall('object'):
                object_id = obj.find('trackid').text
                track_id = _make_track_id(snippet_id, object_id)
                labels.setdefault(track_id, {})[t] = _rect_from_obj_node(obj)

    # Fill in missing times with 'absent' annotations.
    for t in range(n):
        # absent = [track_id for track_id in labels.keys() if t not in labels[track_id]]
        for track_id in labels.keys():
            if t not in labels[track_id]:
                labels[track_id][t] = dict(present=False)

    return labels


def _snippet_length(dir, subset, snippet_id):
    dir_name = os.path.join(dir, 'Data', 'VID', subset, snippet_id)
    image_files = fnmatch.filter(os.listdir(dir_name), '*.JPEG')
    return len(image_files)


def _snippet_from_frame_name(s):
    # Takes frame name from val.txt and gets snippet name.
    parts = s.split('/')
    return '/'.join(parts[:-1])


def _rect_from_obj_node(obj):
    extra = {}
    for field in ['occluded', 'generated']:
        field_node = obj.find(field)
        if field_node is None:
            extra[field] = field_node.text

    bndbox = obj.find('bndbox')
    xmin = float(bndbox.find('xmin').text)
    xmax = float(bndbox.find('xmax').text)
    ymin = float(bndbox.find('ymin').text)
    ymax = float(bndbox.find('ymax').text)
    return dict(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, **extra)


def _rect_from_obj_dict(obj):
    extra = {}
    for field in ['occluded', 'generated']:
        if field in obj:
            extra[field] = obj[field]

    bndbox = obj['bndbox']
    xmin = float(bndbox['xmin'])
    xmax = float(bndbox['xmax'])
    ymin = float(bndbox['ymin'])
    ymax = float(bndbox['ymax'])
    return dict(xmin_pix=xmin, xmax_pix=xmax, ymin_pix=ymin, ymax_pix=ymax, **extra)
