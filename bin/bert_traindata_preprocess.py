#!/usr/bin/python3

import os
from random import shuffle
import sys
import argparse
import random

def add_arguments(parser):
    parser.add_argument("tweet_file_1", type=str, help="a file for making training and dev data")
    parser.add_argument("tweet_file_2", type=str, help="another file for making training and dev data")
    parser.add_argument("out_dir", type=str, help="a directory where train.tsv, dev.tsv files will be saved")
    return parser

def get_random_tweets(list1, list2):
    if len(list1) == 0:
        if len(list2) < 2:
            return None
        else:
            return (1, [list2.pop(), list2.pop()])
    if len(list2) == 0:
        if len(list1) < 2:
            return None
        else: 
            return (1, [list1.pop(), list1.pop()])

    if len(list1) > 1 and len(list2) > 1:
        flag = int(random.uniform(0,4))
    else:
        flag = 0

    if flag < 2:
        retval = [list1.pop(), list2.pop()]
        shuffle(retval)
        return (0, retval)
    elif flag == 2:
        return (1, [list1.pop(), list1.pop()])
    else:
        return (1, [list2.pop(), list2.pop()])



def format_to_mrpc(tweets_file1, tweets_file2, out_dir):
    print("Processing tweet files")
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
        loop_cnt = len(tweets2) if len(tweets1) < len(tweets2) else len(tweets1)
        loop_cnt = loop_cnt*2
        ids = []
        for i in range(loop_cnt):
            ids.append(i)
        shuffle(ids)

        tweet_data = []
        while True:
            tweet_pair = get_random_tweets(tweets1, tweets2) # type: (label, [tw1, tw2])
            if tweet_pair is None:
                break

            tweet_data.append("%s\t%s\t%s\t%s\t%s\n" % (tweet_pair[0], ids.pop(), ids.pop(), tweet_pair[1][0].replace('\n', ' ').replace('\t', ' '), tweet_pair[1][1].replace('\n', ' ').replace('\t', ' ')))
        shuffle(tweet_data)

        num_train_data = int(len(tweet_data)*0.9)
        num_dev_data = len(tweet_data)-num_train_data
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
