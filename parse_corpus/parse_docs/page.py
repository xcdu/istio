#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


class IstioPage(object):
  def __init__(self):
    """
    contents: It is a list storing sliced text.
    """
    # Meta information
    self.url = str()
    self.title = str()
    self.page_indexer = str()
    self.page_id = str()
    self.raw = str()
    self.headline = str()

    # Structured information
    self.contents = None
    self.slice_pos_topic_dict = None
    self.links = None
    self.templates = None

  def build(self, page_parser):
    # analyze and parse contents
    page_parser.parse(self)

  def load_from_dict(self, item):
    for key in item.keys():
      setattr(self, key, item[key])
    return self

  def to_json(self, indent=4):
    return json.dumps(self.__dict__, indent=indent)

