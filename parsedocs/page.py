#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


class IstioPage(object):
  def __init__(self):
    self.url = str()
    self.title = str()
    self.page_indexer = str()
    self.page_id = str()
    self.content = str()
    self.headline = str()

    """
    Each page has multiple slices of contents, which have an sequential index 
    numbers from 1 to len(content_dict).
    The indexer 0 is the root of the current page.
    'content_dict' is a list storing sliced page texts in sequence.
    'adjacency' is a dict storing mapping from a string number to a sequence of 
    string number, such as '1' to ' 2 3 4', which means the content 1 has sub 
    nodes of 2, 3, and 4. It maintains the hierarchy of the page.
    'next_links' is a dict storing mapping from indexer number to actual links.
    'templates_hierarchy' is a dict storing mapping from indexer number to the
    content of template.

    The reason why we use string number as key and sequential string number as 
    value is because of the compatibility of serialization.
    """
    self.content_list = list()
    self.adjacency = dict()
    self.next_links = dict()
    self.templates_hierarchy = dict()

  def parse_content(self):
    pass

  def load_from_json(self, json_string):
    pass

  def load_from_dict(self, item):
    for key in item.keys():
      setattr(self, key, item[key])

  def to_json(self, indent=4):
    return json.dumps(self.__dict__, indent=indent)


