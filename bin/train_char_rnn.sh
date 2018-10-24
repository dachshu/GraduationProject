#!/bin/bash

INPUT_DIR=$1
OUTPUT_DIR=$2
OLD_MODEL_DIR=$3

if [ ! -d "${INPUT_DIR}" ]; then
    >2& echo "argument 1(INPUT_DIR) doesn't exist"; exit 1
fi
mkdir -p "${OUTPUT_DIR}"

if [ -d "${OLD_MODEL_DIR}" ]; then
    OPTION="--init_from ${OLD_MODEL_DIR}"
fi

python3 train.py --data_dir "${INPUT_DIR}" --save_dir "${OUTPUT_DIR}" --rnn_size 1024 --num_layers 3 --num_epochs 100 --batch_size 32 "${OPTION}"
