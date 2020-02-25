#!/bin/bash

echoerr() {
    echo -e "$@" 1>&2
}

function print_help() {
    echoerr "It limits vocabulary size for nmt training"
    echoerr "usage: $(basename "$0") INPUT_DIR"
    echoerr "   INPUT_DIR: in where a input files are for nmt"
    exit 1
}

while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help)
            print_help
            shift
            ;;
        *)
            echoerr "\"$1\" is an invalid argument."
            print_help
            shift
            ;;
    esac
done
