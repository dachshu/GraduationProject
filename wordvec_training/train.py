#!/usr/bin/python3

from gensim import models
import argparse
import os

VECTOR_SIZE=1000

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("train_file", type=argparse.FileType('r', encoding='utf-8'))
    parser.add_argument("-o", "--output_model_name", default='model')
    parser.add_argument("--output_wv_name", default='wordvec')
    parser.add_argument("--output_vocab_name", default='vocab')
    parser.add_argument("--output_dir", default='./save')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse()
    sentences = models.word2vec.LineSentence(args.train_file)
    output_path = os.path.join(args.output_dir, args.output_model_name)
    output_wv_path = os.path.join(args.output_dir, args.output_wv_name)
    output_vocab_path = os.path.join(args.output_dir, args.output_vocab_name)

    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
        print("made output directory")
    if not os.path.isfile(output_path):
        model = models.word2vec.Word2Vec(sentences=sentences, size=VECTOR_SIZE, workers=4)
    else:
        model = models.word2vec.Word2Vec.load(output_path)
        model.build_vocab(sentences, update=True)
        model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)

    print("training compelete")

    model.save(output_path)
    print("model is saved")
    model.wv.save(output_wv_path)
    print("word vector & vocab are saved")
