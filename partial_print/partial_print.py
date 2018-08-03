#!/usr/bin/python3

import sys
import argparse


def add_arguments(arg_parser):
    arg_parser.add_argument("ranges", nargs="+", help="""ranges of characters to be printed.
            'N-' will print from nth character to end.
            '-M' will print from first character to mth character.
            'N-M' will print from nth character to mth character.
            'N' will print only nth character.""")
    return arg_parser


def parse_range(rang):
    range_values = rang.split('-')

    assert len(range_values) > 0 and len(range_values) < 3, "wrong range input."

    if len(range_values) == 1:
        val = int(range_values[0])
        return [val, val+1]

    return [None if val == '' else int(val) for val in range_values]
    

if __name__ == '__main__':
    parser = add_arguments(argparse.ArgumentParser())
    args = parser.parse_args()

    print_ranges = [parse_range(rang) for rang in args.ranges]

    input_text = sys.stdin.read()
    for rang in print_ranges:
        print(input_text[rang[0]:rang[1]])
