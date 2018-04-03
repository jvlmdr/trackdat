#!/bin/bash

dl="$(readlink -m "${1:-./dl/nfs}")"
data="$(readlink -m "${2:-./data/nfs}")"

mkdir -p "${data}"
(
    cd "${data}"
    ls "${dl}"/*.zip | xargs -t -n 1 unzip -q -o
)
