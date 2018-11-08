#!/bin/bash

TODAY="$(date '+%Y-%m-%d')"

# get a daum main news's title and url
echo "[GET A DAUM MAIN NEWS'S TITLE AND URL]"
NEWS_TITLE_N_URL=$(./get_daum_main_news.sh)
NEWS_TITLE=$(echo "${NEWS_TITLE_N_URL}" | head -1)
NEWS_URL=$(echo "${NEWS_TITLE_N_URL}" | tail -1)
echo "selected news : ${NEWS_TITLE}"

# tweet text file
echo ""
echo "[OUTPUT TWEET TEXT FILE]"
OUTPUT_FILE_NAME="$(echo "${NEWS_TITLE}" | awk '{printf "%s", $1}')_$(date +%T)_comment_tweet.txt"
#OUTPUT_FILE_NAME=$(echo "${NEWS_TITLE}" | md5sum | awk '{printf "%s_comment_tweet.txt", $1}')
OUTPUT_FILE_PATH=$(echo "../results/${TODAY}/${OUTPUT_FILE_NAME}")
echo ${OUTPUT_FILE_PATH}
echo -e "${NEWS_TITLE_N_URL}\n" > "${OUTPUT_FILE_PATH}"

# generate comment of charRnn model
echo ""
echo "[GENERATE COMMENT OF CHAR RNN MODEL]"
CHAR_RNN_OUTPUT_DIR=$(./generate_charRNN_comment.sh "${NEWS_TITLE}"| tail -1 | awk '{printf $4}')
echo ${CHAR_RNN_OUTPUT_DIR}
cat "${CHAR_RNN_OUTPUT_DIR}/output.txt" >> ${OUTPUT_FILE_PATH}

# generate commnet of nmt model
echo ""
echo "[GENERATE COMMENT OF NMT MODEL]"
NMT_OUTPUT_DIR=$(./generate_nmt_comment.sh "${NEWS_TITLE}" | tail -1 | awk '{printf $4}')
echo ${NMT_OUTPUT_DIR}
cat "${NMT_OUTPUT_DIR}/output.txt" >> "${OUTPUT_FILE_PATH}"

# tweet generated comments
echo ""
echo "[UPLOAD TWEET]"
TWEET_TEXT=$(cat ${OUTPUT_FILE_PATH})
./upload_tweet.sh "${TWEET_TEXT}"

echo ""
echo "[TWEET TEXT]"
echo "${TWEET_TEXT}"
