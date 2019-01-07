#!/usr/bin/python3

import argparse
import twitter
import sys

MAX_TWEET_LENGTH=140

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
    text_it = (text[i:i+MAX_TWEET_LENGTH] for i in range(0, len(text), MAX_TWEET_LENGTH))

    _ = [upload_tweet(t, keys) for t in text_it]
