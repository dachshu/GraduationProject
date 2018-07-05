#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0) && pwd)
CRAWLER_DIR=${SCRIPT_DIR}/crawler
CRAWLED_DATA_DIR=${CRAWLER_DIR}/crawled_data/daum_news
FILTER_DIR=${SCRIPT_DIR}/DaumFilter
CHAR_RNN_DIR=${SCRIPT_DIR}/char-rnn-tensorflow
NMT_DIR=${SCRIPT_DIR}/nmt
CRAWL_DATE=$(date '+%Y%m%d' -d "yesterday")

# CharRNN 학습 데이터 준비
${CRAWLER_DIR}/DaumCrawler.py --date ${CRAWL_DATE}
echo -e "${CRAWLED_DATA_DIR}/${CRAWL_DATE}" | ${FILTER_DIR}/make_data.sh

mkdir -p ${CHAR_RNN_DIR}/data/news
cp ${FILTER_DIR}/output/char_rnn_data.txt ${CHAR_RNN_DIR}/data/news/input.txt

# NMT 학습 데이터 준비
NMT_ADDTIONAL_DATE=$(date '+%Y%m%d' -d "2 day ago")
echo -e "${CRAWLED_DATA_DIR}/${CRAWL_DATE}\n${CRAWLED_DATA_DIR}/${NMT_ADDTIONAL_DATE}" | ${FILTER_DIR}/make_data.sh
cp ${FILTER_DIR}/output/*.comment ${NMT_DIR}/train/
cp ${FILTER_DIR}/output/*.title ${NMT_DIR}/train/

