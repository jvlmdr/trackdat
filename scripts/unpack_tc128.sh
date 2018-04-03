#!/bin/bash

dl="$(readlink -m "${1:-./dl/tc128}")"
data="$(readlink -m "${2:-./data/tc128}")"

mkdir -p "${data}"
(
    cd "${data}"
    unzip -o "${dl}/Temple-color-128.zip"
)
