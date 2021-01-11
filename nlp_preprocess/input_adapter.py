#!/usr/bin/env python
# -*- coding: utf-8 -*-


class IstioManualInputAdaptor(object):
  def format(self, in_data):
    pass

  def multilevel_format(self, in_data):
    max_level = 0
    for page_indexer in in_data.keys():
      level_depth = len(page_indexer.split("$")) - 1
      max_level = max(level_depth, max_level)

    # init return
    hierarchy_data = dict({"topic": {}, "indexer": {}})
    for i in range(max_level):
      hierarchy_data[i + 1] = dict()

    for page_indexer, topic_contents in in_data.items():
      if page_indexer not in hierarchy_data["indexer"]:
        hierarchy_data["indexer"][page_indexer] = list()

      for topic, contents in topic_contents.items():
        if topic not in hierarchy_data["topic"]:
          hierarchy_data["topic"][topic] = list()
        # topic level
        hierarchy_data["topic"][topic] += contents
        # page_indexer level
        hierarchy_data["indexer"][page_indexer] += contents

      indexer_seq = page_indexer.split("$")
      level_depth = len(indexer_seq) - 1
      if level_depth < 1:
        continue
      for i in range(level_depth):
        label = "$".join(indexer_seq[1: i + 2])
        if label not in hierarchy_data[i + 1]:

          hierarchy_data[i + 1][label] = list()
        for topic, contents in topic_contents.items():
          hierarchy_data[i + 1][label] += contents

    return hierarchy_data


class RawInputAdapter(object):
  def format(self, in_dat):
    # TODO(xcdu)
    pass
