#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0) && pwd)
CRAWLER_DIR=${SCRIPT_DIR}/crawler
CRAWLED_DATA_DIR=${CRAWLER_DIR}/crawled_data/daum_news
FILTER_DIR=${SCRIPT_DIR}/DaumFilter
CHAR_RNN_DIR=${SCRIPT_DIR}/kor-char-rnn-tensorflow
NMT_DIR=${SCRIPT_DIR}/nmt
CRAWL_DATE=$(date '+%Y%m%d' -d "yesterday")
TODAY=$(date '+%Y-%m-%d')

LOG_DIR=${SCRIPT_DIR}/log/${TODAY}
# General log file path.
G_LOG_PATH=${LOG_DIR}/general.log
touch ${G_LOG_PATH}

DETAIL_LOGS_DIR=${LOG_DIR}/detail
mkdir -p ${DETAIL_LOGS_DIR}
CRAWLING_LOG_PATH=${DETAIL_LOGS_DIR}/crawling.log
FILTERING_LOG_PATH=${DETAIL_LOGS_DIR}/filtering.log
CHAR_RNN_LOG_PATH=${DETAIL_LOGS_DIR}/char_rnn_training.log
NMT_LOG_PATH=${DETAIL_LOGS_DIR}/nmt_training.log

# CharRNN 학습 데이터 준비
echo "[INFO] Start crawling" >> ${G_LOG_PATH}
${CRAWLER_DIR}/DaumCrawler.py --date ${CRAWL_DATE} -p 4 > ${CRAWLING_LOG_PATH}
echo "[INFO] Finished crawling" >> ${G_LOG_PATH}

echo "[INFO] Start filtering" >> ${G_LOG_PATH}
echo -e "${CRAWLED_DATA_DIR}/${CRAWL_DATE}" | ${FILTER_DIR}/make_data.sh
# 디테일한 log로 변경
echo "[INFO] Filtering ${CRAWLED_DATA_DIR}/${CRAWL_DATE}" > ${FILTERING}
echo "[INFO] Finished filtering" >> ${G_LOG_PATH}

echo "[INFO] Prepare training for CharRNN model" >> ${G_LOG_PATH}
mkdir -p ${CHAR_RNN_DIR}/data/news
cp ${FILTER_DIR}/output/char_rnn_data.txt ${CHAR_RNN_DIR}/data/news/input.txt
echo "[INFO] Copied filtered data to CharRNN directory" > ${CHAR_RNN_LOG_PATH}

# 백업이 4개 이상이면 기존 것 제거
if [ $(ls ${CHAR_RNN_DIR}/save/news.bak* | wc -l) -gt 4 ]; then
    rm $(ls ${CHAR_RNN_DIR}/save/news.bak* | head -1)
    echo "[INFO] Removed old backup" >> ${CHAR_RNN_LOG_PATH}
fi

# CharRNN 기존 모델 백업
tar -czf "${CHAR_RNN_DIR}/save/news.bak-${TODAY}.tgz" -C ${CHAR_RNN_DIR}/save news/
echo "[INFO] Backup previous model" >> ${CHAR_RNN_LOG_PATH}

echo "[INFO] Start training CharRNN model" >> ${G_LOG_PATH}
cd ${CHAR_RNN_DIR} && ${CHAR_RNN_DIR}/train.sh --init_from ${CHAR_RNN_DIR}/save/news >> ${CHAR_RNN_LOG_PATH}
echo "[INFO] Finished training CharRNN model" >> ${G_LOG_PATH}

# NMT 학습 데이터 준비
echo "[INFO] Prepare training for NMT model" >> ${G_LOG_PATH}
echo "[INFO] Start additional filtering for NMT training data" > ${NMT_LOG_PATH}
NMT_ADDTIONAL_DATE=$(date '+%Y%m%d' -d "2 day ago")
echo -e "${CRAWLED_DATA_DIR}/${CRAWL_DATE}\n${CRAWLED_DATA_DIR}/${NMT_ADDTIONAL_DATE}" | ${FILTER_DIR}/make_data.sh 7000
echo "[INFO] Finish filtering ${CRAWLED_DATA_DIR}/${CRAWL_DATE}, ${CRAWLED_DATA_DIR}/${NMT_ADDTIONAL_DATE}" >> ${NMT_LOG_PATH}
cp -f ${FILTER_DIR}/output/*.title ${FILTER_DIR}/output/*.comment -t ${NMT_DIR}/train
echo "[INFO] Copied filtered data to NMT directory" >> ${NMT_LOG_PATH}

docker run --rm -v ${NMT_DIR}:/nmt tensorflow/tensorflow:nightly-devel-py3 bash -c \
    "rm -r /nmt/save/model/*"
echo "[INFO] Removed previous model" >> ${NMT_LOG_PATH}
echo "[INFO] Start training NMT model" >> ${G_LOG_PATH}
${NMT_DIR}/train.sh >> ${NMT_LOG_PATH}
echo "[INFO] Finished training NMT model" >> ${G_LOG_PATH}
