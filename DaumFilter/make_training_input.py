#!/usr/bin/python3

"""
filtering 된 기사들을 여러 형태의 input으로 변환하는 스크립트
1. 띄어쓰기 기준으로 분리
2. konlpy를 사용하여 분리
"""

import re
import os
import argparse
import konlpy
import json
import random

# 느리고 성능이 안 좋은듯. Mecab 설치?
TAGGER = konlpy.tag.Kkma()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=['space', 'morpheme'], help="choice separating mode")
    parser.add_argument("input", type=argparse.FileType('r', encoding='utf-8'), help="json file which has title, comment field")
    parser.add_argument("--out_dir", type=str, default="./output")
    parser.add_argument("--out_base_name", type=str, default="output")
    parser.add_argument("--separate_title", action='store_true', help="with this, output will be separated in two parts, title and comment.")
    parser.add_argument("--title_suffix", type=str, default='title', help="suffix of title output file. if '--separate_title' option is not set, this option is ignored")
    parser.add_argument("--comment_suffix", type=str, default='comment', help="suffix of comment output file. if '--separate_title' option is not set, this option is ignored")
    parser.add_argument("--vocab_suffix", type=str, default='vocab', help="suffix of vocab output file.")
    return parser.parse_args()

def remove_useless_data(sentence):
    link_pattern = r'http(?:s?)://[\.a-zA-Z\/\?\_\-\,\=&#0-9]+'
    return re.sub(link_pattern, r'', sentence)

def parse_by_space(input_file):
    inputs = json.load(input_file)
    
    tokens = []
    for inp in inputs:
        title = remove_useless_data(inp['title'])
        title = re.sub(r'([^\w\s])', r' \1 ', title)
        title = re.sub(r'(\s|\n)+', r' ', title).strip()
        comments = [remove_useless_data(cmt) for cmt in inp['comments']]
        comments = [re.sub(r'([^\w\s])', r' \1 ', cmt) for cmt in comments]
        comments = [re.sub(r'(\s|\n)+', r' ', cmt).strip() for cmt in comments]
        tokens.append((title, comments))

    return tokens

def parse_by_morpheme(input_file):
    inputs = json.load(input_file)

    tokens = []
    for inp in inputs:
        title = remove_useless_data(inp['title'])
        title = [tag[0] for tag in TAGGER.pos(title)]
        title = ' '.join(title)
        comments = [remove_useless_data(cmt) for cmt in inp['comments']]
        comments = [[tag[0] for tag in TAGGER.pos(cmt)] for cmt in comments]
        comments = [' '.join(cmt) for cmt in comments]
        tokens.append((title, comments))

    return tokens

if __name__ == "__main__":
    args = parse_arguments()
    if args.mode == "space":
        result = parse_by_space(args.input)
    else:
        result = parse_by_morpheme(args.input)

    if not os.path.isdir(args.out_dir):
        os.makedirs(args.out_dir)

    vocab = set()
    if args.separate_title:
        title_path = os.path.join(args.out_dir, args.out_base_name + '.' + args.title_suffix)
        comment_path = os.path.join(args.out_dir, args.out_base_name + '.' + args.comment_suffix)

        title_out = open(title_path, 'w', encoding='utf-8')
        comment_out = open(comment_path, 'w', encoding='utf-8')

        for r in result:
            # comment 수만큼 title을 복사해서 write
            rand_nums = [str(random.randrange(1, 500000)) for _ in range(len(r[1]))]
            title = [' '.join([rand_nums[i], r[0]]) for i in range(len(r[1]))]
            title_out.write('\n'.join(title))
            comment_out.write('\n'.join(r[1]))

            # 마지막 요소를 제외하고는 개행
            if r != result[-1]:
                title_out.write('\n')
                comment_out.write('\n')

            vocab.update(rand_nums)
            vocab.update(r[0].split())
            for cmt in r[1]:
                vocab.update(cmt.split())

    else:
        output_path = os.path.join(args.out_dir, args.out_base_name + '.txt')
        
        out_file = open(output_path, 'w', encoding='utf-8')

        for r in result:
            title = r[0]
            lines = [title + ' ' + cmt for cmt in r[1]]

            out_file.write('\n'.join(lines))

            if r != result[-1]:
                out_file.write('\n')

            vocab.update(r[0].split())
            for cmt in r[1]:
                vocab.update(cmt.split())

    vocab_path = os.path.join(args.out_dir, args.out_base_name + '.' + args.vocab_suffix)

    vocab_file = open(vocab_path, 'w', encoding='utf-8')
    vocab_file.write('<unk>\n<s>\n</s>\n')
    vocab_file.write('\n'.join(vocab))
