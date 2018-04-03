#!/bin/bash

# Use environment variable to set year.
VOT_YEAR="${VOT_YEAR:-2017}"

dl="$(readlink -m "${1:-"./dl/vot${VOT_YEAR}"}")"
data="$(readlink -m "${2:-"./data/vot${VOT_YEAR}"}")"

mkdir -p "${data}"
(
    cd "${data}"
    unzip -o "${dl}/vot${VOT_YEAR}.zip"
)
