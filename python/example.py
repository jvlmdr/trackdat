from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import time

import trackdata
import trackdata.dataset

alov_dir = 'alov'
dtb70_dir = os.path.join('dtb70', 'DTB70')
ilsvrc_dir = os.path.join('ilsvrc', 'ILSVRC2015')
nfs_dir = 'nfs'
nuspro_dir = 'nuspro'
otb_dir = 'otb'
tc128_dir = os.path.join('tc128', 'Temple-color-128')
tlp_dir = 'tlp'
uav123_dir = os.path.join('uav123', 'UAV123')
vot2013_dir = 'vot2013'
vot2014_dir = 'vot2014'
vot2015_dir = 'vot2015'
vot2016_dir = 'vot2016'
vot2017_dir = 'vot2017'

datasets = [
    dict(func=trackdata.load_otb, dir=otb_dir, kwargs=dict()),
    dict(func=trackdata.load_otb, dir=otb_dir, kwargs=dict(subset='cvpr13')),
    dict(func=trackdata.load_otb, dir=otb_dir, kwargs=dict(subset='tb_50')),
    dict(func=trackdata.load_otb, dir=otb_dir, kwargs=dict(subset='tb_100')),
    dict(func=trackdata.load_dtb70, dir=dtb70_dir, kwargs=dict()),
    dict(func=trackdata.load_tlp, dir=tlp_dir, kwargs=dict()),
    dict(func=trackdata.load_vot, dir=vot2013_dir, kwargs=dict()),
    dict(func=trackdata.load_vot, dir=vot2014_dir, kwargs=dict()),
    dict(func=trackdata.load_vot, dir=vot2015_dir, kwargs=dict()),
    dict(func=trackdata.load_vot, dir=vot2016_dir, kwargs=dict()),
    dict(func=trackdata.load_vot, dir=vot2017_dir, kwargs=dict()),
    dict(func=trackdata.load_nuspro, dir=nuspro_dir, kwargs=dict()),
    dict(func=trackdata.load_nfs, dir=nfs_dir, kwargs=dict(fps=240)),
    dict(func=trackdata.load_nfs, dir=nfs_dir, kwargs=dict(fps=30)),
    dict(func=trackdata.load_tc128, dir=tc128_dir, kwargs=dict(keep_prev=False)),
    dict(func=trackdata.load_tc128, dir=tc128_dir, kwargs=dict(keep_prev=True)),
    dict(func=trackdata.load_uav123, dir=uav123_dir, kwargs=dict()),
    dict(func=trackdata.load_alov, dir=alov_dir, kwargs=dict()),
    dict(func=trackdata.load_ilsvrc, dir=ilsvrc_dir, kwargs=dict(subset='val')),
    dict(func=trackdata.load_ilsvrc, dir=ilsvrc_dir, kwargs=dict(subset='train')),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_root', metavar='data/')
    args = parser.parse_args()

    for x in datasets:
        print(x)
        dataset_dir = os.path.join(args.data_root, x['dir'])
        start = time.time()
        dataset = x['func'](dataset_dir, **x['kwargs'])
        dur = time.time() - start
        print('number of tracks:', len(dataset.tracks()))
        print('time to load: {:.3g} sec'.format(dur))
        trackdata.dataset.assert_image_files_exist(dataset_dir, dataset)


if __name__ == '__main__':
    main()
