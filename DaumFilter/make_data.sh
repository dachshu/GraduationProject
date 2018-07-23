#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0) && pwd)
OUT_DIR=${SCRIPT_DIR}/output
OUT_JSON_NAME=${OUT_DIR}/output.json

if [ -n "$1" ]; then
    ADDITIONAL_CMD="-m $1"
fi

mkdir -p ${OUT_DIR}
${SCRIPT_DIR}/filter.py -o ${OUT_JSON_NAME} ${ADDITIONAL_CMD} 0<&0
$(cd ${SCRIPT_DIR} && python3 process_data.py && mv *.txt -t ${OUT_DIR})
sed -i "/^$/d" ${OUT_DIR}/*.txt
${SCRIPT_DIR}/separate_dataset.py ${OUT_DIR}/title.txt ${OUT_DIR}/comment.txt ${OUT_DIR}/vocab.txt --out_dir ${OUT_DIR}
