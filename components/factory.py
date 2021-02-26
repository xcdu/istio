#!/usr/bin/env python
# -*- coding: utf-8 -*-
import spacy
import os
import keras_bert
import codecs
from modules.embedding.embedding_model import BertEmbeddingModel
from pathlib import Path


class ConcreteBase(object):
  def concrete(self):
    return


class ConcreteSpacy(ConcreteBase):
  def concrete(self):
    return spacy.load("en_core_web_sm")


class ConcreteBertEmbeddingModel(ConcreteBase):
  def concrete(self):
    bert_model_path = os.path.join(Path(__file__).parent.absolute(),
                                   "../.bert/uncased_L-12_H-768_A-12/")
    return BertEmbeddingModel(bert_model_path)


class ModuleFactory(object):
  def __init__(self):
    self.__factories = {
      "spacy": ConcreteSpacy,
      ".bert": ConcreteBertEmbeddingModel
    }

  def get_module(self, module_type: str):
    if module_type not in self.__factories:
      raise TypeError("No suitable type found in {}".format(type(self)))
    else:
      return self.__factories[module_type]().concrete()


def singleton(cls):
  _instance = {}

  def inner():
    if cls not in _instance:
      _instance[cls] = cls()
    return _instance[cls]

  return inner


@singleton
class Modules(object):
  def __init__(self):
    self.__objs = dict()
    self.__factory = ModuleFactory()

  def get_keys(self):
    return self.__objs.keys()

  def get(self, key):
    if key not in self.__objs:
      self.__objs[key] = self.__factory.get_module(key)
    return self.__objs[key]
