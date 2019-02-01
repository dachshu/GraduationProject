#!/usr/bin/python3

from gensim import models
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("training_file", type=str, help="a file path which will be used for training. each lines of file is one sentence.")
    parser.add_argument("-o", "--model_output", type=str, required=True, help="a path where the entire model will be saved")
    parser.add_argument("--wordvec_output", type=str, help="a path where the keyedvector will be saved in word2vec format")
    parser.add_argument("--init_model", type=str, help="a path of a model which is going to be used for incremental  training")
    parser.add_argument("--vec_size", type=int, default=256)
    parser.add_argument("--min_count", type=int, default=1)
    parser.add_argument("--window_size", type=int, default=5)
    parser.add_argument("--worker_num", type=int, default=7)

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    line_sentences = models.word2vec.LineSentence(args.training_file)
    is_model_loaded = args.init_model is not None
    if is_model_loaded:
        model = models.fasttext.FastText.load(args.init_model)
    else:
        model = models.fasttext.FastText(
                size=args.vec_size,
                window=args.window_size,
                workers=args.worker_num,
                min_count=args.min_count,
                sg=1, # use skip-gram
                )

    model.build_vocab(
            sentences=line_sentences,
            update=is_model_loaded
            )
    model.train(
            sentences=line_sentences,
            total_examples=model.corpus_count,
            epochs=model.iter
            )

    os.makedirs(os.path.dirname(args.model_output), exist_ok=True)
    model.save(args.model_output)

    if args.wordvec_output is not None:
        os.makedirs(os.path.dirname(args.wordvec_output), exist_ok=True)
        model.wv.save_word2vec_format(args.wordvec_output)
