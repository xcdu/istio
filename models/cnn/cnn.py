#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
import json
from keras_bert import extract_embeddings
import numpy

import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from manual import IstioManual
from modules.factory import Modules
from modules.nlp_preprocess.feature import BertFeature
from modules.nlp_preprocess.feature import SpacyFeature
from modules.nlp_preprocess.input_adapter import IstioManualInputAdaptor
from modules.nlp_preprocess.preprocessor import PipelinePreprocessor
from parsedocs.data_helper import load_pages_from_dir
from keras import layers, models, optimizers
from keras.preprocessing import sequence
from keras.preprocessing import text

in_path = "../../.data/"

raw_pages = load_pages_from_dir(in_path)

manual = IstioManual()
manual.build(pages=raw_pages)

input_adapter = IstioManualInputAdaptor()
data = input_adapter.multilevel_format(manual.manual)

preprocessor = PipelinePreprocessor()
preprocessor.set_features([SpacyFeature])
data = preprocessor.process(in_data=data[3])

texts = list()
labels = list()
for indexer, contents in data.items():
  for content in contents:
    texts.append(content)
    labels.append(indexer)

print("NUMBER OF LABELS: {}".format(len(set(labels))))
print("NUMBER OF SLICED CONTENTS: {}".format(len(set(texts))))

df = pd.DataFrame()
df["text"] = texts
df["label"] = labels

label_encoder = LabelEncoder()
df["label"] = label_encoder.fit_transform(df["label"])

modules = Modules()
bert = modules.get("bert")

all_text = " ".join(df["text"])
embedding_tokens = bert.embedding(all_text)
# word_index = {word: i for i, word in embedding_tokens.keys()}
# for token_, embedding in embedding_tokens.items():
#   embedding_matrix[word_index[token_]] = embedding

for i in range(len(df["text"])):
  (df["text"])[i] = [key for key in bert.embedding((df["text"])[i])]

train_x, valid_x, train_y, valid_y = train_test_split(df["text"], df["label"])

token = text.Tokenizer()
token = token.fit_on_sequences(df["text"])
word_index = token.word_index

train_seq_x = sequence.pad_sequences(token.texts_to_sequences(train_x),
                                     maxlen=10)
valid_seq_x = sequence.pad_sequences(token.texts_to_sequences(valid_x),
                                     maxlen=10)

embedding_matrix = numpy.zeros((len(embedding_tokens.keys()), 512))
for word, i in word_index.items():
  embedding_vector = embedding_tokens[word]
  embedding_matrix[i] = embedding_vector


def train_model(classifier, feature_vector_train, label, feature_vector_valid,
                is_neural_net=False):
  # fit the training dataset on the classifier
  classifier.fit(feature_vector_train, label)

  # predict the labels on validation dataset
  predictions = classifier.predict(feature_vector_valid)

  if is_neural_net:
    predictions = predictions.argmax(axis=-1)

  return metrics.accuracy_score(predictions, valid_y)


def create_cnn(word_index, embedding_matrix):
  # Add an Input Layer
  input_layer = layers.Input((70,))

  # Add the word embedding Layer
  embedding_layer = layers.Embedding(len(word_index) + 1, 512,
                                     weights=[embedding_matrix],
                                     trainable=False)(input_layer)
  embedding_layer = layers.SpatialDropout1D(0.3)(embedding_layer)

  # Add the convolutional Layer
  conv_layer = layers.Convolution1D(100, 3, activation="relu")(
    embedding_layer)

  # Add the pooling Layer
  pooling_layer = layers.GlobalMaxPool1D()(conv_layer)

  # Add the output Layers
  output_layer1 = layers.Dense(50, activation="relu")(pooling_layer)
  output_layer1 = layers.Dropout(0.25)(output_layer1)
  output_layer2 = layers.Dense(1, activation="sigmoid")(output_layer1)

  # Compile the model
  model = models.Model(inputs=input_layer, outputs=output_layer2)
  model.compile(optimizer=optimizers.Adam(),
                loss='sparse_categorical_crossentropy')

  return model
#
#
classifier = create_cnn(word_index, embedding_matrix)
accuracy = train_model(classifier, train_seq_x, train_y, valid_seq_x,
                       is_neural_net=True)
print("CNN, Word Embeddings", accuracy)
