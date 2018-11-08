import argparse
import os
from os import path

def parse_arguments(parser):
    parser.add_argument("log_dir", help="Specifies a directory where log files are.")
    parser.add_argument("-a", "--all", type=bool, help="Shows entire status, not current status.")
    args = parser.parse_args()
    if not path.is_dir(args.log_dir):
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
    with open(path.join(log_dir, "general.log"), 'r') as log:
        if show_all:
            print(log.read())
        else:
            print(log.readlines()[-1])

        for root, _, files in os.walk(path.join(log_dir, "detail", "upload_comment_tweet")):
            for f_name in files:
                with open(path.join(root,f_name), 'r') as at_log:
                    # title, url, comment1, comment2
                    info = at_log.readlines()[-4:]
                    t, _ = path.splitext(f_name)
                    print_at_job_log(t, info, show_all)


if __name__ == "__main__":
    args = parse_arguments(argparse.ArgumentParser())
    show_status(args.log_dir, args.all)
    pass
