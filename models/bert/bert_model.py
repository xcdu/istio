#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from official.nlp import optimization  # to create AdamW optmizer

import matplotlib.pyplot as plt

from model_mapping import name_to_handle, model_to_preprocess
from data_preprocessing import get_data

tf.get_logger().setLevel('ERROR')
data_path = "post_fixed.csv"
bert_model_name = 'small_bert/bert_en_uncased_L-12_H-768_A-12'
AUTOTUNE = tf.data.AUTOTUNE
batch_size = 32
seed = 42
epochs = 20

train_ds, val_ds, test_ds, vocab_size = get_data(data_path, bert_model_name, batch_size, 70, 10, 20)
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

# Loading models from TensorFlow Hub
tfhub_handle_encoder = name_to_handle(bert_model_name)
bert_model = hub.KerasLayer(tfhub_handle_encoder)
tfhub_handle_preprocess = model_to_preprocess(bert_model_name)
bert_preprocess_model = hub.KerasLayer(tfhub_handle_preprocess)

class bert_classifier_model(tf.keras.Model):

    def __init__(self, vocabulary_size, embedding_dimensions, cnn_filters, dnn_units, model_output_classes,
                 dropout_rate, training=False, name="text_model"):
        super(bert_classifier_model, self).__init__(name=name)
        self.embedding = tf.keras.layers.Embedding(vocabulary_size, embedding_dimensions)
        self.cnn_layer1 = tf.keras.layers.Conv1D(filters=cnn_filters,
                                                 kernel_size=2,
                                                 padding="valid",
                                                 activation="relu")
        self.cnn_layer2 = tf.keras.layers.Conv1D(filters=cnn_filters,
                                                 kernel_size=3,
                                                 padding="valid",
                                                 activation="relu")
        self.cnn_layer3 = tf.keras.layers.Conv1D(filters=cnn_filters,
                                                 kernel_size=4,
                                                 padding="valid",
                                                 activation="relu")
        self.pool = tf.keras.layers.GlobalMaxPool1D()
        self.dense1 = tf.keras.layers.Dense(units=dnn_units, activation="relu")
        self.dense2 = tf.keras.layers.Dense(units=model_output_classes, activation="softmax")
        self.dropout = tf.keras.layers.Dropout(rate=dropout_rate)

    def call(self, inputs, training):
        layer0 = self.embedding(inputs)
        layer1 = self.cnn_layer1(layer0)
        layer1 = self.pool(layer1)
        layer2 = self.cnn_layer2(layer0)
        layer2 = self.pool(layer2)
        layer3 = self.cnn_layer3(layer0)
        layer3 = self.pool(layer3)
        all_layers = tf.concat([layer1, layer2, layer3], axis=-1)
        all_layers = self.dense1(all_layers)
        all_layers = self.dropout(all_layers, training)
        all_layers = self.dense2(all_layers)
        return all_layers

classifier_model = bert_classifier_model(vocabulary_size=vocab_size, embedding_dimensions=200, cnn_filters=100,
                                         dnn_units=256, model_output_classes=5, dropout_rate=0.2)

classifier_model.compile(
    optimizer=tf.keras.optimizers.RMSprop(),  # Optimizer
    # Loss function to minimize
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    # List of metrics to monitor
    metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
)
history = classifier_model.fit(
    train_ds,
    batch_size=batch_size,
    epochs=epochs,
    validation_data=val_ds,
)
results = classifier_model.evaluate(test_ds, batch_size=batch_size)
print("test loss, test acc:", results)

# bert_raw_result = classifier_model(tf.constant(text_test))
# print(tf.sigmoid(bert_raw_result))

# tf.keras.utils.plot_model(classifier_model)
