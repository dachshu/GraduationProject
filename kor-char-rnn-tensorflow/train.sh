#!/bin/bash

#python3 train.py --data_dir data/news/ --save_dir save/news/ --rnn_size 1024 --num_layers 3 --num_epochs 100 --batch_size 120 "$@"
python3 train.py --data_dir data/news/ --save_dir save/news/ --rnn_size 1024 --num_layers 3 --num_epochs 100 --batch_size 60 "$@"
