#!/bin/bash

echoerr() {
    echo "$@" 1>&2
}

function print_help() {
    echoerr "usage: train_char_rnn.sh INPUT_DIR OUTPUT_DIR [OLD_MODEL_DIR]"
    echoerr "   INPUT_DIR : a directory where input data is in"
    echoerr "   OUTPUT_DIR : a directory where a trained model will be saved in"
    echoerr "   OLD_MODEL_DIR : a directory where a previous trained model has been saved in"
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
OLD_MODEL_DIR=${POSITIONAL[2]}

mkdir -p "${OUTPUT_DIR}"

if [ -d "${OLD_MODEL_DIR}" ]; then
    OPTION="--init_from ${OLD_MODEL_DIR}"
fi

PROJECT_DIR=$(cd $(dirname "$0")/.. && pwd)
CHAR_RNN_DIR="${PROJECT_DIR}/kor-char-rnn-tensorflow"
python3 "${CHAR_RNN_DIR}/train.py" --data_dir "${INPUT_DIR}" --save_dir "${OUTPUT_DIR}" --rnn_size 1024 --num_layers 3 --num_epochs 100 --batch_size 32 ${OPTION}
exit $?
