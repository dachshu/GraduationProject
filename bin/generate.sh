#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0)/.. && pwd)

TODAY=$(date '+%Y-%m-%d')
LOG_DIR=${SCRIPT_DIR}/log/${TODAY}
# General log file path.
G_LOG_PATH=${LOG_DIR}/general.log
touch ${G_LOG_PATH}

DETAIL_LOGS_DIR=${LOG_DIR}/detail
mkdir -p ${DETAIL_LOGS_DIR}
TIME_LOG_PATH=${DETAIL_LOGS_DIR}/upload_time.log
AT_LOG_PATH=${DETAIL_LOGS_DIR}/at.log

echo "[INFO] Start generating upload time" >> ${G_LOG_PATH}
TIME_GENERATOR_DIR=${SCRIPT_DIR}/CommentTimeGenerator
cd ${TIME_GENERATOR_DIR}
LATEST_TIME=$(cat latest_generated_time)
GENERATED_TIMES=$(./TimeModel.py sample ${LATEST_TIME})
echo "${GENERATED_TIMES}" > ${TIME_LOG_PATH}

echo "[INFO] Start generating comments" >> ${G_LOG_PATH}
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

    echo "/bin/bash -f ${SCRIPT_DIR}/generate_comment.sh >> ${AT_LOG_PATH}" | at ${HOUR}:${MINITE}
done

( cd ${TIME_GENERATOR_DIR} && echo "${GENERATED_TIMES}" | tail -1 > latest_generated_time )

