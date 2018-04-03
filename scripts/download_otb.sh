#!/bin/bash

dl="$(readlink -m "${1:-./dl/otb}")"

mkdir -p "${dl}"
(
    cd "${dl}"
    wget -c "http://cvlab.hanyang.ac.kr/tracker_benchmark/datasets.html" || exit 1
    cat datasets.html | grep zip | sed -e 's/.*href="//' | sed -e 's/".*//' >zips.txt
    mkdir -p videos
    (
        cd videos
        cat ../zips.txt | xargs -t -I{} wget -c "http://cvlab.hanyang.ac.kr/tracker_benchmark/{}"
    )
)
