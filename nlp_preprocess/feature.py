#!/usr/bin/env python
# -*- coding: utf-8 -*-
from nltk.corpus import stopwords
from nlp_preprocess.factory import Modules


class BaseFeature(object):
  def apply(self, text):
    return


class SpacyFeature(object):
  def __init__(self):
    self.nlp = Modules().get("spacy")

  def apply(self, text: str):
    text = str(text)
    text = self.nlp(text)
    return str(text)
