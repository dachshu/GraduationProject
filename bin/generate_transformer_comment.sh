#!/bin/bash

# 1st argument : model dir
# 2nd argument : vocab_file
# 3rd argument : text to translate

function exit_if_err() {
    ERR_CODE=$?
    if [ $[ERR_CODE] -ne 0 ]
    then
        echo "[ERROR] Error has occured in $@" 1>&2
        exit ${ERR_CODE}
    fi
}

MODEL_DIR=$1
MODEL_DIR=$(cd ${MODEL_DIR} && pwd)
VOCAB_FILE=$2
VOCAB_FILE_DIR=$(cd $(dirname "${VOCAB_FILE}") && pwd)
VOCAB_FILE=$(basename "${VOCAB_FILE}")

SCRIPT_DIR=$(cd $(dirname "$0") && pwd)
PROJECT_DIR=$(cd $(dirname "$0")/.. && pwd)
TRANS_DIR=${PROJECT_DIR}/models
INNER_TRANS_DIR=/models
INNER_MODEL_DIR=/trained_model
INNER_VOCAB_FILE_DIR=/vocab_dir

NEWS_TITLE=$3
if [ -z "${NEWS_TITLE}" ];
then
    read line
    NEWS_TITLE="${line}"
    while read line; do
        NEWS_TITLE="${NEWS_TITLE}\n${line}"
    done
fi
NEWS_TITLE=$(echo -e "${NEWS_TITLE}" | ${SCRIPT_DIR}/seperate_morphemes.py)
exit_if_err "seperate news title in transformer"
echo -e "${NEWS_TITLE}" > ${TRANS_DIR}/input.txt
touch ${TRANS_DIR}/output.txt


docker run --runtime=nvidia --rm -u $(id -u):$(id -g) -v "${TRANS_DIR}:${INNER_TRANS_DIR}" -v "${MODEL_DIR}:${INNER_MODEL_DIR}" -v "${VOCAB_FILE_DIR}:${INNER_VOCAB_FILE_DIR}" \
    tensorflow_models \
    bash -c "export PYTHONIOENCODING=UTF-8 && export PYTHONPATH=${INNER_TRANS_DIR} && cd ${INNER_TRANS_DIR}/official/transformer \
    && python3 translate.py --model_dir ${INNER_MODEL_DIR} --vocab_file ${INNER_VOCAB_FILE_DIR}/${VOCAB_FILE} \
    --param_set base \
    --file ${INNER_TRANS_DIR}/input.txt --file_out ${INNER_TRANS_DIR}/output.txt"

exit_if_err "inferring transformer"

cat "${TRANS_DIR}/output.txt"
#exit $?
