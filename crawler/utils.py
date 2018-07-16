import codecs
import os
import collections
from six.moves import cPickle
import numpy as np
import time_preprocess


class TimeLoader():
    def __init__(self, data_dir, batch_size, seq_length, encoding='utf-8'):
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.encoding = encoding

        input_file = os.path.join(data_dir, "input.txt")

        with codecs.open(input_file, "r", encoding=self.encoding) as f:
            data = f.readlines()
            data = [el.strip() for el in data]
            self.data = np.array(time_preprocess.preprocess_times(data))

        self.x_batches = []
        self.y_batches = []
        for i in range(0, len(self.data) - self.seq_length):
            self.x_batches.append(self.data[i: i + seq_length])
            self.y_batches.append(self.data[i + seq_length])


        self.num_batches = int(len(self.x_batches) / self.batch_size)
        if self.num_batches == 0:
            assert False, "Not enough data. Make seq_length and batch_size small."

        self.reset_batch_pointer()

    def next_batch(self):
        end_point = self.pointer + self.batch_size
        if end_point > len(self.x_batches):
            end_point = len(self.x_batches)
        x, y = self.x_batches[self.pointer:end_point], self.y_batches[self.pointer:end_point]
        self.pointer = end_point
        return x, y

    def reset_batch_pointer(self):
        self.pointer = 0
