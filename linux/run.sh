#!/bin/bash

cd common || cd ../common || exit

# Spin up Watson container
docker run -d --rm -it --env ACCEPT_LICENSE=true --publish 1080:1080 tts-standalone 

. ~/miniconda3/etc/profile.d/conda.sh

conda activate teia 

python3 ./run.py
