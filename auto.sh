#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0) && pwd)

${SCRIPT_DIR}/train.sh
${SCRIPT_DIR}/generate.sh
