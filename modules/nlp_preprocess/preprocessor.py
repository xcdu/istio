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
    for label in in_data.keys():
        in_data[label] = self.feature_process(in_data[label])
    return in_data

  def feature_process(self, texts):
    for feature in self.__features:
      texts = feature().apply(texts)
    return texts
