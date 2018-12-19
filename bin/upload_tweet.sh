#!/bin/bash

TWEET_TEXT=$1
if [ -z "${TWEET_TEXT}" ]; then
    TWEET_TEXT=$(cat)
fi
TWEET_UPLOADER_DIR="../TweetUploader"
PARTIAL_PRINTER_DIR="../partial_print"

echo -e "${TWEET_TEXT}" | ${PARTIAL_PRINTER_DIR}/partial_print.py -140 | ${TWEET_UPLOADER_DIR}/TweetUploader.py -k ${TWEET_UPLOADER_DIR}/twitter_key
