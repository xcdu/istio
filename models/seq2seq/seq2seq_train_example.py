#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models.seq2seq.seq2seq_model import Seq2Seq
from tensorflow import keras


def train():
    vocab_words = None
    special_words = []
    vocab_words = special_words + vocab_words
    vocab2id = None
    id2vocab = None

    num_sample = 1000
    source_data = None
    source_data_ids = None
    target_data = None
    target_data_ids = None

    source_input_ids = None
    target_input_ids = None
    target_output_ids = None

    max_len = 10
    embedding_dim = 50
    hidden_units = 128
    vocab_size = len(vocab2id)
    model = Seq2Seq(man_len=max_len, embedding_dim=embedding_dim, hidden_units=hidden_units, vocab_size=vocab_size)

    epochs = 10
    batch_size = 32
    val_rate = 0.2
    loss_function = keras.losses.SparseCategoricalCrossentropy()
    model.compile(loss=loss_function, optimizer="adam")
    model.fit([source_input_ids, target_input_ids], target_output_ids, batch_size=batch_size, epochs=epochs,
              validation_split=val_rate)

    # model.save_weights("")
