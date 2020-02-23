#!/usr/bin/python3

import os
from random import shuffle
import sys
import argparse

def add_arguments(parser):
    parser.add_argument("my_file", type=str, help="my file for making test data")
    parser.add_argument("target_file", type=str, help="target file for making test data")
    parser.add_argument("out_dir", type=str, help="a directory where test.tsv file will be saved")
    return parser

def format_to_mrpc(my_file, target_file, out_dir):
    print("Processing tweet files")
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    assert os.path.isfile(my_file), "my file not found at %s" % my_file
    assert os.path.isfile(target_file), "target file not found at %s" % target_file

    with open(my_file, encoding="utf8") as my_fh, \
         open(target_file, encoding="utf8") as target_fh, \
         open(os.path.join(out_dir, "test.tsv"), 'w', encoding="utf8") as test_fh:
        header = "index\t#1 ID\t#2 ID\t#1 String\t#2 String\n"
        test_fh.write(header)

        my_tweets = my_fh.readlines()
        target_tweets = target_fh.readlines()

        loop_cnt = len(my_tweets) * len(target_tweets)
        ids = []
        for i in range(loop_cnt*2):
            ids.append(i)
        shuffle(ids)

        id_cnt = 0
        for my_tweet in my_tweets:
            for target_tweet in target_tweets:
                test_fh.write("%d\t%s\t%s\t%s\t%s\n" % ((id_cnt//2) + 1, ids[id_cnt], ids[id_cnt+1], \
                my_tweet.replace('\n', ' ').replace('\t', ' '), target_tweet.replace('\n', ' ').replace('\t', ' ')))
                id_cnt = id_cnt + 2

    print("\tCompleted!")



if __name__ == "__main__":
    parser = add_arguments(argparse.ArgumentParser())
    args = parser.parse_args()
    if not os.path.isdir(args.out_dir):
        os.makedirs(args.out_dir, exist_ok=True)
    format_to_mrpc(args.my_file, args.target_file, args.out_dir)
