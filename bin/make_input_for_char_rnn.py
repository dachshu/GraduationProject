#!/usr/bin/python3

import json
import argparse
from os import path
import os
import sys

def add_arguments(parser):
    parser.add_argument("title_comment_file", nargs="?", default=sys.stdin, type=argparse.FileType(mode='r', encoding='utf-8'), help="a JSON formatted file which has titles and comments of news articles")
    return parser

def print_pairs(json_input):
    for dic in json_input:
        title = dic["title"].replace("\n", " ")
        comments = dic["comments"]
        if len(comments) == 0:
            print("WARNING: a news item has no comments. so it is ignored.", file=sys.stderr)
            continue

        sys.stdout.write(title + "\t" + comments[0].replace("\n", " "))
        for comment in comments[1:]:
            sys.stdout.write("\n" + title + "\t" + comment.replace("\n", " "))

if __name__ == "__main__":
    parser = add_arguments(argparse.ArgumentParser())
    args = parser.parse_args()
    json_input = json.load(args.title_comment_file)
    print_pairs(json_input)
