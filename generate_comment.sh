#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0) && pwd)
CHAR_RNN_DIR=${SCRIPT_DIR}/kor-char-rnn-tensorflow
NMT_DIR=${SCRIPT_DIR}/nmt
TWEET_UPLOADER_DIR=${SCRIPT_DIR}/TweetUploader
PARTIAL_PRINTER_DIR=${SCRIPT_DIR}/partial_print

# get a news article
ARTICLE_TITLES_LINKS=$(${SCRIPT_DIR}/GetDaumMainNews.py)
INDEX=$(shuf -i 1-5 -n 1)
SELECTED_TITLE=$(echo "${ARTICLE_TITLES_LINKS}" | awk "NR == (${INDEX}*2-1)")
SELECTED_LINK=$(echo "${ARTICLE_TITLES_LINKS}" | awk "NR == ${INDEX}*2")
echo -e "${SELECTED_TITLE}\n${SELECTED_LINK}\n" > /tmp/generated_comments.txt

# generate comments of the article via char-rnn and seq2seq model
echo "Generate a comment from the title: ${SELECTED_TITLE}"
echo "${SELECTED_TITLE}" > ${CHAR_RNN_DIR}/input_for_generation.txt
python3 ${CHAR_RNN_DIR}/sample.py --save_dir ${CHAR_RNN_DIR}/save/news --prime "$(head -1 ${CHAR_RNN_DIR}/input_for_generation.txt)" \
    --output_file /tmp/char_rnn_infer_output.txt && \
cat /tmp/char_rnn_infer_output.txt >> /tmp/generated_comments.txt

echo "${SELECTED_TITLE}" > ${NMT_DIR}/input_for_generation.txt
${NMT_DIR}/infer.sh ${NMT_DIR}/save/model ${NMT_DIR}/input_for_generation.txt ${NMT_DIR}/infer_output.txt && \
cat ${NMT_DIR}/infer_output.txt >> /tmp/generated_comments.txt

cat /tmp/generated_comments.txt | ${PARTIAL_PRINTER_DIR}/partial_print.py -140 | ${TWEET_UPLOADER_DIR}/TweetUploader.py -k ${TWEET_UPLOADER_DIR}/twitter_key
