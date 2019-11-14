#!/usr/bin/python3
import argparse
import os
import json
import sys

def add_arguments(arg_parser):
    arg_parser.add_argument("archive", nargs="*", help="archives to be filtered")
    arg_parser.add_argument("-c", "--max-comment-num", type=int, default=100, help="a number that commments will be filtered")
    arg_parser.add_argument("--out-plain-text", action="store_true", help="print comments as plain text, not as json structure")
    return arg_parser

# 걸러진 댓글들을 반환하는 함수
def filter_comment(archive_file, max_count):
    archive_dict = json.load(archive_file)
    title = archive_dict["title"].replace("\t", " ")
    comment_list = get_comment_list(archive_dict)

    result = sorted(comment_list, key=lambda o: int(o["like"]), reverse=True)
    result_len = len(result)
    result_len = min(result_len, max_count)

    result_dict = {"title":title, "comments":[cmt["text"].replace("\t", " ") for cmt in result[:int(result_len)]]}
    if len(result_dict["comments"]) == 0:
        print("WARNING: a news item(\'%s\', in \'%s\') has no comments" % (title, archive_file.name), file=sys.stderr)
    return result_dict


# 전체 기록에서 댓글만 반환하는 함수
def get_comment_list(archive_dict):
    return archive_dict["comment"].values()


if __name__ == "__main__":
    parser = add_arguments(argparse.ArgumentParser())
    args = parser.parse_args()
    inputs = args.archive

    # input들을 모두 open함
    archives = []
    # 명령줄 입력이 없으면 stdin에서 읽음
    if len(inputs) == 0:
        inputs += list(map(lambda x: x.strip(), sys.stdin.readlines()))
    if all([os.path.isfile(inp) or os.path.isdir(inp) for inp in inputs]):
        for inp in inputs:
            if os.path.isdir(inp):
                for (path, dir, files) in os.walk(inp):
                    archives += [os.path.join(path,f) for f in files]
            else:
                archives.append(inp)
    else:
        parser.error("The input archives are neither directories nor files")

    result = [filter_comment(open(archive), args.max_comment_num) for archive in archives]
    if args.out_plain_text:
        for r in result:
            comments = [comment.replace("\n", "") for comment in r["comments"]]
            print("\n".join(comments))
    else:
        print(json.dumps(result, ensure_ascii=False))

