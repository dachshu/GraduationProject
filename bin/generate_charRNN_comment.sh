#!/bin/bash

function exit_if_err() {
    ERR_CODE=$?
    if [ ${ERR_CODE} -ne 0 ]
    then
        echo "[ERROR] Error has occurred in $@" 1>&2
        exit ${ERR_CODE}
    fi
}

NEWS_TITLE=$1

if [ -z "${NEWS_TITLE}" ];
then
    read line
    NEWS_TITLE="${line}"
    while read line; do
        NEWS_TITLE="${NEWS_TITLE}\n${line}"
    done
fi
#DIR_NAME="$(echo "${NEWS_TITLE}" | awk '{printf "%s", $1}')_$(date +%T)_charRNN"
#DIR_NAME=$(echo "${NEWS_TITLE}" | md5sum | awk '{printf "%s_charRNN", $1}')
TODAY=$(date '+%Y-%m-%d')
MODEL_DIR=$(echo "../kor-char-rnn-tensorflow")
echo -e "${NEWS_TITLE}" | while read title; do
    python3 ${MODEL_DIR}/sample.py --save_dir ${MODEL_DIR}/save/news --prime "$title"
    exit_if_err "inferring char rnn"
done
