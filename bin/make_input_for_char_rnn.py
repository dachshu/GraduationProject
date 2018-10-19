#!/usr/bin/python3

import json
import argparse

def add_arguments(parser):
    parser.add_argument("title_comment_file", type=argparse.FileType(mode='r', encoding='utf-8'), help="a JSON formatted file which has titles and comments of news articles")
    parser.add_argument("out_file", type=argparse.FileType(mode='w', encoding='utf-8'), help="a file which will store the output of this script")
    return parser

def write_pairs_to_out_file(json_input, out_file):
    for dic in json_input:
        for comment in dic["comments"]:
            out_file.write(dic["title"].replace("\n", " ") + "\t" + comment.replace("\n", " ") + "\n")

if __name__ == "__main__":
    parser = add_arguments(argparse.ArgumentParser())
    args = parser.parse_args()
    json_input = json.load(args.title_comment_file)
    write_pairs_to_out_file(json_input, args.out_file)