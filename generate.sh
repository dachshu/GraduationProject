#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0) && pwd)
CHAR_RNN_DIR=${SCRIPT_DIR}/char-rnn-tensorflow
NMT_DIR=${SCRIPT_DIR}/nmt

echo "=== Generating Times ==="
TIME_GENERATOR_DIR=${SCRIPT_DIR}/CommentTimeGenerator
cd ${TIME_GENERATOR_DIR}
LATEST_TIME=$(cat latest_generated_time)
GENERATED_TIMES=$(./TimeModel.py sample ${LATEST_TIME})

echo "=== Generating Comments ==="
TODAY=$(date '+%Y-%m-%d')
for t in ${GENERATED_TIMES}; do
    HOUR=$(echo "${t}/3600" | bc)
    MINUTE=$(echo "${t}%3600/60" | bc)
    SECOND=$(echo "${t}%3600%60" | bc)

    TARGET_TIME=$(date --date="${TODAY} ${HOUR}:${MINUTE}:${SECOND}" '+%s')
    CURRENT_TIME=$(date '+%s')

    if [ $(echo "${TARGET_TIME}<${CURRENT_TIME}" | bc) -eq 1 ]; then
        continue
    fi

    PERIOD_TO_SLEEP=$((TARGET_TIME-CURRENT_TIME))
    echo "Sleep for ${PERIOD_TO_SLEEP}s"
    sleep ${PERIOD_TO_SLEEP}

    # get a news article
    ARTICLE_TITLES_LINKS=$(${SCRIPT_DIR}/GetDaumMainNews.py)
    SELECTED_TITLE=$(echo "${ARTICLE_TITLES_LINKS}" | awk 'NR % 2 == 1' | shuf -n 1)
    # generate comments of the article via char-rnn and seq2seq model
    echo "Generate a comment from the title: ${SELECTED_TITLE}"
    echo "${SELECTED_TITLE}" > ${CHAR_RNN_DIR}/input_for_generation.txt
    ${CHAR_RNN_DIR}/run.py infer --input_file ${CHAR_RNN_DIR}/input_for_generation.txt
    CRNN_RESULT="$(cat ${CHAR_RNN_DIR}/infer_output.txt)"

    echo "${SELECTED_TITLE}" > ${NMT_DIR}/input_for_generation.txt
    ${NMT_DIR}/infer.sh ${NMT_DIR}/save/model ${NMT_DIR}/input_for_generation.txt ${NMT_DIR}/infer_output.txt
    NMT_RESULT="$(cat ${NMT_DIR}/infer_output.txt)"
    # TODO:
    # upload comment and original news web link to twitter

done

cd ${TIME_GENERATOR_DIR} && echo "${GENERATED_TIMES}" | tail -1 > latest_generated_time
