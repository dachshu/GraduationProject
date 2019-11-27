#!/usr/bin/python3

import argparse
import os
import sys

def add_arguments(parser):
    parser.add_argument("eval_file", nargs="?", default=sys.stdin, type=argparse.FileType(mode='r', encoding='utf-8'),
            help="a counter's bert evaluation output file")
    return parser

def score(f):
    lines = f.readlines()
    cnt = 0
    for line in lines:
        scores = line.split('\t')
        diff = float(scores[1]) - float(scores[0])
        if diff > 0.5:
            #print(scores[0], scores[1])
            cnt += 1
    #print(len(lines), cnt)
    print(int(float(cnt/len(lines)) * 100))
    f.close()

if __name__ == "__main__":
    parser = add_arguments(argparse.ArgumentParser())
    args = parser.parse_args()
    score(args.eval_file)
    
