#!/bin/bash

dl="$(readlink -m "${1:-./dl/dtb70}")"
data="$(readlink -m "${2:-./data/dtb70}")"

mkdir -p "${data}"
(
    cd "${data}"
    tar -xzf "${dl}/DTB70.tar.gz"
)
