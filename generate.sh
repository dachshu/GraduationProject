#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0) && pwd)

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

    $(echo "${SCRIPT_DIR}/generate_comment.sh 2>&1 | tee ${SCRIPT_DIR}/log/${TODAY}/generation-log" | at ${HOUR}:${MINUTE})
done

( cd ${TIME_GENERATOR_DIR} && echo "${GENERATED_TIMES}" | tail -1 > latest_generated_time )

