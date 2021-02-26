#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd


class IstioForumCorpus(object):
    def __init__(self, raw_forum_corpus: pd.DataFrame):
        self.raw = raw_forum_corpus
        self.comments = None

    def build(self):
        self.format_comments()
        return

    def format_comments(self):
        pass


if __name__ == '__main__':
    from forum_helper import load_forum_corpus_from_dir

    forum_corpus = IstioForumCorpus(load_forum_corpus_from_dir())
    cnt_dict = dict()
    test_tag = "category"
    for i, row in forum_corpus.raw.iterrows():
        if row[test_tag] not in cnt_dict:
            cnt_dict[row[test_tag]] = 0
        cnt_dict[row[test_tag]] += 1
    for key, value in cnt_dict.items():
        print(key, value)
