#!/bin/bash

dl="$(readlink -m "${1:-./dl/tlp}")"

mkdir -p "${dl}"
(
    cd "${dl}"
    wget -c https://amoudgl.github.io/tlp/datasets/index.html
    # Take Google Drive links that appear on a line by themselves.
    cat index.html | grep 'drive\.google\.com.*id=' | grep -v '<[^a]' | \
        sed -e 's/.*id=//' | sed -e 's/[^a-zA-Z0-9_-].*//' >ids.txt
    mkdir -p videos
    (
        cd videos
        cat ../ids.txt | xargs -t -n 1 gdrive download --skip
    )
)
