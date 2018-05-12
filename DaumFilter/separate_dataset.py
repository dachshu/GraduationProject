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
    parser.add_argument("--out_dir", default='output')
    return parser


if __name__ == '__main__':
    parser = add_arguments(argparse.ArgumentParser())
    args = parser.parse_args()
    title_list = args.title.read().splitlines()
    comment_list = args.comment.read().splitlines()
    data_set = list(zip(title_list, comment_list))
    random.shuffle(data_set)

    train_path = (os.path.join(args.out_dir, 'train.' + args.title_suffix), os.path.join(args.out_dir, 'train.' + args.comment_suffix))
    test_path = (os.path.join(args.out_dir, 'test.' + args.title_suffix), os.path.join(args.out_dir, 'test.' + args.comment_suffix))
    dev_path = (os.path.join(args.out_dir, 'dev.' + args.title_suffix), os.path.join(args.out_dir, 'dev.' + args.comment_suffix))
    vocab_path = (os.path.join(args.out_dir, 'vocab.' + args.title_suffix), os.path.join(args.out_dir, 'vocab.' + args.comment_suffix))

    train_len = int(len(data_set)*0.7)
    title_train = open(train_path[0], 'w', encoding='utf-8')
    comment_train = open(train_path[1], 'w', encoding='utf-8')
    title_test = open(test_path[0], 'w', encoding='utf-8')
    comment_test = open(test_path[1], 'w', encoding='utf-8')
    for (title, comment) in data_set[:train_len]:
        title_train.write(title+'\n')
        comment_train.write(comment+'\n')
    for (title, comment) in data_set[train_len:]:
        title_test.write(title+'\n')
        comment_test.write(comment+'\n')

    # dev 파일과 vocab 파일 생성
    shutil.copyfile(test_path[0], dev_path[0])
    shutil.copyfile(test_path[1], dev_path[1])
    if args.vocab and os.path.isfile(args.vocab):
        shutil.copyfile(args.vocab, vocab_path[0])
        shutil.copyfile(args.vocab, vocab_path[1])
