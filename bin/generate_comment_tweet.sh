#!/bin/bash

PROJECT_DIR=$(cd $(dirname $0)/.. && pwd)

TODAY=$(date '+%Y-%m-%d')
LOG_DIR=${PROJECT_DIR}/log/${TODAY}
GENERAL_LOG_PATH=${LOG_DIR}/general.log
touch ${GENERAL_LOG_PATH}

DETAIL_LOGS_DIR=${LOG_DIR}/detail
mkdir -p ${DETAIL_LOGS_DIR}
#detail log path

# get a daum main news's title and url
NEWS_TITLE_N_URL=$(./get_daum_main_news.sh)
NEWS_TITLE=$(echo "${NEWS_TITLE_N_URL}" | head -1)
NEWS_URL=$(echo "${NEWS_TITLE_N_URL}" | tail -1)
echo "selected news : ${NEWS_TITLE}"

# tweet text file
OUTPUT_FILE_NAME=$(echo "${NEWS_TITLE}" | md5sum | awk '{printf "%s_comment_tweet.txt", $1}')
OUTPUT_FILE_PATH=$(echo "../results/${TODAY}/${OUTPUT_FILE_NAME}")
echo ${OUTPUT_FILE_PATH}
echo -e "${NEWS_TITLE_N_URL}\n" > "${OUTPUT_FILE_PATH}"

# generate comment of charRnn model
CHAR_RNN_OUTPUT_DIR=$(./generate_charRNN_comment.sh "${NEWS_TITLE}"| tail -1 | awk '{printf $4}')
echo ${CHAR_RNN_OUTPUT_DIR}
cat "${CHAR_RNN_OUTPUT_DIR}/output.txt" >> ${OUTPUT_FILE_PATH}

# generate commnet of nmt model
NMT_OUTPUT_DIR=$(./generate_nmt_comment.sh "${NEWS_TITLE}" | tail -1 | awk '{printf $4}')
echo ${NMT_OUTPUT_DIR}
cat "${NMT_OUTPUT_DIR}/output.txt" >> "${OUTPUT_FILE_PATH}"

# tweet generated comments
TWEET_TEXT=$(cat ${OUTPUT_FILE_PATH})
./upload_tweet.sh "${TWEET_TEXT}"
