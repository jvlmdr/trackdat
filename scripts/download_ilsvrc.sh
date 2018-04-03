#!/bin/bash

dl="$(readlink -m "${1:-./dl/ilsvrc}")"

mkdir -p "${dl}"
(
    cd "${dl}"
    wget -c "http://bvisionweb1.cs.unc.edu/ilsvrc2015/ILSVRC2015_VID.tar.gz"
)
