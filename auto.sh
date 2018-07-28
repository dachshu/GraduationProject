#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0) && pwd)
TODAY=$(date '+%Y-%m-%d')

mkdir -p ${SCRIPT_DIR}/log/${TODAY}
${SCRIPT_DIR}/train.sh 2>&1 | tee ${SCRIPT_DIR}/log/${TODAY}/train-log
${SCRIPT_DIR}/generate.sh 2>&1 | tee ${SCRIPT_DIR}/log/${TODAY}/generation-log
