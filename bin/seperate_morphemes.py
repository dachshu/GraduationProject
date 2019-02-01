#!/usr/bin/python3

from konlpy.tag import Mecab
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="*", default=sys.stdin, type=argparse.FileType('r', encoding='utf-8'))
    args = parser.parse_args()

    mecab = Mecab()

    files = args.file if type(args.file) is list else [args.file]
    for f in files:
        for line in f.readlines():
            print(' '.join(mecab.morphs(line.strip())))
