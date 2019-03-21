#!/usr/bin/python3

import os
from random import shuffle
import sys
import argparse

def add_arguments(parser):
    parser.add_argument("tweet_file_1", type=str, help="a file for making training and dev data")
    parser.add_argument("tweet_file_2", type=str, help="another file for making training and dev data")
    parser.add_argument("out_dir", type=str, help="a directory where train.tsv, dev.tsv files will be saved")
    return parser

def format_to_mrpc(tweets_file1, tweets_file2, out_dir_path):
    print("Processing tweet files")
    out_dir = os.path.join(out_dir_path, "bert_train_data")
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    assert os.path.isfile(tweets_file1), "tweet file 1 not found at %s" % tweets_file1
    assert os.path.isfile(tweets_file2), "tweet file 2 not found at %s" % tweets_file2

    with open(tweets_file1, encoding="utf8") as tweet1_fh, \
         open(tweets_file2, encoding="utf8") as tweet2_fh, \
         open(os.path.join(out_dir, "train.tsv"), 'w', encoding="utf8") as train_fh, \
         open(os.path.join(out_dir, "dev.tsv"), 'w', encoding="utf8") as dev_fh:
        header = "Quality\t#1 ID\t#2 ID\t#1 String\t#2 String\n"
        train_fh.write(header)
        dev_fh.write(header)

        tweets1 = tweet1_fh.readlines()
        shuffle(tweets1)
        tweets2 = tweet2_fh.readlines()
        shuffle(tweets2)
        loop_cnt = len(tweets1) if len(tweets1) < len(tweets2) else len(tweets2)
        loop_cnt = int(loop_cnt / 4)
        ids = []
        for i in range(loop_cnt * 4 * 2):
            ids.append(i)
        shuffle(ids)

        tweet_data = []
        for i in range(loop_cnt * 4):
            tweet_data.append("%s\t%s\t%s\t%s\t%s\n" % (0, ids[i], ids[i + 1], tweets1[i].replace('\n', '').replace('\t', ''), tweets2[i].replace('\n', '').replace('\t', '')))
            tweet_data.append("%s\t%s\t%s\t%s\t%s\n" % (0, ids[i + 2], ids[i + 3], tweets2[i + 1].replace('\n', '').replace('\t', ''), tweets1[i + 1].replace('\n', '').replace('\t', '')))
            tweet_data.append("%s\t%s\t%s\t%s\t%s\n" % (1, ids[i + 4], ids[i + 5], tweets1[i + 2].replace('\n', '').replace('\t', ''), tweets1[i + 3].replace('\n', '').replace('\t', '')))
            tweet_data.append("%s\t%s\t%s\t%s\t%s\n" % (1, ids[i + 6], ids[i + 7], tweets2[i + 2].replace('\n', '').replace('\t', ''), tweets2[i + 3].replace('\n', '').replace('\t', '')))
        shuffle(tweet_data)

        num_train_data = int((loop_cnt*4)*(10/11))
        num_dev_data = loop_cnt*4 - num_train_data
        for i in range(num_train_data):
            train_fh.write(tweet_data[i])
        for i in range(num_dev_data):
            dev_fh.write(tweet_data[num_train_data + i])
    print("\tCompleted!")



if __name__ == "__main__":
    parser = add_arguments(argparse.ArgumentParser())
    args = parser.parse_args()
    if not os.path.isdir(args.out_dir):
        os.makedirs(args.out_dir, exist_ok=True)
    format_to_mrpc(args.tweet_file_1, args.tweet_file_2, args.out_dir)
