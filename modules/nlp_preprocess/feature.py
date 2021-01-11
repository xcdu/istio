#!/usr/bin/env python
# -*- coding: utf-8 -*-
from factory import Modules


class BaseFeature(object):
  def apply(self, texts: list):
    return texts


class SpacyFeature(BaseFeature):
  def __init__(self):
    self.nlp = Modules().get("spacy")

  def apply(self, texts: list):
    texts = " ".join(texts)
    texts = self.nlp(texts)
    formatted_texts = []
    for sentence in texts.sents:
      formatted_sentence = []
      for token in sentence:
        if token.is_punct or token.like_url or token.like_email:
          continue
        formatted_sentence.append(token.lemma_)
      formatted_sentence = " ".join(
        [w for w in formatted_sentence if w != "\n"])
      if formatted_sentence.strip():
        formatted_texts.append(formatted_sentence.strip())
    return formatted_texts


class RuleFeature(object):
  def apply(self, texts: list):
    return texts


class RegexFeature(object):
  def apply(self, texts: list):
    return texts


class BertFeature(BaseFeature):
  def __init__(self):
    self.bert = Modules().get("bert")

  def apply(self, texts: list):
    for i in range(len(texts)):
      texts[i] = " ".join([token for token in self.bert.tokenize(texts[i])])
    return texts
