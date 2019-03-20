#!/bin/bash

dl="${1:-./dl/tracknet}"
data="${2:-./data/tracknet}"

mkdir -p "${data}"
dl="$( cd "${dl}" && pwd )"
data="$( cd "${data}" && pwd )"

# Copy anno and zips from dl/data/ to data/.
# (This is inefficient, could use symlinks instead.)
rsync -av "${dl}/data/" "${data}/" || exit 1

(
    cd "${dl}/TrackingNet-devkit" || exit 1
    python extract_frame.py --trackingnet_dir "${data}" || exit 1
) || exit 1

rm -r "${data}"/*/zips || exit 1
