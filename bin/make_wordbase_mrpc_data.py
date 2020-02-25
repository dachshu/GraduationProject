#!/usr/bin/python3

import os
from random import shuffle, randint
import sys
import argparse

def add_arguments(parser):
    parser.add_argument("my_file", type=str, help="my file for making test data")
    parser.add_argument("target_file", type=str, help="target file for making test data")
    parser.add_argument("out_dir", type=str, help="a directory where test.tsv file will be saved")
    return parser

def filter_tuple(tweet1, tweet2, n):
    list_to_filter1 = [word for word in tweet1 if len(word) > 1]
    list_to_filter2 = [word for word in tweet2 if len(word) > 1]
    if len(set(list_to_filter1) & set(list_to_filter2)) >= n :
        return True
    return False


def filter_tuples(tuples, n):
    ret = []
    for (label, tweet1, tweet2) in tuples:
        list_to_filter1 = [word for word in tweet1 if len(word) > 1]
        list_to_filter2 = [word for word in tweet2 if len(word) > 1]
        if len(set(list_to_filter1) & set(list_to_filter2)) >= n :
            # print([len(set(list_to_filter1) & set(list_to_filter2)), set(list_to_filter1) & set(list_to_filter2), ' '.join(tweet1), ' '.join(tweet2)])
            ret.append((label, tweet1, tweet2))
    return ret
    #return [(label, tweet1, tweet2) for (label, tweet1, tweet2) in tuples if len(set(tweet1) & set(tweet2)) >= n]

def format_to_mrpc(my_file, target_file, out_dir):
    print("Processing tweet files")
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    assert os.path.isfile(my_file), "my file not found at %s" % my_file
    assert os.path.isfile(target_file), "target file not found at %s" % target_file

    with open(my_file, encoding="utf8") as my_fh, \
         open(target_file, encoding="utf8") as target_fh, \
         open(os.path.join(out_dir, "train.tsv"), 'w', encoding="utf8") as train_fh, \
         open(os.path.join(out_dir, "dev.tsv"), 'w', encoding="utf8") as dev_fh:
        header = "Quality\t#1 ID\t#2 ID\t#1 String\t#2 String\n"
        train_fh.write(header)
        dev_fh.write(header)

        my_tweets = my_fh.readlines()
        my_tweets = [tweet.split() for tweet in my_tweets]
        target_tweets = target_fh.readlines()
        target_tweets = [tweet.split() for tweet in target_tweets]

        N = 7 
        mtweet_tuples = []
        ttweet_tuples = []
        mttweet_tuples = []
        for i in range(len(my_tweets)):
            for k in range(i + 1, len(my_tweets)):
                if filter_tuple(my_tweets[i], my_tweets[k], N):
                    mtweet_tuples.append((1, my_tweets[i], my_tweets[k]))

        for i in range(len(target_tweets)):
            for k in range(i + 1, len(target_tweets)):
                if filter_tuple(target_tweets[i], target_tweets[k], N):
                    ttweet_tuples.append((1, target_tweets[i], target_tweets[k]))

        for mtweet in my_tweets:
            for ttweet in target_tweets:
                if filter_tuple(mtweet, ttweet, N):
                    mttweet_tuples.append((0, mtweet, ttweet))

        #shuffle(filter_tuples(mtweet_tuples, N))
        #shuffle(filter_tuples(ttweet_tuples, N))
        #mttweet_tuples = filter_tuples(mttweet_tuples, N)
        shuffle(mtweet_tuples)
        shuffle(ttweet_tuples)
        #mttweet_tuples = filter_tuples(mttweet_tuples, N)
        pivot_cnt = len(mttweet_tuples)

        ttweet_tuples = ttweet_tuples[:(pivot_cnt//2)]
        mtweet_tuples = mtweet_tuples[:(pivot_cnt - pivot_cnt//2)]

        total_tuples = mtweet_tuples + ttweet_tuples + mttweet_tuples
        shuffle(total_tuples)

        loop_cnt = len(total_tuples)
        ids = []
        for i in range(loop_cnt*2):
            ids.append(i)
        shuffle(ids)

        i = 0
        for (label, tweet1, tweet2) in total_tuples[:int(loop_cnt*0.9)]:
            if randint(0,1) == 0:
                first_tweet = tweet1
                second_tweet = tweet2
            else:
                first_tweet = tweet2
                second_tweet = tweet1

            train_fh.write("%d\t%s\t%s\t%s\t%s\n" % (label, ids[2*i], ids[2*i+1], \
                ' '.join(first_tweet).replace('\n', ' ').replace('\t', ' '), ' '.join(second_tweet).replace('\n', ' ').replace('\t', ' ')))

            i = i+1

        i = 0
        for (label, tweet1, tweet2) in total_tuples[int(loop_cnt*0.9):]:
            if randint(0,1) == 0:
                first_tweet = tweet1
                second_tweet = tweet2
            else:
                first_tweet = tweet2
                second_tweet = tweet1

            dev_fh.write("%d\t%s\t%s\t%s\t%s\n" % (label, ids[2*i], ids[2*i+1], \
                ' '.join(first_tweet).replace('\n', ' ').replace('\t', ' '), ' '.join(second_tweet).replace('\n', ' ').replace('\t', ' ')))

            i = i+1

    print("\tCompleted!")



if __name__ == "__main__":
    parser = add_arguments(argparse.ArgumentParser())
    args = parser.parse_args()
    if not os.path.isdir(args.out_dir):
        os.makedirs(args.out_dir, exist_ok=True)
    format_to_mrpc(args.my_file, args.target_file, args.out_dir)
