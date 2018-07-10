import tensorflow as tf
import numpy as np
from tensorflow.contrib import rnn
import os
from utils import TimeLoader

import matplotlib
if "DISPLAY" not in os.environ:
    # remove Travis CI Error
    matplotlib.use('Agg')

import matplotlib.pyplot as plt

data_dir = './TimeData'
output_dir = './tTimeModeloutput'
checkpoint_path = os.path.join(output_dir, 'model.ckpt')

seq_length = 10
hidden_dim = 10
output_dim = 1
learning_rate = 0.01
iterations = 500
batch_size = 100

data_loader = TimeLoader(data_dir, batch_size, seq_length)

X = tf.placeholder(tf.int32, [None, seq_length])
Y = tf.placeholder(tf.int32, [None, 1])

def lstm_cell():
    cell = tf.contrib.rnn.BasicLSTMCell(
                num_units=hidden_dim, state_is_tuple=True, activation=tf.tanh)
    return cell

multi_cells = rnn.MultiRNNCell([lstm_cell() for _ in range(2)], state_is_tuple=True)
outputs, _states = tf.nn.dynamic_rnn(multi_cells, X, dtype=tf.float32)

Y_pred = tf.contrib.layers.fully_connected(
    outputs[:, -1], output_dim, activation_fn=None) 

loss = tf.reduce_sum(tf.square(Y_pred - Y))

optimizer = tf.train.AdamOptimizer(learning_rate)
train = optimizer.minimize(loss)

targets = tf.placeholder(tf.float32, [None, 1])
predictions = tf.placeholder(tf.float32, [None, 1])
rmse = tf.sqrt(tf.reduce_mean(tf.square(targets - predictions)))

with tf.Session() as sess:
    saver = tf.train.Saver(tf.global_variables())
    init = tf.global_variables_initializer()
    sess.run(init)

    # Training step
    for i in range(iterations):
        for b in range(data_loader.num_batches):
            trainX, trainY = data_loader.next_batch()
            _, step_loss = sess.run([train, loss], feed_dict={
                                X: trainX, Y: trainY})
            print("[step: {} , {}] loss: {}".format(i, b, step_loss))
        saver.save(sess, checkpoint_path, global_step=i * data_loader.num_batches)

    # Test step
    testX, testY = data_loader.next_batch()
    test_predict = sess.run(Y_pred, feed_dict={X: testX})
    rmse_val = sess.run(rmse, feed_dict={
                    targets: testY, predictions: test_predict})
    print("RMSE: {}".format(rmse_val))

    plt.plot(testY)
    plt.plot(test_predict)
    plt.xlabel("Time Period")
    plt.ylabel("Stock Price")
    plt.show()
