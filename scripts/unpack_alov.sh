#!/bin/bash

dl="$(readlink -m "${1:-./dl/alov}")"
data="$(readlink -m "${2:-./data/alov}")"

mkdir -p "${data}"
(
    cd "${data}"
    unzip -o "${dl}/alov300++GT_txtFiles.zip" && \
        unzip -o "${dl}/alov300++_frames.zip" && \
        rm -rf data && \
        mv imagedata++ data && \
        rsync -a alov300++_rectangleAnnotation_full/ data/ && \
        rm -r alov300++_rectangleAnnotation_full &&
        mv data/* ./ &&
        rmdir data
)
