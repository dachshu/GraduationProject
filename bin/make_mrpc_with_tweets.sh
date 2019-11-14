#!/bin/bash

PROJECT_DIR="$(cd $(dirname $0)/.. && pwd)"
SCRIPT_DIR="${PROJECT_DIR}/bin"
CRAWLER_DIR="${PROJECT_DIR}/crawler"
CRAWLED_DATA_DIR="${CRAWLER_DIR}/crawled_data/daum_news"
TWITTER_CONTROLLER_DIR="${PROJECT_DIR}/TwitterController"
TODAY=$(date '+%Y-%m-%d')
RESULT_DIR="${PROJECT_DIR}/results/${TODAY}"
TWEET_CRAWLER_DIR="${PROJECT_DIR}/tweetCrawler"
TWEET_DIR="${TWEET_CRAWLER_DIR}/tweets"
BERT_DATA_DIR="${RESULT_DIR}/bert_tweet"
TARGET_DATE=$(date --date='6 month ago' +'%Y-%m')

RECOMMENDED_USERS=$("${TWITTER_CONTROLLER_DIR}/get_recommend_accounts.py" -c 3 "${TWITTER_CONTROLLER_DIR}/twitter_auth")

echo "${RECOMMENDED_USERS}" | parallel "cd ${TWEET_CRAWLER_DIR} && python3 \"${TWEET_CRAWLER_DIR}/main.py\" -c ${TARGET_DATE} {} && python3 \"${TWEET_CRAWLER_DIR}/main.py\" -f text {}"

mkdir -p "${BERT_DATA_DIR}"
find ${CRAWLED_DATA_DIR}/* -type d | sort | tail -1 | ${SCRIPT_DIR}/news_filter.py -c 10 --out-plain-text > "${BERT_DATA_DIR}/comments"

while read -r user; do
    sed '/^$/d' "${TWEET_DIR}/${user}/data_text" > "${BERT_DATA_DIR}/${user}.twt"
    python3 "${SCRIPT_DIR}/bert_testdata_preprocess.py" "${BERT_DATA_DIR}/${user}.twt" "${BERT_DATA_DIR}/comments" "${BERT_DATA_DIR}/evel_data/${user}"
done <<< "${RECOMMENDED_USERS}"
