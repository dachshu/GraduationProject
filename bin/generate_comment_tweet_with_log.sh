#!/bin/bash

PROJECT_DIR=$(cd $(dirname $0)/.. && pwd)

TODAY="$(date '+%Y-%m-%d')"
TIME="$(date +%T)"
LOG_DIR=${PROJECT_DIR}/log/${TODAY}
DETAIL_LOG_DIR=${LOG_DIR}/detail/upload_comment_tweet
DETAIL_LOG_PATH="${DETAIL_LOG_DIR}/${TIME}.log"
mkdir -p ${DETAIL_LOG_DIR}
touch "${DETAIL_LOG_PATH}"

cd "${PROJECT_DIR}/bin"
./generate_comment_tweet.sh > ${DETAIL_LOG_PATH} 2>&1

