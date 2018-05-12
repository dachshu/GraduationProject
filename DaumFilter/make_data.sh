#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0) && pwd)
OUT_DIR=${SCRIPT_DIR}/output
OUT_JSON_NAME=${OUT_DIR}/output.json

mkdir -p ${OUT_DIR}
./filter.py ${ARCHIVES_DIR} -o ${OUT_JSON_NAME} 0<&0
./make_training_input.py space ${OUT_JSON_NAME} --out_dir ${OUT_DIR} --separate_title
./separate_dataset.py ${OUT_DIR}/output.title ${OUT_DIR}/output.comment ${OUT_DIR}/output.vocab --out_dir ${OUT_DIR}
cp -f ${OUT_DIR}/*.title ${OUT_DIR}/*.comment -t ${SCRIPT_DIR}/../nmt/train
