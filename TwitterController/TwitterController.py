#!/usr/bin/python3

import twitter
import click
import sys
import json
import tweepy


@click.group()
def cli():
    pass


@cli.command()
@click.option('--key_file', type=click.File(), required=True, help="A file in which api tokens are")
@click.option('--user_name', '-u', help="Twitter screen name", metavar="USER_NAME")
@click.option('--user_id', help="Twitter numeric id", metavar="USER_ID(INTEGER)")
@click.option('--unfollow', is_flag=True, help="Unfollow a user rather than follow")
def follow(key_file, user_name, user_id, unfollow):
    if not (user_name is not None or user_id is not None):
        print("Error: either --user_name or --user_id is required. not both, not none.", file=sys.stderr)
        raise click.Abort()

    api = create_api_instance(key_file)
    if unfollow:
        api.DestroyFriendship(screen_name=user_name, user_id=user_id)
    else:
        api.CreateFriendship(screen_name=user_name, user_id=user_id)


@cli.command()
@click.option('--key_file', type=click.File(), required=True, help="A file in which api tokens are")
@click.option('--user_name', '-u', help="Twitter screen name", metavar="USER_NAME")
@click.option('--user_id', help="Twitter numeric id", metavar="USER_ID(INTEGER)")
@click.option('--num_status', type=click.INT, default=20, help="A number of status to be printed. this may not be greatr than 200.")
def timeline(key_file, user_name, user_id, num_status):
    if user_name is not None and user_id is not None:
        print(
            "Error: either --user_name or --user_id is required, not both.", file=sys.stderr)
        raise click.Abort()

    # python-twitter 로는 자신의 timeline 가져오기가 동작하지 않아서 tweepy로 교체
    keys = [key.strip() for key in key_file.readlines()]
    auth = tweepy.OAuthHandler(keys[0], keys[1])
    auth.set_access_token(keys[2], keys[3])
    api = tweepy.API(auth)

    if user_name is None and user_id is None:
        timeline_data = api.me().timeline(count=num_status, tweet_mode='extended')
    else:
        id = user_name if user_name is not None else user_id
        timeline_data = api.user_timeline(
            id, count=num_status, tweet_mode='extended')

    for data in timeline_data:
        print(vars(data)['full_text'].replace("\n", " "))


@cli.command()
@click.option('--key_file', type=click.File(), required=True, help="A file in which api tokens are")
@click.argument('tweet_id', type=click.INT)
def retweet(key_file, tweet_id):
    api = create_api_instance(key_file)
    api.PostRetweet(tweet_id)


def create_api_instance(key_file):
    keys = [key.strip() for key in key_file.readlines()]
    return twitter.Api(consumer_key=keys[0],
                       consumer_secret=keys[1],
                       access_token_key=keys[2],
                       access_token_secret=keys[3])


if __name__ == '__main__':
    cli()
