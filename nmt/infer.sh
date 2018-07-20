#!/bin/bash

MODEL_DIR=${1:?give a directory in which saved model is}
INPUT_FILE="${2:?give an input text file to decode}"
OUTPUT_FILE="${3:?give an output file name to store decoded result}"

# get full path
INPUT_FILE=$(readlink -f "${INPUT_FILE}")
OUTPUT_FILE=$(readlink -f "${OUTPUT_FILE}")
MODEL_DIR=$(readlink -f ${MODEL_DIR})
CKPT_FILE=$(ls ${MODEL_DIR} | grep "ckpt.\+\.index" | sort -V -r | head -1)
CKPT_FILE=${CKPT_FILE%'.index'}

SOURCE_DIR=$(cd $(dirname "$0") && pwd)
VOLUME_DIR=/nmt

INPUT_FILE=${INPUT_FILE//${SOURCE_DIR}/${VOLUME_DIR}}
OUTPUT_FILE=${OUTPUT_FILE//${SOURCE_DIR}/${VOLUME_DIR}}
MODEL_DIR=${MODEL_DIR//${SOURCE_DIR}/${VOLUME_DIR}}


nvidia-docker run --rm -v ${SOURCE_DIR}:${VOLUME_DIR} tensorflow/tensorflow:nightly-devel-gpu-py3 bash -c "export PYTHONIOENCODING=UTF-8 && cd /nmt && python3 -m nmt.nmt \
    --src=title --tgt=comment \
    --ckpt=${MODEL_DIR}/${CKPT_FILE} \
    --out_dir=${MODEL_DIR} \
    --vocab_prefix=${VOLUME_DIR}/train \
    --share_vocab \
    --inference_input_file="${INPUT_FILE}" \
    --inference_output_file="${OUTPUT_FILE}""
