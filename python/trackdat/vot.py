'''

Expects directory structure:
    list.txt
    {video}/{frame:08d}.jpg
    {video}/groundtruth.txt
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from . import dataset
from . import util

from .vot_toolkit import vot as _vot


def load_vot(dir):
    # Cannot use load_csv_dataset_simple because
    # we use the VOT code to load the regions.
    video_ids = _load_tracks(dir)
    labels = {}
    for video_id in video_ids:
        with open(os.path.join(dir, _annot_file(video_id)), 'r') as f:
            labels[video_id] = _load_groundtruth(f)
    return dataset.Dataset(
        track_ids=video_ids,
        labels=labels,
        image_files=util.func_dict(video_ids, _image_file))


def _load_tracks(dir):
    with open(os.path.join(dir, 'list.txt'), 'r') as f:
        lines = f.readlines()
    # Strip whitespace and remove empty lines.
    return list(filter(bool, map(str.strip, lines)))


def _annot_file(video_id):
    return os.path.join(video_id, 'groundtruth.txt')


def _image_file(video_id):
    return os.path.join(video_id, '{:08d}.jpg')


def _load_groundtruth(f, init_time=1):
    # with open(os.path.join(dir, video_id, 'groundtruth.txt'), 'r') as f:
    lines = f.readlines()
    # Strip whitespace and remove empty lines.
    lines = filter(bool, map(str.strip, lines))
    frames = {}
    t = init_time
    for line in lines:
        r = _vot.convert_region(_vot.parse_region(line), 'rectangle')
        # TODO: Confirm that we should subtract 1 here.
        # Perhaps we should rather subtract and add 0.5 from min and max.
        frames[t] = dataset.make_rect(
            xmin=r.x - 1,
            ymin=r.y - 1,
            xmax=r.x - 1 + r.width,
            ymax=r.y - 1 + r.height)
        t += 1
    return frames
