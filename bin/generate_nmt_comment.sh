#!/bin/bash

NEWS_TITLE=$1
DIR_NAME=$(echo "${NEWS_TITLE}" | md5sum | awk '{printf "%s_nmt", $1}')
TODAY=$(date '+%Y-%m-%d')
IN_OUT_DIR=$(echo "../results/${TODAY}/${DIR_NAME}")
MODEL_DIR=$(echo "../nmt")
mkdir -p ${IN_OUT_DIR}
echo "${NEWS_TITLE}" > ${IN_OUT_DIR}/input.txt
${MODEL_DIR}/infer.sh ${MODEL_DIR}/save/model ${IN_OUT_DIR}/input.txt ${IN_OUT_DIR}/output.txt
echo "[output dir name] ${IN_OUT_DIR}"
