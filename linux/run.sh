#!bin/bash

cd /home/fightthebyte/teia/linux 
docker run -d --rm -it --env ACCEPT_LICENSE=true --publish 1080:1080 tts-standalone 
source /home/fightthebyte/miniconda3/etc/profile.d/conda.sh
conda activate teia 
python3 ./run.py
