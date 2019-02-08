#!/bin/bash

function exit_if_err() {
    ERR_CODE=$?
    if [ ${ERR_CODE} -ne 0 ]
    then
        echo "[ERROR] Error has occurred in $@" 1>&2
        exit ${ERR_CODE}
    fi
}

TODAY="$(date '+%Y-%m-%d')"

# get a daum main news's title and url
echo "[GET A DAUM MAIN NEWS'S TITLE AND URL $(date +"%T")]"
ARTICLE_URLS=$(./GetDaumMainNews.py)
exit_if_err "get daum news urls $(date +"%T")"
NUM_URLS=$(echo "$ARTICLE_URLS" | wc -l)
INDEX=$(shuf -i 1-$NUM_URLS -n 1)
NEWS_URL=$(echo "$ARTICLE_URLS" | awk "NR == $INDEX")
NEWS_TITLE=$(./get_daum_news_title.py "$NEWS_URL")
exit_if_err "get a daum news $(date +"%T")"
echo "selected news $(date +"%T") : ${NEWS_TITLE}"


# generate comment of charRnn model
echo ""
echo "[GENERATE COMMENT OF CHAR RNN MODEL $(date +"%T")]"
CHAR_RNN_OUTPUT="$(echo "$(./generate_charRNN_comment.sh "${NEWS_TITLE}")")"
exit_if_err "generate char rnn comment $(date +"%T")"
echo "${CHAR_RNN_OUTPUT}"

# generate commnet of nmt model
echo ""
echo "[GENERATE COMMENT OF NMT MODEL $(date +"%T")]"
NMT_OUTPUT="$(echo "$(./generate_nmt_comment.sh "${NEWS_TITLE}" | tail -1)")"
exit_if_err "generate nmt comment $(date +"%T")"
echo "${NMT_OUTPUT}"

# tweet generated comments
echo ""
echo "[UPLOAD TWEET $(date +"%T")]"
TWEET_TEXT="$(echo -e "${NEWS_TITLE}\n${NEWS_URL}\n${CHAR_RNN_OUTPUT}\n\n${NMT_OUTPUT}")"
./upload_tweet.sh "${TWEET_TEXT}"
exit_if_err "upload tweet $(date +"%T")"

echo ""
echo "[TWEET TEXT]"
echo "${TWEET_TEXT}"
