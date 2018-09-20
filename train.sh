#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0) && pwd)
CRAWLER_DIR=${SCRIPT_DIR}/crawler
CRAWLED_DATA_DIR=${CRAWLER_DIR}/crawled_data/daum_news
FILTER_DIR=${SCRIPT_DIR}/DaumFilter
CHAR_RNN_DIR=${SCRIPT_DIR}/kor-char-rnn-tensorflow
NMT_DIR=${SCRIPT_DIR}/nmt
CRAWL_DATE=$(date '+%Y%m%d' -d "yesterday")
TODAY=$(date '+%Y-%m-%d')

# CharRNN 학습 데이터 준비
echo "=== Start Crawling ${CRAWL_DATE} ==="
${CRAWLER_DIR}/DaumCrawler.py --date ${CRAWL_DATE} -p 4

echo "=== Filtering Crawled Data ==="
echo -e "${CRAWLED_DATA_DIR}/${CRAWL_DATE}" | ${FILTER_DIR}/make_data.sh

echo "=== Start Learning ==="
mkdir -p ${CHAR_RNN_DIR}/data/news
cp ${FILTER_DIR}/output/char_rnn_data.txt ${CHAR_RNN_DIR}/data/news/input.txt

# 백업이 4개 이상이면 기존 것 제거
if [ $(ls ${CHAR_RNN_DIR}/save/news.bak* | wc -l) -gt 4 ]; then
    rm $(ls ${CHAR_RNN_DIR}/save/news.bak* | head -1)
fi
# CharRNN 기존 모델 백업
tar -czf "${CHAR_RNN_DIR}/save/news.bak-${TODAY}.tgz" -C ${CHAR_RNN_DIR}/save news/

cd ${CHAR_RNN_DIR} && ${CHAR_RNN_DIR}/train.sh --init_from ${CHAR_RNN_DIR}/save/news

# NMT 학습 데이터 준비
NMT_ADDTIONAL_DATE=$(date '+%Y%m%d' -d "2 day ago")
echo -e "${CRAWLED_DATA_DIR}/${CRAWL_DATE}\n${CRAWLED_DATA_DIR}/${NMT_ADDTIONAL_DATE}" | ${FILTER_DIR}/make_data.sh 7000
cp -f ${FILTER_DIR}/output/*.title ${FILTER_DIR}/output/*.comment -t ${NMT_DIR}/train

docker run --rm -v ${NMT_DIR}:/nmt tensorflow/tensorflow:nightly-devel-py3 bash -c \
    "rm -r /nmt/save/model/*"
${NMT_DIR}/train.sh
