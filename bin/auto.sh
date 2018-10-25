#!/bin/bash

PROJECT_DIR=$(cd $(dirname $0)/.. && pwd)
SCRIPT_DIR="${PROJECT_DIR}/bin"
CRAWLER_DIR=${PROJECT_DIR}/crawler
CRAWLED_DATA_DIR=${CRAWLER_DIR}/crawled_data/daum_news
CHAR_RNN_DIR=${PROJECT_DIR}/kor-char-rnn-tensorflow
CHAR_RNN_MODEL_DIR=${CHAR_RNN_DIR}/model/news
NMT_DIR=${PROJECT_DIR}/nmt
NMT_MODEL_DIR=${NMT_DIR}/model
CRAWL_DATE=$(date '+%Y%m%d' -d "yesterday")
TODAY=$(date '+%Y%m%d')
RESULT_DIR="${PROJECT_DIR}/results/${TODAY}"

#mkdir -p ${PROJECT_DIR}/log/${TODAY}

mkdir -p "${RESULT_DIR}"

# 어제 뉴스 크롤링
${CRAWLER_DIR}/DaumCrawler.py "${CRAWL_DATE}" "${CRAWLED_DATA_DIR}" -p 4

# 뉴스 필터링
${SCRIPT_DIR}/news_filter.py "${CRAWLED_DATA_DIR}/${CRAWL_DATE}" ${RESULT_DIR}/daum_news.json

# CharRNN 입력 데이터 생성
${SCRIPT_DIR}/make_input_for_char_rnn.py "${RESULT_DIR}/daum_news.json" "${RESULT_DIR}/char_rnn_input"

# CharRNN 학습
if [ -d "${CHAR_RNN_MODEL_DIR}" ]; then
    CHAR_RNN_OPTION="${CHAR_RNN_MODEL_DIR}"
fi
${SCRIPT_DIR}/train_char_rnn.sh "${RESULT_DIR}/char_rnn_input" "${CHAR_RNN_MODEL_DIR}" ${CHAR_RNN_OPTION}

# NMT 입력 데이터 생성
${SCRIPT_DIR}/make_input_for_nmt.py "${RESULT_DIR}/daum_news.json" "${RESULT_DIR}/nmt_input"

# NMT 학습
${SCRIPT_DIR}/train_nmt.sh "${RESULT_DIR}/nmt_input" "${NMT_MODEL_DIR}"
