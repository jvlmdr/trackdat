'''

Expects directory structure:
    {video}/img/{frame}.jpg
    {video}/groundtruth_rect.txt
    {video}/groundtruth_rect.{object_num}.txt
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import fnmatch
import os

from . import dataset
from . import util


def load_otb(dir, subset=None):
    # subset can be 'tb_100', 'tb_50', 'cvpr13'
    track_ids = _load_tracks_otb_subset(subset) if subset else None
    return _load_otb_format(dir, track_ids=track_ids, init_times=INIT_TIMES_OTB)


def load_dtb70(dir):
    return _load_otb_format(dir)


def load_tlp(dir):
    '''
    The TLP format is close to the OTB format but with extra ground-truth fields.
    '''
    # https://amoudgl.github.io/tlp/datasets/
    fieldnames = ['time', 'xmin', 'ymin', 'width', 'height', 'absent']
    return _load_otb_format(dir, fieldnames=fieldnames)


def _load_tracks_otb_subset(name):
    source_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(source_dir, 'otb_toolkit', name + '.txt'), 'r') as f:
        lines = f.readlines()
    # Split by whitespace and take first element.
    track_ids = []
    for line in lines:
        parts = line.split()
        if not parts:
            continue
        track_ids.append(parts[0])
    return track_ids


def _load_otb_format(dir, track_ids=None, init_times=None, default_init_time=1, fieldnames=None):
    '''
    Args:
        track_ids: List of strings or None.
            If None, then tracks are discovered from directory structure.

    For OTB, it is necessary to specify init_times for 'David' sequence.
    '''
    # Cannot use load_csv_dataset_simple because
    # there are multiple tracks per file.

    init_times = init_times or {}
    if fieldnames is None:
        fieldnames = ['xmin', 'ymin', 'width', 'height']

    if track_ids is None:
        track_ids = list(_discover_tracks(dir))
        if len(track_ids) == 0:
            raise RuntimeError('no tracks found in dir: {}'.format(dir))

    labels = {}
    for track_id in track_ids:
        video_id, object_id = _split_track_id(track_id)
        gt_file = _filename_from_object_id(object_id)
        with open(os.path.join(dir, video_id, gt_file), 'r') as f:
            labels[track_id] = dataset.load_rects_csv(
                f, fieldnames=fieldnames,
                init_time=init_times.get(track_id, default_init_time),
                delim='\s+|,')

    video_id_map = util.func_dict(track_ids, _video_id_from_track_id)
    video_ids = set(video_id_map.values())
    return dataset.Dataset(
        track_ids=track_ids,
        labels=labels,
        video_id_map=video_id_map,
        image_files=util.func_dict(video_ids, lambda v: _infer_image_format(dir, v)))


def _infer_image_format(dir, video_id):
    image_dir = _image_dir(video_id)
    fname = util.infer_image_file_pattern(os.path.join(dir, image_dir))
    return os.path.join(image_dir, fname)


def _image_dir(video_id):
    return os.path.join(video_id, 'img')


def _filename_from_object_id(object_id):
    if not object_id:
        return 'groundtruth_rect.txt'
    return 'groundtruth_rect.{}.txt'.format(object_id)


def _video_id_from_track_id(track_id):
    parts = str.split(track_id, '.')
    return parts[0]


def _discover_tracks(dir):
    subdirs = util.list_subdirs(dir)
    for video_id in subdirs:
        rect_files = fnmatch.filter(os.listdir(os.path.join(dir, video_id)), 'groundtruth_rect*')
        for rect_file in rect_files:
            if os.stat(os.path.join(dir, video_id, rect_file)).st_size == 0:
                continue  # Skip empty files.
            object_id = _object_id_from_filename(rect_file)
            yield _make_track_id(video_id, object_id)


def _make_track_id(video_id, object_id):
    if not object_id:
        return video_id
    else:
        return video_id + '.' + object_id


def _split_track_id(track_id):
    parts = track_id.split('.')
    if len(parts) == 1:
        return track_id, ''
    elif len(parts) == 2:
        return parts
    else:
        raise RuntimeError('wrong number of dots: {}'.format(track_id))


def _object_id_from_filename(fname):
    basename, _ = os.path.splitext(fname)
    if basename == 'groundtruth_rect':
        return ''
    return _remove_prefix(basename, 'groundtruth_rect.')


def _remove_prefix(s, pre):
    if not s.startswith(pre):
        raise ValueError('string does not start with prefix: ' + s)
    return s[len(pre):]


INIT_TIMES_OTB = {
    'David': 300,
    'BlurCar1': 247,
    'BlurCar3': 3,
    'BlurCar4': 18,
}
