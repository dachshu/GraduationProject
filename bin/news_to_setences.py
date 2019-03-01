#!/usr/bin/python3

import json
import argparse
from os import path
import os
import sys

def add_arguments(parser):
    parser.add_argument("title_comment_file", nargs="?", default=sys.stdin, type=argparse.FileType(mode='r', encoding='utf-8'), help="a JSON formatted file which has titles and comments of news articles")
    return parser

def print_news(json_input):
    for dic in json_input:
        title = dic["title"].replace("\n", " ")
        print(title)

        comments = dic["comments"]
        for comment in comments:
            print(comment.replace("\n", " "))

if __name__ == "__main__":
    parser = add_arguments(argparse.ArgumentParser())
    args = parser.parse_args()
    json_input = json.load(args.title_comment_file)
    print_news(json_input)

