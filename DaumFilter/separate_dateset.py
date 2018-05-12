#!/usr/bin/python3

import argparse
import random
import shutil
import os

def add_arguments(parser):
    parser.add_argument("title", type=argparse.FileType('r', encoding='utf-8'), help="text file which has titles")
    parser.add_argument("comment", type=argparse.FileType('r', encoding='utf-8'), help="text file which has comments")
    parser.add_argument("vocab", nargs='?', help="text file which has vocabraries")
    parser.add_argument("--title_suffix", default='title')
    parser.add_argument("--comment_suffix", default='comment')
    return parser


if __name__ == '__main__':
    parser = add_arguments(argparse.ArgumentParser())
    args = parser.parse_args()
    title_list = args.title.read().splitlines()
    comment_list = args.comment.read().splitlines()
    data_set = list(zip(title_list, comment_list))
    random.shuffle(data_set)

    train_len = int(len(data_set)*0.7)
    title_train = open('train.' + args.title_suffix, 'w', encoding='utf-8')
    comment_train = open('train.' + args.comment_suffix, 'w', encoding='utf-8')
    title_test = open('test.' + args.title_suffix, 'w', encoding='utf-8')
    comment_test = open('test.' + args.comment_suffix, 'w', encoding='utf-8')
    for (title, comment) in data_set[:train_len]:
        title_train.write(title+'\n')
        comment_train.write(comment+'\n')
    for (title, comment) in data_set[train_len:]:
        title_test.write(title+'\n')
        comment_test.write(comment+'\n')

    # dev 파일과 vocab 파일 생성
    shutil.copyfile('test.'+args.title_suffix, 'dev.'+args.title_suffix)
    shutil.copyfile('test.'+args.comment_suffix, 'dev.'+args.comment_suffix)
    if args.vocab and os.path.isfile(args.vocab):
        shutil.copyfile(args.vocab, 'vocab.'+args.title_suffix)
        shutil.copyfile(args.vocab, 'vocab.'+args.comment_suffix)
