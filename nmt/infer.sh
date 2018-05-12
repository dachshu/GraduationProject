#!/bin/bash

INPUT_FILE="${1:?give input text file to decode}"
OUTPUT_FILE="${2:?give output file name to store decoded result}"

# get full path
INPUT_FILE=$(cd $(dirname "${INPUT_FILE}") && pwd)/${INPUT_FILE}
OUTPUT_FILE=$(cd $(dirname "${OUTPUT_FILE}") && pwd)/${OUTPUT_FILE}

SOURCE_DIR=$(cd $(dirname "$0") && pwd)
VOLUME_DIR=/nmt

INPUT_FILE=${INPUT_FILE//${SOURCE_DIR}/${VOLUME_DIR}}
OUTPUT_FILE=${OUTPUT_FILE//${SOURCE_DIR}/${VOLUME_DIR}}

docker run --rm -v ${SOURCE_DIR}:${VOLUME_DIR} tensorflow/tensorflow:nightly-devel-py3 bash -c "cd /nmt && python3 -m nmt.nmt \
    --src=title --tgt=comment \
    --ckpt=${VOLUME_DIR}/save/model/translate.ckpt-11000 \
    --out_dir=${VOLUME_DIR}/save/model \
    --vocab_prefix=${VOLUME_DIR}/train \
    --inference_input_file="${INPUT_FILE}" \
    --inference_output_file="${OUTPUT_FILE}""
