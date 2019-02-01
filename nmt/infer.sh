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
INPUT_DIR=$(cd $(dirname "${INPUT_FILE}") && pwd)
INNER_INPUT_DIR=/input
OUTPUT_DIR=$(cd $(dirname "${OUTPUT_FILE}") && pwd)
INNER_OUTPUT_DIR=/output
INNER_MODEL_DIR=/nmt_output # 모델의 hparam에 training 할때의 경로가 저장되므로 똑같이 맞춰줘야 함.
INNER_VOCAB_DIR=/nmt_input

INPUT_FILE=${INPUT_FILE//${INPUT_DIR}/${INNER_INPUT_DIR}}
OUTPUT_FILE=${OUTPUT_FILE//${OUTPUT_DIR}/${INNER_OUTPUT_DIR}}

nvidia-docker run --rm -v "${SOURCE_DIR}:${VOLUME_DIR}" -v "${INPUT_DIR}:${INNER_INPUT_DIR}" -v "${OUTPUT_DIR}:${INNER_OUTPUT_DIR}" -v "${MODEL_DIR}:${INNER_MODEL_DIR}" -v "${MODEL_DIR}:${INNER_VOCAB_DIR}" tensorflow/tensorflow:nightly-devel-gpu-py3 bash -c "export PYTHONIOENCODING=UTF-8 && cd ${VOLUME_DIR} && python3 -m nmt.nmt \
    --src=title --tgt=comment \
    --ckpt=${INNER_MODEL_DIR}/${CKPT_FILE} \
    --out_dir=${INNER_MODEL_DIR} \
    --inference_input_file=${INPUT_FILE} \
    --inference_output_file=${OUTPUT_FILE}"

exit $?
