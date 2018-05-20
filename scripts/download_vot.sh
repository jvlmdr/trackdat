#!/bin/bash

# Use environment variable to set year.
VOT_YEAR="${VOT_YEAR:-2018}"
VOT_CHALLENGE="${VOT_CHALLENGE:-main}"

if [ "${VOT_CHALLENGE}" == "main" ]; then
    name="vot${VOT_YEAR}"
else
    name="vot${VOT_YEAR}_${VOT_CHALLENGE}"
fi

dl="${1:-"./dl/${name}"}"
mkdir -p "${dl}"
(
    cd "${dl}"
    base_url="http://data.votchallenge.net/vot${VOT_YEAR}/${VOT_CHALLENGE}"
    wget -c "${base_url}/description.json"
    cat description.json | jq -r '.sequences[] | .channels.color.url' >zips.txt
    mkdir -p videos
    (
        cd videos
        cat ../zips.txt | xargs -P 4 -t -I{} wget -nv -c "${base_url}/{}"
    )
)
