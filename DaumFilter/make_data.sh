#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0) && pwd)
OUT_DIR=${SCRIPT_DIR}/output
OUT_JSON_NAME=${OUT_DIR}/output.json

mkdir -p ${OUT_DIR}
${SCRIPT_DIR}/filter.py ${ARCHIVES_DIR} -o ${OUT_JSON_NAME} 0<&0
$(cd ${SCRIPT_DIR} && python3 process_data.py && mv *.txt -t ${OUT_DIR})
sed -i "/^$/d" ${OUT_DIR}/*.txt
${SCRIPT_DIR}/separate_dataset.py ${OUT_DIR}/title.txt ${OUT_DIR}/comment.txt ${OUT_DIR}/vocab.txt --out_dir ${OUT_DIR}
cp -f ${OUT_DIR}/*.title ${OUT_DIR}/*.comment -t ${SCRIPT_DIR}/../nmt/train
