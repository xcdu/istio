#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from modules.nlp_preprocess.preprocessor import PipelinePreprocessor


class IstioManualInputAdaptor(object):
  def format(self, in_data):
    pass

  @staticmethod
  def multilevel_format(in_data):
    """
    Convert manual into specific format:

    dict:
      "topic":    # split by detailed topic
        "${indexer}": "text"
        "${indexer}": "text"
        ...

      "indexer":  # split in indexer level
        "${indexer}": "text"
        "${indexer}": "text"
        ...

      1:          # split by the first substring of index
        "${indexer}": "text"
        "${indexer}": "text"
        ...

      2:          # split by the second substring of index
        "${indexer}": "text"
        "${indexer}": "text"
        ...
      ...

    :param in_data:
    :return:
    """
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


class SklearnInputAdapter(object):
  @staticmethod
  def format(in_data, fast_test=False):
    preprocessor = PipelinePreprocessor()
    # TODO(xcdu) added features here

    preprocessor.set_features([])
    data = preprocessor.process(in_data=in_data)
    texts = list()
    labels = list()
    for indexer, contents in data.items():
      for content in contents:
        texts.append(content)
        labels.append(indexer)
    df = pd.DataFrame()
    df["text"] = texts
    df["label"] = labels

    return df


class NeuralNetworkInputAdapter(object):
  def format(self, text):
    pass


class RawInputAdapter(object):
  def format(self, in_data):
    # TODO(xcdu)
    pass
