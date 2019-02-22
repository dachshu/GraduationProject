#!/bin/bash

function exit_if_err() {
    ERR_CODE=$?
    if [ ${ERR_CODE} -ne 0 ]
    then
        echo "[ERROR] Error has occurred in $@" 1>&2
        exit ${ERR_CODE}
    fi
}


SCRIPT_DIR=$(cd $(dirname $0) && pwd)
PROJECT_DIR=${SCRIPT_DIR}/..
NEWS_TITLE=$1
if [ -z "${NEWS_TITLE}" ];
then
    read line
    NEWS_TITLE="${line}"
    while read line; do
        NEWS_TITLE="${NEWS_TITLE}\n${line}"
    done
fi
NEWS_TITLE=$(echo -e "${NEWS_TITLE}" | ${SCRIPT_DIR}/seperate_morphemes.py)
exit_if_err "seperate news title"
echo "${NEWS_TITLE}" 1>&2

in_out_dir="${PROJECT_DIR}/results/nmt"
model_dir="${PROJECT_DIR}/nmt"
mkdir -p ${in_out_dir}
echo -e "${news_title}" > ${in_out_dir}/input.txt
${model_dir}/infer.sh ${model_dir}/save/model ${in_out_dir}/input.txt ${in_out_dir}/output.txt
exit_if_err "inferring nmt"
cat "${in_out_dir}/output.txt"
