#!/bin/bash

echoerr() {
    echo "$@" 1>&2
}

function print_help() {
    echoerr "usage: train_nmt.sh INPUT_DIR OUTPUT_DIR"
    echoerr "   INPUT_DIR : a directory where input data is in"
    echoerr "   OUTPUT_DIR : a directory where trained model will be saved in"
    exit 1
}

POSITIONAL=()

while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help)
            print_help
            shift
            ;;
        -*|--*)
            echoerr "\"$1\" is an invalid argument."
            print_help
            shift
            ;;
        *)
            POSITIONAL+=("$1")
            shift
            ;;
    esac
done

if [ ${#POSITIONAL[@]} -lt 2 ]; then
    echoerr "this script requires 2 positional arguments."
    print_help
fi

INPUT_DIR=${POSITIONAL[0]}
OUTPUT_DIR=${POSITIONAL[1]}

mkdir -p "${OUTPUT_DIR}"

INPUT_DIR=$(cd ${INPUT_DIR} && pwd)
OUTPUT_DIR=$(cd ${OUTPUT_DIR} && pwd)

PROJECT_DIR=$(cd $(dirname "$0")/.. && pwd)
NMT_DIR=${PROJECT_DIR}/nmt
INNER_NMT_DIR=/nmt
INNER_OUTPUT_DIR=/nmt_output
INNER_INPUT_DIR=/nmt_input

nvidia-docker run --rm -v "${NMT_DIR}:${INNER_NMT_DIR}" -v "${OUT_DIR}:${INNER_OUTPUT_DIR}" -v "${INPUT_DIR}:${INNER_INPUT_DIR}" \
    tensorflow/tensorflow:nightly-devel-gpu-py3 \
    bash -c "export PYTHONIOENCODING=UTF-8 && cd /nmt && python3 -m nmt.nmt \
    --src=title --tgt=comment \
    --vocab_prefix=${INNER_INPUT_DIR}/vocab \
    --train_prefix=${INNER_INPUT_DIR}/train \
    --dev_prefix=${INNER_INPUT_DIR}/dev  \
    --test_prefix=${INNER_INPUT_DIR}/test \
    --out_dir=${INNER_OUTPUT_DIR} \
    --num_train_steps=12000 \
    --steps_per_stats=100 \
    --num_layers=2 \
    --num_units=128 \
    --dropout=0.5 \
    --share_vocab \
    --metrics=bleu"
