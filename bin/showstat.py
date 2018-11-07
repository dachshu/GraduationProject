#!/usr/bin/python3
import argparse
import os
from os import path
import re

def parse_arguments(parser):
    parser.add_argument("log_dir", help="Specifies a directory where log files are.")
    parser.add_argument("-a", "--all", action="store_true", help="Shows entire status, not current status.")
    args = parser.parse_args()
    if not path.isdir(args.log_dir):
        parser.error("LOG_DIR is not a directory")
    return args


def print_at_job_log(time, at_log, show_all):
    if show_all:
        print("Time: " + time)
        print("Title: " + at_log[0].strip())
        print("URL: " + at_log[1].strip())
        print("Comment1: " + at_log[2].strip())
        print("Comment2: " + at_log[3].strip())
    else:
        print("Time: " + time)
        print("Title: " + at_log[0].strip())
        print("Comment1: " + at_log[2].strip())
        print("Comment2: " + at_log[3].strip())



def show_status(log_dir, show_all):
    LAST_PATTERN = re.compile(r"\[INFO\] Finished .+")

    with open(path.join(log_dir, "general.log"), 'r') as log:
        log_data = log.readlines()
        if show_all:
            print(''.join(log_data))
        else:
            print(log_data[-1])

        if LAST_PATTERN.fullmatch(log_data[-1].strip()):
            print("--- Generated comments ---")
            for root, _, files in os.walk(path.join(log_dir, "detail", "upload_comment_tweet")):
                for f_name in files:
                    with open(path.join(root,f_name), 'r') as at_log:
                        # info format: [title, url, comment1, comment2]
                        info = at_log.readlines()[-4:]
                        t, _ = path.splitext(f_name)
                        print_at_job_log(t, info, show_all)


if __name__ == "__main__":
    args = parse_arguments(argparse.ArgumentParser())
    show_status(args.log_dir, args.all)
