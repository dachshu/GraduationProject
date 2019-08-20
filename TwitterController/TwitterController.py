#!/usr/bin/python3

import twitter
import click
import sys
import json


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

    api = create_api_instance(key_file)
    if user_name is None and user_id is None:
        timeline_data = api.GetHomeTimeline(count=num_status)
    else:
        timeline_data = api.GetUserTimeline(
            screen_name=user_name, user_id=user_id, count=num_status)

    print(json.dumps([data.AsJsonString(ensure_ascii=False)
                      for data in timeline_data], ensure_ascii=False))


@cli.command()
@click.option('--key_file', type=click.File(), required=True, help="A file in which api tokens are")
@click.argument('tweet_id', type=click.INT)
def retweet(key_file, tweet_id):
    api = create_api_instance(key_file)
    api.PostRetweet(tweet_id)


@cli.command()
@click.option('--key_file', type=click.File(), required=True, help="A file in which api tokens are")
@click.option('--get_category', is_flag=True, help="If this flag is set, it prints suggestion categories")
@click.option('--from_category', 'category', help="Print suggested users from specified category", metavar="CATEGORY")
def suggest(key_file, get_category, category):
    api = create_api_instance(key_file)

    if not get_category and category is None:
        print(
            "Error: either --get_category or --from_category is required.", file=sys.stderr)
        raise click.Abort()

    categories = api.GetUserSuggestionCategories()

    if category is not None:
        print_suggested_users(api, categories, category)
    else:
        for cat in categories:
            print(cat.name)


def find_category(categories, category_name):
    for cat in categories:
        if cat.name == category_name:
            selected_cat = cat
            break

    if selected_cat is None:
        print("Error: the category doesn't exist.", file=sys.stderr)
        exit(1)

    return selected_cat


def print_suggested_users(api, categories, category_name):
    cat = find_category(categories, category_name)
    user_list = api.GetUserSuggestion(cat)
    for user in user_list:
        print(user.screen_name)


def create_api_instance(key_file):
    keys = [key.strip() for key in key_file.readlines()]
    return twitter.Api(consumer_key=keys[0],
                       consumer_secret=keys[1],
                       access_token_key=keys[2],
                       access_token_secret=keys[3])


if __name__ == '__main__':
    cli()
