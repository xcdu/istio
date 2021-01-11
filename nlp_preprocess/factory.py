#!/usr/bin/env python
# -*- coding: utf-8 -*-
import spacy


class ConcreteBase(object):
  def concrete(self):
    return


class ConcreteSpacy(ConcreteBase):
  def concrete(self):
    return spacy.load("en_core_web_sm")


class ModuleFactory(object):
  def __init__(self):
    self.__factories = {
      "spacy": ConcreteSpacy
    }

  def get_module(self, module_type: str):
    if module_type not in self.__factories:
      raise TypeError("No suitable type found in {}".format(type(self)))
    else:
      return self.__factories[module_type]().concrete()


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

