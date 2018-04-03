#!/bin/bash

dl="$(readlink -m "${1:-./dl/alov}")"

mkdir -p "${dl}"
(
    cd "${dl}"
    wget -c "http://isis-data.science.uva.nl/alov/alov300++GT_txtFiles.zip" && \
        wget -c "http://isis-data.science.uva.nl/alov/alov300++_frames.zip"
)
