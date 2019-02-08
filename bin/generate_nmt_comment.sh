#!/bin/bash

function exit_if_err() {
    ERR_CODE=$?
    [ ${ERR_CODE} -ne 0 ] && echo "[ERROR] Error has occurred in $@" 1>&2; exit ${ERR_CODE}
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

DIR_NAME="nmt"
IN_OUT_DIR=$(echo "../results/${DIR_NAME}")
MODEL_DIR=$(echo "../nmt")
mkdir -p ${IN_OUT_DIR}
echo -e "${NEWS_TITLE}" > ${IN_OUT_DIR}/input.txt
${MODEL_DIR}/infer.sh ${MODEL_DIR}/save/model ${IN_OUT_DIR}/input.txt ${IN_OUT_DIR}/output.txt
exit_if_err "inferring nmt"
cat "${IN_OUT_DIR}/output.txt"


