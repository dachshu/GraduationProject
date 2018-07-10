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
            data = [int(el) for el in data]
            self.data = time_preprocess.preprocess_times(data)

        self.num_batches = int(self.data.size / (self.batch_size *
                                                   self.seq_length))
        if self.num_batches == 0:
            assert False, "Not enough data. Make seq_length and batch_size small."
        self.data = self.data[:self.num_batches * self.batch_size * self.seq_length]
        xdata = self.data
        ydata = np.copy(self.data)
        ydata[:-1] = xdata[1:]
        ydata[-1] = xdata[0]
        self.x_batches = np.split(xdata.reshape(self.batch_size, -1), self.num_batches, 1)
        self.y_batches = np.split(ydata.reshape(self.batch_size, -1),
                                  self.num_batches, 1)
        self.reset_batch_pointer()



    def next_batch(self):
        x, y = self.x_batches[self.pointer], self.y_batches[self.pointer]
        self.pointer += 1
        return x, y

    def reset_batch_pointer(self):
        self.pointer = 0