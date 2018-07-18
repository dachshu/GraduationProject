#!/usr/bin/python3

import argparse
import twitter
import sys


def upload_tweet(text, keys):
    api = twitter.Api(consumer_key=keys[0],
            consumer_secret=keys[1], 
            access_token_key=keys[2],
            access_token_secret=keys[3])
    return api.PostUpdate(text)


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key', type=argparse.FileType('r'), required=True, help="Twitter API key file")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_argument()
    keys = [key.strip() for key in args.key.readlines()]
    text = sys.stdin.read()

    upload_tweet(text, keys)

