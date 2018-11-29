#!/bin/bash

NEWS_TITLE=$1
DIR_NAME="$(echo "${NEWS_TITLE}" | awk '{printf "%s", $1}')_$(date +%T)_charRNN"
#DIR_NAME=$(echo "${NEWS_TITLE}" | md5sum | awk '{printf "%s_charRNN", $1}')
TODAY=$(date '+%Y-%m-%d')
MODEL_DIR=$(echo "../kor-char-rnn-tensorflow")
python3 ${MODEL_DIR}/sample.py --save_dir ${MODEL_DIR}/save/news --prime "$NEWS_TITLE"
