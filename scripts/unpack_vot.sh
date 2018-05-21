#!/bin/bash

# Use environment variable to set year.
# For unpacking, these are only used for the default name.
VOT_YEAR="${VOT_YEAR:-2018}"
VOT_CHALLENGE="${VOT_CHALLENGE:-main}"

if [ "${VOT_CHALLENGE}" == "main" ]; then
    name="vot${VOT_YEAR}"
else
    name="vot${VOT_YEAR}_${VOT_CHALLENGE}"
fi

dl="${1:-"./dl/${name}"}"
data="${2:-"./data/${name}"}"
scripts="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

mkdir -p "${data}" || exit 1
cp "${dl}/description.json" "${data}/"|| exit 1
python "$scripts/unzip_vot.py" "$dl" "$data"
