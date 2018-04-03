#!/bin/bash

dl="$(readlink -m "${1:-./dl/uav123}")"
data="$(readlink -m "${2:-./data/uav123}")"

mkdir -p "${data}"
(
    cd "${data}"
    unzip -o "${dl}/Dataset_UAV123.zip"
)
