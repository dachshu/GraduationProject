#!/bin/bash

function exit_if_err() {
    ERR_CODE=$?
    if [ ${ERR_CODE} -ne 0 ]
    then
        echo "[$(date +"%T")][ERROR] Error has occurred in $@" 1>&2
        exit ${ERR_CODE}
    fi
}

TODAY="$(date '+%Y-%m-%d')"
###################################################################
TRANS_MODEL_DIR="../results/saved_transformer_model"
TRANS_VOCAB_FILE="../results/saved_transformer_model/vocab"
###################################################################


# get a daum main news's title and url
echo "[$(date +"%T")][GET A DAUM MAIN NEWS'S TITLE AND URL]"
ARTICLE_URLS=$(./GetDaumMainNews.py)
exit_if_err "get daum news urls"
NUM_URLS=$(echo "$ARTICLE_URLS" | wc -l)
INDEX=$(shuf -i 1-$NUM_URLS -n 1)
NEWS_URL=$(echo "$ARTICLE_URLS" | awk "NR == $INDEX")
NEWS_TITLE=$(./get_daum_news_title.py "$NEWS_URL")
exit_if_err "get a daum news $(date +"%T")"
echo "selected news $(date +"%T") : ${NEWS_TITLE}"


# generate comment of charRnn model
#char_rnn_output=""
#echo ""
#echo "[generate comment of char rnn model $(date +"%t")]"
#char_rnn_output="$(./generate_charrnn_comment.sh "${news_title})"
#exit_if_err "generate char rnn comment $(date +"%t")"
#echo "${char_rnn_output}"

# generate commnet of nmt model
NMT_OUTPUT=""
echo ""
echo "[$(date +"%T")][GENERATE COMMENT OF NMT MODEL]"
NMT_OUTPUT="$(./generate_nmt_comment.sh "${NEWS_TITLE}")"
exit_if_err "generate nmt comment"
NMT_OUTPUT="$(echo "${NMT_OUTPUT}" |  tail -1)"
echo "${NMT_OUTPUT}"

# generate comment of transformer model
TRANSFORMER_OUTPUT=""
echo ""
echo "[$(date +"%T")][GENERATE COMMENT OF TRANSFORMER MODEL]"
TRANSFORMER_OUTPUT="$(./generate_transformer_comment.sh ${TRANS_MODEL_DIR} ${TRANS_VOCAB_FILE} "${NEWS_TITLE}")"
exit_if_err "generate transformer comment"
echo "${TRANSFORMER_OUTPUT}"

# tweet generated comments
echo ""
echo "[$(date +"%T")][UPLOAD TWEET]"
NEWS_NMT_TEXT="$(echo -e "${NEWS_TITLE}\n${NEWS_URL}\n\n${NMT_OUTPUT}")"
./upload_tweet.sh "${NEWS_NMT_TEXT}"
exit_if_err "upload tweet"
./upload_tweet.sh "${TRANSFORMER_OUTPUT}"
exit_if_err "upload tweet"

echo ""
echo "[TWEET TEXT]"
echo -e "${NEWS_TITLE}\n${NEWS_URL}\n\n${NMT_OUTPUT}\n\n${TRANSFORMER_OUTPUT}"
