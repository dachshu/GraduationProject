#!/bin/bash

NEWS_TITLE=$1
DIR_NAME="nmt"
IN_OUT_DIR=$(echo "../results/${DIR_NAME}")
MODEL_DIR=$(echo "../nmt")
mkdir -p ${IN_OUT_DIR}
echo "${NEWS_TITLE}" > ${IN_OUT_DIR}/input.txt
${MODEL_DIR}/infer.sh ${MODEL_DIR}/save/model ${IN_OUT_DIR}/input.txt ${IN_OUT_DIR}/output.txt
echo "$(cat "${IN_OUT_DIR}/output.txt")"


