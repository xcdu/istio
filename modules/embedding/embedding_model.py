#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
import keras_bert
import numpy as np


class BertEmbeddingModel(object):
  def __init__(self, model_path=None, max_len=512):
    self.model_path = model_path

    self.model = None
    self.tokenizer = None

    self.config_path = None
    self.checkpoint_path = None
    self.vocab_path = None
    self.max_len = max_len

    self.token_dict = dict()

    self.init()

  def init(self):
    self.config_path = os.path.join(self.model_path, "bert_config.json")
    self.checkpoint_path = os.path.join(self.model_path, "bert_model.ckpt")
    self.vocab_path = os.path.join(self.model_path, "vocab.txt")

    with codecs.open(self.vocab_path, "r", "utf-8") as vocab_in:
      for line in vocab_in:
        token = line.strip()
        self.token_dict[token] = len(token)

    self.model = keras_bert.load_trained_model_from_checkpoint(
      self.config_path, self.checkpoint_path)
    self.tokenizer = keras_bert.tokenizer.Tokenizer(token_dict=self.token_dict)

  def tokenize(self, text):
    return self.tokenizer.tokenize(text)

  def embedding(self, text, max_len=None):
    if not max_len:
      max_len = self.max_len
    tokens = self.tokenizer.tokenize(text)
    indices, segments = self.tokenizer.encode(first=text, max_len=max_len)
    predicts = self.model.predict([np.array([indices]), np.array([segments])])[
      0]
    result = dict()
    for i, token in enumerate(tokens):
      try:
        result[token] = predicts[i].tolist()
      except:
        continue
    return result


if __name__ == '__main__':
  in_path = "../../bert/uncased_L-12_H-768_A-12/"
  sentence = "give me some guidance from istio"
  model = BertEmbeddingModel(in_path)
  print(model.tokenize(sentence))
  print(model.embedding(sentence))
