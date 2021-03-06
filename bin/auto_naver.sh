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
CRAWLED_DATA_DIR=${CRAWLER_DIR}/crawled_data/naver_news
CRAWL_DATE=$(date '+%Y%m%d' -d "yesterday")
TODAY=$(date '+%Y-%m-%d')
RESULT_DIR="${PROJECT_DIR}/results/naver/${TODAY}"
K_LOG_DIR="${PROJECT_DIR}/logs/naver/${TODAY}"
DETAIL_K_LOG_DIR="${PROJECT_DIR}/logs/naver/${TODAY}/detail"

GENERAL_LOG_PATH="${K_LOG_DIR}/general.log"

mkdir -p "${K_LOG_DIR}"
mkdir -p "${RESULT_DIR}"
mkdir -p "${DETAIL_K_LOG_DIR}"

function exit_if_err() {
    ERR_CODE=$?
    if [ ${ERR_CODE} -ne 0 ]; then
        echo "[$(date +"%T")][ERROR] Error has occurred in $@" | tee -a "${GENERAL_LOG_PATH}" 1>&2
        exit ${ERR_CODE}
    fi
}

function log_err() {
    ERR_CODE=$?
    if [ ${ERR_CODE} -ne 0 ]; then
        echo "[$(date +"%T")][ERROR] Error has occurred in $@" | tee -a "${GENERAL_LOG_PATH}" 1>&2
    fi
}

# exit_if_err 함수에 들어가는 문자열은 에러를 구분하는 용도로 사용되므로
# 문자열을 변경할 경우 showstat.py 스크립트도 변경된 문자열에 맞춰
# 수정해야 한다.

# 어제 뉴스 크롤링
echo "[$(date +"%T")][INFO] Crawling Naver news" >> ${GENERAL_LOG_PATH}
(("${CRAWLER_DIR}/NaverCrawler.py" "${CRAWLED_DATA_DIR}" "${CRAWL_DATE}" &> "${DETAIL_K_LOG_DIR}/crawling.log" && echo "[$(date +"%T")][INFO] Crawling has finished" >> ${GENERAL_LOG_PATH}); log_err "crawling") &

## NMT용 14일치 학습 데이터 준비
#echo "[$(date +"%T")][INFO] Filtering additional news" >> ${GENERAL_LOG_PATH}
#FILTERED_DATA=$(find ${CRAWLED_DATA_DIR}/* -type d | sort | head --lines=-1 | tail -30 | ${SCRIPT_DIR}/news_filter.py 2> "${DETAIL_K_LOG_DIR}/filtering_for_nmt.log")
#log_err "filtering for NMT"

## NMT 입력 데이터 생성
#echo "[$(date +"%T")][INFO] making input for the NMT model" >> ${GENERAL_LOG_PATH}
#echo "${FILTERED_DATA}" | ${SCRIPT_DIR}/make_input_for_nmt.py "${RESULT_DIR}/nmt_training_input"

## NMT 학습
#echo "[$(date +"%T")][INFO] Training the NMT model" >> ${GENERAL_LOG_PATH}
## NMT가 학습과정을 stdout으로 출력하기 때문에 stdout과 stderr를 모두 log로 출력한다.
#${SCRIPT_DIR}/train_nmt.sh "${RESULT_DIR}/nmt_training_input" "${NMT_MODEL_DIR}" --gpu_id 1 &> "${DETAIL_K_LOG_DIR}/training_nmt.log" &
#NMT_TRAINING_PID=$!

# Transformer 데이터 준비
echo "[$(date +"%T")][INFO] making input for the Transformer model" >> ${GENERAL_LOG_PATH}
find ${CRAWLED_DATA_DIR}/* -type d | sort | head --lines=-1 | tail -160 | ${SCRIPT_DIR}/naver_news_filter.py | ${SCRIPT_DIR}/make_input_for_nmt.py "${RESULT_DIR}/transformer_training_input"

TRANSFORMER_MODEL_DATE_FILE="${RESULT_DIR}/../saved_transformer_model/model_created_date"
# Transformer 이전 모델 제거
if [ ! -s "${TRANSFORMER_MODEL_DATE_FILE}" ]; then
    echo "${TODAY}" > "${TRANSFORMER_MODEL_DATE_FILE}"
else
    CREATED_DATE_S=$(date --date="$(cat ${TRANSFORMER_MODEL_DATE_FILE}) + 1week" '+%s')
    TODAY_S=$(date --date="${TODAY}" '+%s')
    if [ ${CREATED_DATE_S} -le ${TODAY_S} ]; then
        rm -r "${RESULT_DIR}/../saved_transformer_model/*"
        echo "${TODAY}" > "${TRANSFORMER_MODEL_DATE_FILE}"
    fi
fi

# Transformer 학습
echo "[$(date +"%T")][INFO] Training the Transformer model" >> ${GENERAL_LOG_PATH}
${SCRIPT_DIR}/train_transformer.sh "${RESULT_DIR}/transformer_training_input" "${RESULT_DIR}/../saved_transformer_model" --epoch 5 2> "${DETAIL_K_LOG_DIR}/training_transformer.log" &
TRANSFORMER_TRAINING_PID=$!

#wait ${NMT_TRAINING_PID}
#log_err "NMT training"
wait ${TRANSFORMER_TRAINING_PID}
log_err "Transformer training"

echo "[$(date +"%T")][INFO] Generating schedules" >> ${GENERAL_LOG_PATH}
TIME_GENERATOR_DIR=${PROJECT_DIR}/CommentTimeGenerator
LATEST_TIME=$(([ -f "${TIME_GENERATOR_DIR}"/latest_generated_time ] && cat "${TIME_GENERATOR_DIR}"/latest_generated_time) || echo "0")
echo "latest time was: ${LATEST_TIME}" >> "${DETAIL_K_LOG_DIR}/generating_schedule.log"

GENERATED_TIMES=$("${TIME_GENERATOR_DIR}"/TimeModel.py sample --save_dir "${TIME_GENERATOR_DIR}/save" --seed "${LATEST_TIME}" 2> "${DETAIL_K_LOG_DIR}/generating_schedule.log")
exit_if_err "schedule generating"
echo -e "The generated schedules:\n${GENERATED_TIMES}" >> "${DETAIL_K_LOG_DIR}/generating_schedule.log"

for t in ${GENERATED_TIMES}; do
    HOUR=$(echo "${t}/3600" | bc)
    HOUR=$(printf "%02d" ${HOUR})
    MINUTE=$(echo "${t}%3600/60" | bc)
    MINUTE=$(printf "%02d" ${MINUTE})
    SECOND=$(echo "${t}%3600%60" | bc)
    SECOND=$(printf "%02d" ${SECOND})

    TARGET_TIME=$(date --date="${TODAY} ${HOUR}:${MINUTE}:${SECOND}" '+%s')
    CURRENT_TIME=$(date '+%s')

    if [ $(echo "${TARGET_TIME}<${CURRENT_TIME}" | bc) -eq 1 ]; then
        continue
    fi

    echo "target time: ${HOUR}:${MINUTE}:${SECOND}(raw time: ${t})" >> "${DETAIL_K_LOG_DIR}/generating_schedule.log"

    ${SCRIPT_DIR}/enq_generation_at_job_naver.sh "${HOUR}:${MINUTE}" &>> "${DETAIL_K_LOG_DIR}/enqueue_generation_job.log"

    if [ $? -eq 0 ]; then
        echo "[$(date +"%T")][INFO] A comment will be generated at ${HOUR}:${MINUTE}" >> ${GENERAL_LOG_PATH}
    else
        echo "[$(date +"%T")][Error] Enqueueing generation job failed" >> ${GENERAL_LOG_PATH}
    fi
done

[ ! -z "${GENERATED_TIMES}" ] && (echo "${GENERATED_TIMES}" | tail -1 > "${TIME_GENERATOR_DIR}"/latest_generated_time)

echo "[$(date +"%T")][INFO] Finished training steps" >> ${GENERAL_LOG_PATH}
