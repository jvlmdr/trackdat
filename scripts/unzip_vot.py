from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import json
import os
import zipfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', help='e.g. dl/vot2018')
    parser.add_argument('dl_dir', help='e.g. data/vot2018')
    args = parser.parse_args()

    with open(os.path.join(args.data_dir, 'description.json'), 'r') as f:
        dataset = json.load(f)

    for seq in dataset['sequences']:
        filename = seq['channels']['color']['url'].split('/')[-1]
        print('extract "{}"'.format(filename))
        with zipfile.ZipFile(os.path.join(args.data_dir, 'videos', filename), 'r') as zf:
            zf.extractall(os.path.join(args.dl_dir, seq['name']))

if __name__ == '__main__':
    main()
