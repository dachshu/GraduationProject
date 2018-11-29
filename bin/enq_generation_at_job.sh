#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0) && pwd)
GENERATION_TIME=$1
at -q d ${GENERATION_TIME} -f "${SCRIPT_DIR}/generate_comment_tweet_with_log.sh"

