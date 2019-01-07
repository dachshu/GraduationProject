#!/bin/bash

TODAY="$(date '+%Y-%m-%d')"

# get a daum main news's title and url
echo "[GET A DAUM MAIN NEWS'S TITLE AND URL]"
ARTICLE_URLS=$(./GetDaumMainNews.py)
NUM_URLS=$(echo "$ARTICLE_URLS" | wc -l)
INDEX=$(shuf -i 1-$NUM_URLS -n 1)
NEWS_URL=$(echo "$ARTICLE_URLS" | awk "NR == $INDEX")
NEWS_TITLE=$(./get_daum_news_title.py "$NEWS_URL")
echo "selected news : ${NEWS_TITLE}"

# generate comment of charRnn model
echo ""
echo "[GENERATE COMMENT OF CHAR RNN MODEL]"
CHAR_RNN_OUTPUT="$(echo "$(./generate_charRNN_comment.sh "${NEWS_TITLE}")")"
echo "${CHAR_RNN_OUTPUT}"

# generate commnet of nmt model
echo ""
echo "[GENERATE COMMENT OF NMT MODEL]"
NMT_OUTPUT="$(echo "$(./generate_nmt_comment.sh "${NEWS_TITLE}" | tail -1)")"
echo "${NMT_OUTPUT}"

# tweet generated comments
echo ""
echo "[UPLOAD TWEET]"
TWEET_TEXT="$(echo -e "${NEWS_TITLE}\n${NEWS_URL}\n${CHAR_RNN_OUTPUT}\n\n${NMT_OUTPUT}")"
./upload_tweet.sh "${TWEET_TEXT}"

echo ""
echo "[TWEET TEXT]"
echo "${TWEET_TEXT}"
