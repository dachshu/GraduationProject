#!/bin/bash

echoerr() { echo "$@" 1>&2; exit; }

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

echo "[INFO] Start filtering" >> ${G_LOG_PATH}
if [ ! -d "${CRAWLED_DATA_DIR}/${CRAWL_DATE}" ]; then
    echoerr "Crawled data does not exist."
fi
echo -e "${CRAWLED_DATA_DIR}/${CRAWL_DATE}" | ${FILTER_DIR}/make_data.sh
echo "[INFO] Filtered ${CRAWLED_DATA_DIR}/${CRAWL_DATE}" > ${FILTERING_LOG_PATH}

echo "[INFO] Prepare training for CharRNN model" >> ${G_LOG_PATH}
mkdir -p ${CHAR_RNN_DIR}/data/news
cp ${FILTER_DIR}/output/char_rnn_data.txt ${CHAR_RNN_DIR}/data/news/input.txt
echo "[INFO] Copied filtered data to CharRNN directory" > ${CHAR_RNN_LOG_PATH}

# 백업이 4개 이상이면 기존 것 제거
BACKUP_NUM=$(ls ${CHAR_RNN_DIR}/save/news.bak* | wc -l)
if [ ${BACKUP_NUM} -gt 4 ]; then
    NUM_TO_DELETE=$(echo "${BACKUP_NUM}-4" | bc)
    rm $(ls ${CHAR_RNN_DIR}/save/news.bak* | head -${NUM_TO_DELETE})
    echo "[INFO] Removed old backup" >> ${CHAR_RNN_LOG_PATH}
fi

# CharRNN 기존 모델 백업
if [ -d "${CHAR_RNN_DIR}/save/news" ]; then
    tar -czf "${CHAR_RNN_DIR}/save/news.bak-${TODAY}.tgz" -C ${CHAR_RNN_DIR}/save news/
    echo "[INFO] Done backup previous model" >> ${CHAR_RNN_LOG_PATH}
fi

echo "[INFO] Start training CharRNN model" >> ${G_LOG_PATH}
CHAR_RNN_MODEL_DIR=${CHAR_RNN_DIR}/save/news
if [ -d "${CHAR_RNN_MODEL_DIR}" ]; then
    CHAR_RNN_OPTION="--init_from ${CHAR_RNN_MODEL_DIR}"
fi
cd ${CHAR_RNN_DIR} && ${CHAR_RNN_DIR}/train.sh ${CHAR_RNN_OPTION} >> ${CHAR_RNN_LOG_PATH}

# NMT 학습 데이터 준비
echo "[INFO] Prepare training for NMT model" >> ${G_LOG_PATH}
echo "[INFO] Start additional filtering for NMT training data" > ${NMT_LOG_PATH}
NMT_ADDTIONAL_DATE=$(date '+%Y%m%d' -d "2 day ago")
if [ -d "${CRAWLED_DATA_DIR}/${NMT_ADDTIONAL_DATE}" ]; then
    INPUT="${CRAWLED_DATA_DIR}/${CRAWL_DATE}\n${CRAWLED_DATA_DIR}/${NMT_ADDTIONAL_DATE}"
else
    INPUT="${CRAWLED_DATA_DIR}/${CRAWL_DATE}"
fi
echo -e "${INPUT}" | ${FILTER_DIR}/make_data.sh 7000
mkdir -p "${NMT_DIR}/train"
cp -f ${FILTER_DIR}/output/*.title ${FILTER_DIR}/output/*.comment -t ${NMT_DIR}/train
echo "[INFO] Copied filtered data to NMT directory" >> ${NMT_LOG_PATH}

docker run --rm -v ${NMT_DIR}:/nmt tensorflow/tensorflow:nightly-devel-py3 bash -c \
    "rm -r /nmt/save/model/*"
echo "[INFO] Removed previous model" >> ${NMT_LOG_PATH}
echo "[INFO] Start training NMT model" >> ${G_LOG_PATH}
${NMT_DIR}/train.sh >> ${NMT_LOG_PATH}
