#!/bin/bash

dl="$(readlink -m "${1:-./dl/tc128}")"

mkdir -p "${dl}"
(
    cd "${dl}"
    wget -c "http://www.dabi.temple.edu/~hbling/data/TColor-128/Temple-color-128.zip"
)
