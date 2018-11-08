#!/bin/bash

NEWS_TITLE=$1
DIR_NAME="$(echo "${NEWS_TITLE}" | awk '{printf "%s", $1}')_$(date +%T)_charRNN"
#DIR_NAME=$(echo "${NEWS_TITLE}" | md5sum | awk '{printf "%s_charRNN", $1}')
TODAY=$(date '+%Y-%m-%d')
IN_OUT_DIR=$(echo "../results/${TODAY}/${DIR_NAME}")
MODEL_DIR=$(echo "../kor-char-rnn-tensorflow")
mkdir -p ${IN_OUT_DIR}
echo "${NEWS_TITLE}" > ${IN_OUT_DIR}/input.txt
python3 ${MODEL_DIR}/sample.py --save_dir ${MODEL_DIR}/save/news --prime "$(head -1 ${IN_OUT_DIR}/input.txt)" \
    --output_file "${IN_OUT_DIR}/output.txt" 
echo "[output dir name] ${IN_OUT_DIR}"
