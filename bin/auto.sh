#!/bin/bash

PROJECT_DIR=$(cd $(dirname $0)/.. && pwd)
SCRIPT_DIR="${PROJECT_DIR}/bin"
CRAWLER_DIR=${PROJECT_DIR}/crawler
CRAWLED_DATA_DIR=${CRAWLER_DIR}/crawled_data/daum_news
CHAR_RNN_DIR=${PROJECT_DIR}/kor-char-rnn-tensorflow
CHAR_RNN_MODEL_DIR=${CHAR_RNN_DIR}/save/news
NMT_DIR=${PROJECT_DIR}/nmt
NMT_MODEL_DIR=${NMT_DIR}/save/model
CRAWL_DATE=$(date '+%Y%m%d' -d "yesterday")
TODAY=$(date '+%Y-%m-%d')
RESULT_DIR="${PROJECT_DIR}/results/${TODAY}"
LOG_DIR="${PROJECT_DIR}/logs/${TODAY}"

GENERAL_LOG_PATH="${LOG_DIR}/general.log"

mkdir -p "${LOG_DIR}"
mkdir -p "${RESULT_DIR}"

# 어제 뉴스 크롤링
echo "[INFO] Crawling Daum news" >> ${GENERAL_LOG_PATH}
CRAWLED_PATH=$(${CRAWLER_DIR}/DaumCrawler.py "${CRAWL_DATE}" "${CRAWLED_DATA_DIR}" -p 4)

# 뉴스 필터링
echo "[INFO] Filtering Daum news" >> ${GENERAL_LOG_PATH}
FILTERED_DATA=$(echo "${CRAWLED_PATH}" | ${SCRIPT_DIR}/news_filter.py)

# CharRNN 입력 데이터 생성
echo "[INFO] making input for the Char-RNN model" >> ${GENERAL_LOG_PATH}
mkdir -p "${RESULT_DIR}/char_rnn_training_input"
echo "${FILTERED_DATA}" | ${SCRIPT_DIR}/make_input_for_char_rnn.py > "${RESULT_DIR}/char_rnn_training_input/input.txt"

# CharRNN 학습
if [ -d "${CHAR_RNN_MODEL_DIR}" ]; then
    echo "[INFO] Training the Char-RNN model from a previous model" >> ${GENERAL_LOG_PATH}
    CHAR_RNN_OPTION="${CHAR_RNN_MODEL_DIR}"
else
    echo "[INFO] Training the Char-RNN model" >> ${GENERAL_LOG_PATH}
fi
${SCRIPT_DIR}/train_char_rnn.sh "${RESULT_DIR}/char_rnn_training_input" "${CHAR_RNN_MODEL_DIR}" ${CHAR_RNN_OPTION}

# NMT용 2일치 학습 데이터 준비
NMT_ADDTIONAL_DATE=$(date '+%Y%m%d' -d "2 day ago")
if [ ! -d "${CRAWLED_DATA_DIR}/${NMT_ADDTIONAL_DATE}" ]; then
    echo "[INFO] Crawling additional news" >> ${GENERAL_LOG_PATH}
    NEWLY_CRAWLED_PATH="$(${CRAWLER_DIR}/DaumCrawler.py ${NMT_ADDTIONAL_DATE} ${CRAWLED_DATA_DIR} -p 4)"
    CRAWLED_PATH="${CRAWLED_PATH}\n${NEWLY_CRAWLED_PATH}"
fi
echo "[INFO] Filtering additional news" >> ${GENERAL_LOG_PATH}
FILTERED_DATA=$(echo -e "${CRAWLED_PATH}" | ${SCRIPT_DIR}/news_filter.py)

# NMT 입력 데이터 생성
echo "[INFO] making input for the NMT model" >> ${GENERAL_LOG_PATH}
echo "${FILTERED_DATA}" | ${SCRIPT_DIR}/make_input_for_nmt.py "${RESULT_DIR}/nmt_training_input"

# NMT 학습
echo "[INFO] Training the NMT model" >> ${GENERAL_LOG_PATH}
${SCRIPT_DIR}/train_nmt.sh "${RESULT_DIR}/nmt_training_input" "${NMT_MODEL_DIR}"

TIME_GENERATOR_DIR=${PROJECT_DIR}/CommentTimeGenerator
LATEST_TIME=$(([ -f "${TIME_GENERATOR_DIR}"/latest_generated_time ] && cat "${TIME_GENERATOR_DIR}"/latest_generated_time) || echo "0")

echo "[INFO] Generating schedules" >> ${GENERAL_LOG_PATH}
GENERATED_TIMES=$("${TIME_GENERATOR_DIR}"/TimeModel.py sample "${LATEST_TIME}")

for t in ${GENERATED_TIMES}; do
    HOUR=$(echo "${t}/3600" | bc)
    MINUTE=$(echo "${t}%3600/60" | bc)
    SECOND=$(echo "${t}%3600%60" | bc)

    TARGET_TIME=$(date --date="${TODAY} ${HOUR}:${MINUTE}:${SECOND}" '+%s')
    CURRENT_TIME=$(date '+%s')

    if [ $(echo "${TARGET_TIME}<${CURRENT_TIME}" | bc) -eq 1 ]; then
        continue
    fi

    ${SCRIPT_DIR}/enq_generation_at_job.sh ${HOUR}:${MINUTE}
done

[ ! -z "${GENERATED_TIMES}" ] && (echo "${GENERATED_TIMES}" | tail -1 > "${TIME_GENERATOR_DIR}"/latest_generated_time)

echo "[INFO] Finished training steps" >> ${GENERAL_LOG_PATH}
