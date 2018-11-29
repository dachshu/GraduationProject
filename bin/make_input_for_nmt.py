#!/usr/bin/python3

import json
import argparse
import itertools
import re
import shutil
from os import path
import os
import sys

TITLE_SUFFIX="title"
COMMENT_SUFFIX="comment"
white_to_space = re.compile(r"\s+")

def add_arguments(parser):
    parser.add_argument("out_dir", type=str, help="a directory where title, comment, vocab files will be saved")
    parser.add_argument("-n", "--max_num", type=int, default=7000, help="a maximum number of comments that the output files can have")
    return parser

def write_output_files(json_input, out_dir, max_comment_num):
    #각 타이틀에 대해
    #   제목의 whitespace들을 공백문자로 변경
    #   변경된 제목을 공백으로 분리해서 set에 추가
    #   댓글들을 순회하며
    #       댓글의 모든 whitespace들을 공백문자로 변경
    #       title 파일에 제목을 작성하고 comment 파일에 댓글 작성
    #       댓글을 공백으로 분리해서 set에 추가
    join_out_path = lambda f: path.join(out_dir, f)
    open_out_file = lambda p, mod: open(join_out_path(p), mod, encoding='utf-8')
    vocab = set()
    total_comment_num = 0

    for i, dic in enumerate(json_input):
        title = white_to_space.sub(" ", dic["title"])
        vocab.update(title.split(" "))
        comment_it = itertools.islice(map(lambda cmt: white_to_space.sub(" ", cmt), dic["comments"]), max_comment_num - total_comment_num)
        comments = list(comment_it)
        total_comment_num += len(comments)
        train_set_num = int(len(comments)*0.7)
        
        is_this_last_item = (i+1) == len(json_input)
        terminator =  '\n' if not is_this_last_item else ''
        open_mode = 'a' if i != 0 else 'w'

        with open_out_file("train.title", open_mode) as train_title, open_out_file("train.comment", open_mode) as train_comment:
            train_title.write('\n'.join(itertools.repeat(title, train_set_num)) + terminator)
            train_comment.write('\n'.join(comments[:train_set_num]) + terminator)

        with open_out_file("test.title", open_mode) as test_title, open_out_file("test.comment", open_mode) as test_comment:
            test_title.write('\n'.join(itertools.repeat(title, len(comments)-train_set_num)) + terminator)
            test_comment.write('\n'.join(comments[train_set_num:]) + terminator)

        for comment in comments:
            vocab.update(comment.split(" "))

    with open_out_file("vocab.title", 'w') as vocab_title:
        vocab_title.write('<unk>\n<s>\n</s>\n')
        vocab_title.write('\n'.join(vocab))

    shutil.copyfile(join_out_path("test.title"), join_out_path("dev.title"))
    shutil.copyfile(join_out_path("test.comment"), join_out_path("dev.comment"))


if __name__ == "__main__":
    parser = add_arguments(argparse.ArgumentParser())
    args = parser.parse_args()
    if not path.isdir(args.out_dir):
        os.makedirs(args.out_dir, exist_ok=True)
    json_input = json.load(sys.stdin)
    write_output_files(json_input, args.out_dir, args.max_num)
