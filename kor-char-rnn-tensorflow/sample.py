from __future__ import print_function
import tensorflow as tf

import os
from six.moves import cPickle

from model import Model

from six import text_type


def sample(save_dir, prime):
    with open(os.path.join(save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(save_dir, 'chars_vocab.pkl'), 'rb') as f:
        chars, vocab = cPickle.load(f)
    model = Model(saved_args, training=False)
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(save_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            return model.sample(sess, chars, vocab, 500, prime, 1)


if __name__ == '__main__':
    print('save dir : ')
    s = input()
    sample(s, '문')
