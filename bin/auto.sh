#!/bin/bash

echoerr() {
    echo -e "$@" 1>&2
}

function print_help() {
    echoerr "This script runs automatic training and register jobs to generate comments."
    echoerr "It receives no arguments."
    exit 1
}

while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help)
            print_help
            shift
            ;;
        *)
            echoerr "\"$1\" is an invalid argument."
            print_help
            shift
            ;;
    esac
done

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
K_LOG_DIR="${PROJECT_DIR}/logs/${TODAY}"
DETAIL_K_LOG_DIR="${PROJECT_DIR}/logs/${TODAY}/detail"

GENERAL_LOG_PATH="${K_LOG_DIR}/general.log"

mkdir -p "${K_LOG_DIR}"
mkdir -p "${RESULT_DIR}"
mkdir -p "${DETAIL_K_LOG_DIR}"

function exit_if_err() {
    ERR_CODE=$?
    if [ ${ERR_CODE} -ne 0 ]; then
        echo "[ERROR] Error has occurred in $@ $(date +"%T")" | tee -a "${GENERAL_LOG_PATH}" 1>&2
        exit ${ERR_CODE}
    fi
}

# exit_if_err 함수에 들어가는 문자열은 에러를 구분하는 용도로 사용되므로
# 문자열을 변경할 경우 showstat.py 스크립트도 변경된 문자열에 맞춰
# 수정해야 한다.

# 어제 뉴스 크롤링
echo "[INFO] Crawling Daum news $(date +"%T")" >> ${GENERAL_LOG_PATH}
CRAWLED_PATH=$(echo "${CRAWL_DATE}" | "${CRAWLER_DIR}/DaumCrawler.py" "${CRAWLED_DATA_DIR}" -p 4 2> "${DETAIL_K_LOG_DIR}/crawling.log")
exit_if_err "crawling"

# 뉴스 필터링
echo "[INFO] Filtering Daum news $(date +"%T")" >> ${GENERAL_LOG_PATH}
FILTERED_DATA=$(echo "${CRAWLED_PATH}" | ${SCRIPT_DIR}/news_filter.py 2> "${DETAIL_K_LOG_DIR}/filtering_for_char_rnn.log")
exit_if_err "filtering for CharRNN"

# CharRNN 입력 데이터 생성
echo "[INFO] making input for the Char-RNN model $(date +"%T")" >> ${GENERAL_LOG_PATH}
mkdir -p "${RESULT_DIR}/char_rnn_training_input"
echo "${FILTERED_DATA}" | ${SCRIPT_DIR}/make_input_for_char_rnn.py > "${RESULT_DIR}/char_rnn_training_input/input.txt" 2> "${DETAIL_K_LOG_DIR}/char_rnn_input_making.log"

# CharRNN 학습
if [ -d "${CHAR_RNN_MODEL_DIR}" ] && [ $(ls "${CHAR_RNN_MODEL_DIR}" | wc -l) -ne 0 ]; then
    echo "[INFO] Training the Char-RNN model from a previous model $(date +"%T")" >> ${GENERAL_LOG_PATH}
    CHAR_RNN_OPTION="${CHAR_RNN_MODEL_DIR}"
else
    echo "[INFO] Training the Char-RNN model $(date +"%T")" >> ${GENERAL_LOG_PATH}
fi
${SCRIPT_DIR}/train_char_rnn.sh "${RESULT_DIR}/char_rnn_training_input" "${CHAR_RNN_MODEL_DIR}" ${CHAR_RNN_OPTION} 2> "${DETAIL_K_LOG_DIR}/training_char_rnn.log"
exit_if_err "CharRNN training"

# NMT용 2일치 학습 데이터 준비
NMT_ADDITIONAL_DATE=$(date '+%Y%m%d' -d "2 day ago")
if [ ! -d "${CRAWLED_DATA_DIR}/${NMT_ADDITIONAL_DATE}" ]; then
    echo "[INFO] Crawling additional news $(date +"%T")" >> ${GENERAL_LOG_PATH}
    NEWLY_CRAWLED_PATH="$(echo "${NMT_ADDITIONAL_DATE}" | ${CRAWLER_DIR}/DaumCrawler.py ${CRAWLED_DATA_DIR} -p 4 2> "${DETAIL_K_LOG_DIR}/crawling_for_nmt.log")"
    exit_if_err "crawling for NMT"
    CRAWLED_PATH="${CRAWLED_PATH}\n${NEWLY_CRAWLED_PATH}"
else
    CRAWLED_PATH="${CRAWLED_PATH}\n${CRAWLED_DATA_DIR}/${NMT_ADDITIONAL_DATE}"
fi
echo "[INFO] Filtering additional news $(date +"%T")" >> ${GENERAL_LOG_PATH}
FILTERED_DATA=$(echo -e "${CRAWLED_PATH}" | ${SCRIPT_DIR}/news_filter.py 2> "${DETAIL_K_LOG_DIR}/filtering_for_nmt.log")
exit_if_err "filtering for NMT"

# NMT 입력 데이터 생성
echo "[INFO] making input for the NMT model $(date +"%T")" >> ${GENERAL_LOG_PATH}
echo "${FILTERED_DATA}" | ${SCRIPT_DIR}/make_input_for_nmt.py "${RESULT_DIR}/nmt_training_input" 2> "${DETAIL_K_LOG_DIR}/nmt_input_making.log"

# NMT 학습
echo "[INFO] Training the NMT model $(date +"%T")" >> ${GENERAL_LOG_PATH}
# NMT가 학습과정을 stdout으로 출력하기 때문에 stdout과 stderr를 모두 log로 출력한다.
${SCRIPT_DIR}/train_nmt.sh "${RESULT_DIR}/nmt_training_input" "${NMT_MODEL_DIR}" &> "${DETAIL_K_LOG_DIR}/training_nmt.log"
exit_if_err "NMT training"

# Transformer 데이터 준비
echo "[INFO] making input for the Transformer model $(date +"%T")" >> ${GENERAL_LOG_PATH}
ls -d ${CRAWLED_DATA_DIR}/* | tail -120 | ${SCRIPT_DIR}/news_filter.py | ${SCRIPT_DIR}/make_input_for_nmt.py "${RESULT_DIR}/transformer_training_input" 2> "${DETAIL_K_LOG_DIR}/transformer_input_making.log"

# Transformer 학습
echo "[INFO] Training the Transformer model $(date +"%T")" >> ${GENERAL_LOG_PATH}
${SCRIPT_DIR}/train_transformer.sh "${RESULT_DIR}/transformer_training_input" "${RESULT_DIR}/saved_transformer_model" --epoch 5 2> "${DETAIL_K_LOG_DIR}/training_transformer.log"

TIME_GENERATOR_DIR=${PROJECT_DIR}/CommentTimeGenerator
LATEST_TIME=$(([ -f "${TIME_GENERATOR_DIR}"/latest_generated_time ] && cat "${TIME_GENERATOR_DIR}"/latest_generated_time) || echo "0")

echo "[INFO] Generating schedules $(date +"%T")" >> ${GENERAL_LOG_PATH}
GENERATED_TIMES=$("${TIME_GENERATOR_DIR}"/TimeModel.py sample --save_dir "${TIME_GENERATOR_DIR}/save" --seed "${LATEST_TIME}" 2> "${DETAIL_K_LOG_DIR}/generating_schedule.log")
exit_if_err "schedule generating"
echo -e "The generated schedules:\n${GENERATED_TIMES}" >> "${DETAIL_K_LOG_DIR}/generating_schedule.log"

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

echo "[INFO] Finished training steps $(date +"%T")" >> ${GENERAL_LOG_PATH}
