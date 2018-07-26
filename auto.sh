#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0) && pwd)
TODAY=$(date '+%Y-%m-%d')

${SCRIPT_DIR}/train.sh
mkdir -p ${SCRIPT_DIR}/log && ${SCRIPT_DIR}/generate.sh | tee ${SCRIPT_DIR}/log/generation-log-${TODAY}
