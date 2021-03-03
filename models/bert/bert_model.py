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

tf.get_logger().setLevel('ERROR')

# Download the IMDB dataset

dataset_dir = 'Istio_data'

train_dir = os.path.join(dataset_dir, 'train')
test_dir = os.path.join(dataset_dir, 'test')

AUTOTUNE = tf.data.AUTOTUNE
batch_size = 32
seed = 42
epochs = 60

raw_train_ds = tf.keras.preprocessing.text_dataset_from_directory(
    directory=train_dir,
    batch_size=batch_size,
    validation_split=0.2,
    subset='training',
    seed=seed)

class_names = raw_train_ds.class_names
train_ds = raw_train_ds.cache().prefetch(buffer_size=AUTOTUNE)

val_ds = tf.keras.preprocessing.text_dataset_from_directory(
    directory=train_dir,
    batch_size=batch_size,
    validation_split=0.2,
    subset='validation',
    seed=seed)

val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

test_ds = tf.keras.preprocessing.text_dataset_from_directory(
    test_dir,
    batch_size=batch_size)

test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

# Loading models from TensorFlow Hub
bert_model_name = 'small_bert/bert_en_uncased_L-12_H-768_A-12'
tfhub_handle_encoder = name_to_handle(bert_model_name)
bert_model = hub.KerasLayer(tfhub_handle_encoder)
tfhub_handle_preprocess = model_to_preprocess(bert_model_name)
bert_preprocess_model = hub.KerasLayer(tfhub_handle_preprocess)

# define your model
def build_classifier_model():
  inputs = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
  preprocessing_layer = hub.KerasLayer(tfhub_handle_preprocess, name='preprocessing')
  encoder_inputs = preprocessing_layer(inputs)
  encoder = hub.KerasLayer(tfhub_handle_encoder, trainable=True, name='BERT_encoder')
  outputs = encoder(encoder_inputs)
  net = outputs['pooled_output']
  net = tf.keras.layers.Dropout(0.1)(net)
  net = tf.keras.layers.Dense(5, activation='softmax', name='classifier')(net)
  return tf.keras.Model(inputs, net)

classifier_model = build_classifier_model()

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


#bert_raw_result = classifier_model(tf.constant(text_test))
#print(tf.sigmoid(bert_raw_result))

#tf.keras.utils.plot_model(classifier_model)