#!/usr/bin/env python
# -*- coding: utf-8 -*-
import spacy
import nltk
import string


class PipelinePreprocessor(object):
  def __init__(self):
    self.__features = []

  def set_features(self, features: list):
    self.__features = features

  def process(self, in_data):
    for label, texts in in_data.items():
      for i in range(len(texts)):
        texts[i] = self.batch_process(texts[i])
    return in_data

  def batch_process(self, text):
    for feature in self.__features:
      text = feature().apply(text)
    return text
