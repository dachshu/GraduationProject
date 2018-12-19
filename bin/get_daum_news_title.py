#!/usr/bin/python3

import sys
import requests
import argparse
from bs4 import BeautifulSoup

def get_article_title(url):
    ret_url = url
    rq = requests.get(url)
    soup = BeautifulSoup(rq.text, 'html.parser')
    
    return soup.find('h3', class_='tit_view').text


def parse_argments(parser):
    parser.add_argument(
            "urls",
            nargs="*",
            help="""specify an url from which you get a title.
            if this arguments are not provided, the scripts would read urls from STDIN"""
            )
    return parser.parse_args()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parse_argments(parser)

    urls = args.urls
    if len(urls) == 0:
        urls = [u.strip() for u in sys.stdin.readlines()]

    for url in urls:
        print(get_article_title(url))

