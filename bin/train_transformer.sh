#!/bin/bash

echoerr() {
    echo "$@" 1>&2
}

function print_help() {
    echoerr "usage: train_nmt.sh INPUT_DIR OUTPUT_DIR [--epoch EPOCH]"
    echoerr "   INPUT_DIR : a directory where input data is in"
    echoerr "   OUTPUT_DIR : a directory where trained model will be saved in"
    echoerr "   --epoch : training epochs"
    exit 1
}

POSITIONAL=()
EPOCH=20

while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help)
            print_help
            shift
            ;;
        --epoch)
            shift
            EPOCH=$1
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
TRANS_DIR=${PROJECT_DIR}/models
INNER_TRANS_DIR=/models
INNER_OUTPUT_DIR=/trans_output
INNER_INPUT_DIR=/trans_input
INNER_DATA_DIR=/tmp/trans_data

docker run --runtime=nvidia --rm -u $(id -u):$(id -g) -v "${TRANS_DIR}:${INNER_TRANS_DIR}" -v "${OUTPUT_DIR}:${INNER_OUTPUT_DIR}" -v "${INPUT_DIR}:${INNER_INPUT_DIR}" \
    tensorflow_models \
    bash -c "export PYTHONIOENCODING=UTF-8 && export PYTHONPATH=${INNER_TRANS_DIR} && cd ${INNER_TRANS_DIR}/official/transformer \
    && python3 data_preprocess.py --input_dir ${INNER_INPUT_DIR} --data_dir ${INNER_DATA_DIR} \
    && python3 transformer_main.py --data_dir ${INNER_DATA_DIR} --model_dir ${INNER_OUTPUT_DIR} \
        --vocab_file ${INNER_DATA_DIR}/vocab \
        --param_set base \
        --train_epochs ${EPOCH} \
    && mv ${INNER_DATA_DIR}/vocab -t ${INNER_OUTPUT_DIR}"

exit $?

