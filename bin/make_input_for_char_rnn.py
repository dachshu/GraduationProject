#!/usr/bin/python3

import json
import argparse
from os import path
import os

def add_arguments(parser):
    parser.add_argument("title_comment_file", type=argparse.FileType(mode='r', encoding='utf-8'), help="a JSON formatted file which has titles and comments of news articles")
    parser.add_argument("out_dir", type=str, help="a directory where the output file will be stored at")
    return parser

def write_pairs_to_out_file(json_input, out_dir):
    with open(path.join(out_dir, "input.txt"), 'w', encoding='utf-8') as f:
        for dic in json_input:
            title = dic["title"].replace("\n", " ")
            comments = dic["comments"]
            f.write(title + "\t" + comments[0].replace("\n", " "))
            for comment in comments[1:]:
                f.write("\n" + title + "\t" + comment.replace("\n", " "))

if __name__ == "__main__":
    parser = add_arguments(argparse.ArgumentParser())
    args = parser.parse_args()
    if not path.isdir(args.out_dir):
        os.mkdir(args.out_dir)
    json_input = json.load(args.title_comment_file)
    write_pairs_to_out_file(json_input, args.out_dir)