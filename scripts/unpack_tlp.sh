#!/bin/bash

dl="$(readlink -m "${1:-./dl/tlp}")"
data="$(readlink -m "${2:-./data/tlp}")"

mkdir -p "${data}"
(
    cd "${data}"
    ls "${dl}"/videos/*.zip | xargs -t -n 1 unzip -q -o
)
