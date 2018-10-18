#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0) && pwd)
CHAR_RNN_DIR=${SCRIPT_DIR}/kor-char-rnn-tensorflow
NMT_DIR=${SCRIPT_DIR}/nmt
TWEET_UPLOADER_DIR=${SCRIPT_DIR}/TweetUploader
PARTIAL_PRINTER_DIR=${SCRIPT_DIR}/partial_print
TODAY=$(date '+%Y-%m-%d')

LOG_DIR=${SCRIPT_DIR}/log/${TODAY}
# General log file path.
G_LOG_PATH=${LOG_DIR}/general.log
touch ${G_LOG_PATH}

DETAIL_LOGS_DIR=${LOG_DIR}/detail
mkdir -p ${DETAIL_LOGS_DIR}
DAUM_NEWS_LOG_PATH=${DETAIL_LOGS_DIR}/daum_news.log
CHAR_RNN_LOG_PATH=${DETAIL_LOGS_DIR}/char_rnn.log
NMT_LOG_PATH=${DETAIL_LOGS_DIR}/nmt.log
TWEET_LOG_PATH=${DETAIL_LOGS_DIR}/tweet.log

# get a news article
echo "[INFO] Get Daum main news" >> ${G_LOG_PATH}
ARTICLE_TITLES_LINKS=$(${SCRIPT_DIR}/GetDaumMainNews.py)
echo "${ARTICLE_TITLES_LINKS}" > ${DAUM_NEWS_LOG_PATH}
INDEX=$(shuf -i 1-5 -n 1)
SELECTED_TITLE=$(echo "${ARTICLE_TITLES_LINKS}" | awk "NR == (${INDEX}*2-1)")
SELECTED_LINK=$(echo "${ARTICLE_TITLES_LINKS}" | awk "NR == ${INDEX}*2")
echo -e "${SELECTED_TITLE}\n${SELECTED_LINK}\n" > /tmp/generated_comments.txt
echo "Selected news : ${SELECTED_TITLE}(${SELECTED_LINK})" >> ${DAUM_NEWS_LOG_PATH}

# generate comments of the article via char-rnn and seq2seq model
echo "[INFO] Start generating CharRNN comment" >> ${G_LOG_PATH}
echo "Generate a comment from the title: ${SELECTED_TITLE}" > ${CHAR_RNN_LOG_PATH}
echo "${SELECTED_TITLE}" > ${CHAR_RNN_DIR}/input_for_generation.txt
python3 ${CHAR_RNN_DIR}/sample.py --save_dir ${CHAR_RNN_DIR}/save/news --prime "$(head -1 ${CHAR_RNN_DIR}/input_for_generation.txt)" \
    --output_file /tmp/char_rnn_infer_output.txt >> ${CHAR_RNN_LOG_PATH} && \
cat /tmp/char_rnn_infer_output.txt >> /tmp/generated_comments.txt && \
(echo "[INFO] Generated output: " >> ${CHAR_RNN_LOG_PATH} && \
cat /tmp/char_rnn_infer_output.txt >> ${CHAR_RNN_LOG_PATH})
echo "[INFO] Finished generating CharRNN comment" >> ${G_LOG_PATH}

echo "[INFO] Start generating NMT comment" >> ${G_LOG_PATH}
echo "Generate a comment from the title: ${SELECTED_TITLE}" > ${NMT_LOG_PATH}
echo "${SELECTED_TITLE}" > ${NMT_DIR}/input_for_generation.txt
${NMT_DIR}/infer.sh ${NMT_DIR}/save/model ${NMT_DIR}/input_for_generation.txt ${NMT_DIR}/infer_output.txt >> ${NMT_LOG_PATH} && \
cat ${NMT_DIR}/infer_output.txt >> /tmp/generated_comments.txt && \
(echo "[INFO] Generated output: " >> ${NMT_LOG_PATH} && \
cat ${NMT_DIR}/infer_output.txt >> ${NMT_LOG_PATH})
echo "[INFO] Finished generating NMT comment" >> ${G_LOG_PATH}

echo "[INFO] Tweet to Twitter" >> ${G_LOG_PATH}
TWEET_TEXT=$(cat /tmp/generated_comments.txt | ${PARTIAL_PRINTER_DIR}/partial_print.py -140)
echo "[INFO] Generated tweet message: ${TWEET_TEXT}" > ${TWEET_LOG_PATH}
echo "${TWEET_TEXT}" | ${TWEET_UPLOADER_DIR}/TweetUploader.py -k ${TWEET_UPLOADER_DIR}/twitter_key
