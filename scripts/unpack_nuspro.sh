#!/bin/bash

dl="$(readlink -m "${1:-./dl/nuspro}")"
data="$(readlink -m "${2:-./data/nuspro}")"

mkdir -p "${data}"
(
    cd "${data}"
    ls "${dl}"/data/*.zip | xargs -t -n 1 unzip -q -o
)
