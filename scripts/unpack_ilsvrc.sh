#!/bin/bash

dl="$(readlink -m "${1:-./dl/ilsvrc}")"
data="$(readlink -m "${2:-./data/ilsvrc}")"

mkdir -p "${data}"
(
    cd "${data}"
    tar -xzf "${dl}/ILSVRC2015_VID.tar.gz"
)
