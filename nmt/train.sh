#!/bin/bash

SOURCE_DIR=$(cd $(dirname "$0") && pwd)
VOLUME_DIR=/nmt
CURR_TIME=$(date "+%F-%H-%M-%S")

nvidia-docker run --rm -v ${SOURCE_DIR}:${VOLUME_DIR} tensorflow/tensorflow:nightly-devel-gpu-py3 bash -c "export PYTHONIOENCODING=UTF-8 && cd /nmt && python3 -m nmt.nmt \
    --src=title --tgt=comment \
    --vocab_prefix=/nmt/train/vocab \
    --train_prefix=/nmt/train/train \
    --dev_prefix=/nmt/train/dev  \
    --test_prefix=/nmt/train/test \
    --out_dir=/nmt/save/model \
    --num_train_steps=12000 \
    --steps_per_stats=100 \
    --num_layers=2 \
    --num_units=128 \
    --dropout=0.5 \
    --share_vocab \
    --metrics=bleu | tee /nmt/logs/train-${CURR_TIME}.log"

