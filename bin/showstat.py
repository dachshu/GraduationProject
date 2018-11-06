import argparse

def parse_arguments(parser):
    parser.add_argument("log_dir", help="Specifies a directory where log files are.")
    parser.add_argument("-a", "--all", type=bool, help="Shows entire status, not current status.")
    return parser.parse_args()


def show_status(log_dir, show_all):
    if show_all:
        pass


if __name__ == "__main__":
    args = parse_arguments(argparse.ArgumentParser())
    show_status(args.log_dir, args.all)
    pass
