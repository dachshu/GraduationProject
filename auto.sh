#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0) && pwd)
TODAY=$(date '+%Y-%m-%d')

mkdir -p ${SCRIPT_DIR}/log/${TODAY}
${SCRIPT_DIR}/train.sh
${SCRIPT_DIR}/generate.sh
