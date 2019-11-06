#!/bin/bash

SCRIPT_DIR="$(cd $(dirname $0) && pwd)"
PROJECT_DIR="${SCRIPT_DIR}/.."
TWITTER_CONTROLLER_DIR="${PROJECT_DIR}/TwitterController"
TWEET_CRAWLER_DIR="${PROJECT_DIR}/tweetCrawler"
TARGET_DATE=$(date --date='a month ago' +'%Y-%m')

RECOMMENDED_USERS=$("${TWITTER_CONTROLLER_DIR}/get_recommend_accounts.py" -c 3 "${TWITTER_CONTROLLER_DIR}/twitter_auth")

echo "${RECOMMENDED_USERS}" | parallel python3 "${TWEET_CRAWLER_DIR}/main.py" -c ${TARGET_DATE} "{}"
