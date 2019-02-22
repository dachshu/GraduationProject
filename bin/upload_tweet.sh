#!/bin/bash

echoerr() {
    echo "$@" 1>&2
}

function print_help() {
    echoerr "usage: upload_tweet.sh [TEXT..]"
    echoerr "   TEXT : some text which will be posted on twitter."
    echoerr "       if no TEXT is provided, the script would read text from STDIN."
    exit 1
}

function exit_if_err() {
    ERR_CODE=$?
    if [ ${ERR_CODE} -ne 0 ]; then
        echo "[ERROR] Error has occurred in $@ $(date +"%T")" | tee -a "${GENERAL_LOG_PATH}" 1>&2
        exit ${ERR_CODE}
    fi
}

POSITIONAL=()

while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help)
            print_help
            shift
            ;;
        *)
            POSITIONAL+=("$1")
            shift
            ;;
    esac
done

if [ ${#POSITIONAL[@]} -lt 1 ]; then
    TWEET_TEXT=$(cat)
else
    TWEET_TEXT=${POSITIONAL[0]}
    for t in ${POSITIONAL[@]:1}; do
        TWEET_TEXT="${TWEET_TEXT} $t"
    done
fi

TWEET_UPLOADER_DIR="../TweetUploader"

echo -e "${TWEET_TEXT}" | ${TWEET_UPLOADER_DIR}/TweetUploader.py -k ${TWEET_UPLOADER_DIR}/twitter_key
exit_if_err "upload tweet"


