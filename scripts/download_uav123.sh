#!/bin/bash

dl="$(readlink -m "${1:-./dl/uav123}")"

mkdir -p "${dl}"
(
    cd "${dl}"
    gdrive download --skip 0B6sQMCU1i4NbNGxWQzRVak5yLWs
)
