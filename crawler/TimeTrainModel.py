#!/usr/bin/python3

import tensorflow as tf
import numpy as np
from tensorflow.contrib import rnn
import os
from utils import TimeLoader
import time_preprocess
import argparse


data_dir = './TimeData'
output_dir = './TimeModelOutput'
checkpoint_path = os.path.join(output_dir, 'model.ckpt')

seq_length = 10
hidden_dim = 128 
output_dim = 1
learning_rate = 0.00001
iterations = 10
batch_size = 2 

data_loader = TimeLoader(data_dir, batch_size, seq_length)

X = tf.placeholder(tf.float32, [None, None, 1])
Y = tf.placeholder(tf.float32, [None, 1])
state_batch_size = tf.placeholder(tf.int32, shape=[])

def lstm_cell():
    cell = tf.contrib.rnn.BasicLSTMCell(
                num_units=hidden_dim, state_is_tuple=True, activation=tf.nn.softsign)
    return cell

multi_cells = rnn.MultiRNNCell([lstm_cell() for _ in range(2)], state_is_tuple=True)
initial_state = multi_cells.zero_state(state_batch_size, tf.float32)
outputs, _states = tf.nn.dynamic_rnn(multi_cells, X, initial_state=initial_state, dtype=tf.float32)

Y_pred = tf.contrib.layers.fully_connected(
    outputs[:, -1], output_dim, activation_fn=None) 

loss = tf.reduce_sum(tf.square(Y_pred - Y)) / 2

optimizer = tf.train.AdamOptimizer(learning_rate)
train_op = optimizer.minimize(loss)


def train():
    with tf.Session() as sess:
        saver = tf.train.Saver(tf.global_variables())
        latest_check_point = tf.train.latest_checkpoint(output_dir)
        if latest_check_point is None:
            init = tf.global_variables_initializer()
            sess.run(init)
        else:
            saver.restore(sess, latest_check_point)
            print("model restored from latest_check_point")
    
        # Training step
        for i in range(iterations):
            state = sess.run(initial_state, feed_dict={state_batch_size : batch_size})
            for b in range(data_loader.num_batches):
                trainX, trainY = data_loader.next_batch()
                trainX = np.reshape(trainX, (batch_size, seq_length, 1))
                trainY = np.reshape(trainY, (batch_size, 1))
                feed_dict = {X: trainX, Y: trainY, state_batch_size : batch_size}
                for j, (c, h) in enumerate(initial_state):
                    feed_dict[c] = state[j].c
                    feed_dict[h] = state[j].h

                _, step_loss = sess.run([train_op, loss], feed_dict=feed_dict)
                print("[step: {} , {}] loss: {}".format(i, b, step_loss))
            data_loader.reset_batch_pointer()
            saver.save(sess, checkpoint_path, global_step=i * data_loader.num_batches)
        
        testX, _ = data_loader.next_batch()
        testX = np.reshape(testX, (batch_size, seq_length, 1))
        test_predict = sess.run(Y_pred, feed_dict={X: testX, state_batch_size : batch_size})
        print(test_predict)

def sample(seed):
    num_sampling = 100

    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(output_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            state = sess.run(multi_cells.zero_state(1, tf.float32)) # RNN의 최초 state값을 0으로 초기화
            ret = []
            x = np.zeros((1, 1, 1))
            x[0, 0, 0] = time_preprocess.normalize(int(seed))

            for n in range(num_sampling):
                feed_dict = {X : x, state_batch_size : 1, initial_state : state}
                [probs_result, state] = sess.run([Y_pred, _states], feed_dict=feed_dict)

                pred = time_preprocess.restore_normalized_time(probs_result[0][0])
                if len(ret) > 0 and pred <= ret[-1]: break
                ret.append(pred)

                x = np.zeros((1, 1, 1))
                x[0, 0, 0] = probs_result[0][0]

            print(ret)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('op', choices=['train', 'sample'])
    parser.add_argument('seed', nargs='?', type=int)
    args = parser.parse_args()

    if args.op == 'sample' and args.seed is None:
        parser.error('you should give a seed')

    return args


if __name__ == '__main__':
    args = parse_arguments()
    if args.op == 'train':
        train()
    else:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        sample(args.seed)
