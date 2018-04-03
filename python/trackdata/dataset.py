from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re

from . import util


# def make_track_label():
#     pass


# def make_frame_label():
#     pass


def make_rect(xmin, ymin, xmax, ymax):
    return dict(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)


# def make_rect_pix(xmin, ymin, xmax, ymax, imwidth, imheight):
#     return make_rect(
#         xmin=float(xmin) / imwidth,
#         xmax=float(xmax) / imwidth,
#         ymin=float(ymin) / imheight,
#         ymax=float(ymax) / imheight)


class Dataset(object):

    def __init__(self, track_ids, labels, image_files, video_id_map=None):
        self._track_ids = track_ids
        self._labels = labels
        self._video_id_map = video_id_map or {}
        self._image_files = image_files

    def tracks(self):
        return self._track_ids

    def video(self, track_id):
        # Default to track ID itself.
        return self._video_id_map.get(track_id, track_id)

    def labels(self, track_id):
        return self._labels[track_id]

    def image_file(self, video_id, time):
        return self._image_files[video_id].format(time)


def load_csv_dataset_simple(dir, load_videos_fn, annot_file_fn, image_file_fn,
                            fieldnames=None, init_time=None, delim=','):
    '''Load simple dataset (where each video has one track).'''
    video_ids = load_videos_fn(dir)
    if len(video_ids) == 0:
        raise RuntimeError('no tracks found')

    labels = {}
    for video_id in video_ids:
        annot_file = os.path.join(dir, annot_file_fn(video_id))
        with open(annot_file, 'r') as f:
            labels[video_id] = load_rects_csv(
                f, fieldnames=fieldnames, init_time=init_time, delim=delim)

    return Dataset(
        track_ids=video_ids,
        labels=labels,
        image_files=util.func_dict(video_ids, image_file_fn))


def load_rects_csv(f, fieldnames, init_time=None, delim=','):
    re_delim = re.compile(delim)
    time_is_field = 'time' in fieldnames
    if 'xmin' in fieldnames:
        if 'xmax' in fieldnames:
            rect_fn = _rect_min_max
        else:
            rect_fn = _rect_min_size
    elif 'x0' in fieldnames:
        rect_fn = _rect_corners
    else:
        raise RuntimeError('unknown fields: {}'.format(', '.join(fieldnames)))

    if not time_is_field and init_time is None:
        raise RuntimeError('must specify init time if time is not a field')
    t = init_time
    rects = {}
    for line in f:
        fields = re_delim.split(line.strip())
        row = dict(zip(fieldnames, fields))
        if time_is_field:
            t = int(row['time'])
        rects[t] = rect_fn(row)
        t += 1
    return rects


def _rect_min_size(row):
    xmin = float(row['xmin'])
    ymin = float(row['ymin'])
    xmax = xmin + float(row['width'])
    ymax = ymin + float(row['height'])
    return make_rect(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)


def _rect_min_max(row):
    xmin = float(row['xmin'])
    ymin = float(row['ymin'])
    xmax = float(row['xmax'])
    ymax = float(row['ymax'])
    return make_rect(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)


def _rect_corners(row):
    xs = [float(row[key]) for key in ['x0', 'x1', 'x2', 'x3']]
    ys = [float(row[key]) for key in ['y0', 'y1', 'y2', 'y3']]
    if len(set(xs)) != 2:
        raise RuntimeError('not 2 unique x values: {}'.format(str(xs)))
    if len(set(ys)) != 2:
        raise RuntimeError('not 2 unique y values: {}'.format(str(ys)))
    return make_rect(xmin=min(xs), ymin=min(ys), xmax=max(xs), ymax=max(ys))


def assert_image_files_exist(dir, dataset):
    for track_id in dataset.tracks():
        video_id = dataset.video(track_id)
        times = dataset.labels(track_id).keys()
        # Check first and last times.
        util.assert_file_exists(os.path.join(dir, dataset.image_file(video_id, min(times))))
        util.assert_file_exists(os.path.join(dir, dataset.image_file(video_id, max(times))))
