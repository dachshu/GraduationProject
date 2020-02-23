#!/bin/bash

TODAY="$(date '+%Y-%m-%d')"
TIME="$(date +%T)"

PROJECT_DIR=$(cd $(dirname $0)/.. && pwd)
SCRIPT_DIR="${PROJECT_DIR}/bin"
RESULT_DIR="${PROJECT_DIR}/results/naver/${TODAY}"

LOG_DIR=${PROJECT_DIR}/logs/naver/${TODAY}
DETAIL_LOG_DIR=${LOG_DIR}/detail/upload_comment_tweet
DETAIL_LOG_PATH="${DETAIL_LOG_DIR}/${TIME}.log"

mkdir -p ${DETAIL_LOG_DIR}
touch "${DETAIL_LOG_PATH}"

cd "${PROJECT_DIR}/bin"
./generate_comment_tweet_naver.sh > ${DETAIL_LOG_PATH} 2>&1

# get recommended users and check they are similar to me
echo "[$(date +"%T")][INFO] Start crawling tweets of recommended users" >> ${DETAIL_LOG_PATH}
${SCRIPT_DIR}/make_mrpc_with_tweets_naver.sh >> ${DETAIL_LOG_PATH}
echo "[$(date +"%T")][INFO] End crawling tweets" >> ${DETAIL_LOG_PATH}

echo "[$(date +"%T")][INFO] Start inference tendencies of users" >> ${DETAIL_LOG_PATH}
BERT_DIR="${PROJECT_DIR}/bert"
EVAL_DATA_DIR="${RESULT_DIR}/bert_tweet/eval_data"
USER_NAMES=$(ls "${EVAL_DATA_DIR}")
for user in ${USER_NAMES}
do
    ${BERT_DIR}/infer_classifier.sh "${EVAL_DATA_DIR}/${user}"
    INFER_RESULT=$(${SCRIPT_DIR}/score_bert_eval_output.py "${EVAL_DATA_DIR}/${user}/classification_infer_output/test_results.tsv")
    echo "[$(date +"%T")][INFO] User '${user}' is ${INFER_RESULT}% similar to me" >> ${DETAIL_LOG_PATH}
    if ((${INFER_RESULT} > 1));then
        ${PROJECT_DIR}/TwitterController/TwitterController.py follow --key_file ${PROJECT_DIR}/TwitterController/twitter_key_naver --user_name "${user}"
    fi
done

${PROJECT_DIR}/bin/retweet_naver.sh
