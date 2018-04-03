#!/bin/bash

# Use environment variable to set year.
VOT_YEAR="${VOT_YEAR:-2017}"

dl="$(readlink -m "${1:-"./dl/vot${VOT_YEAR}"}")"

mkdir -p "${dl}"
(
    cd "${dl}"
    wget -c "http://data.votchallenge.net/vot${VOT_YEAR}/vot${VOT_YEAR}.zip"
)
