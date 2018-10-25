#!/bin/bash

TWEET_TEXT=$1
TWEET_UPLOADER_DIR="../TweetUploader"
PARTIAL_PRINTER_DIR="../partial_print"

echo "${TWEET_TEXT}" | ${PARTIAL_PRINTER_DIR}/partial_print.py -140 | ${TWEET_UPLOADER_DIR}/TweetUploader.py -k ${TWEET_UPLOADER_DIR}/twitter_key
