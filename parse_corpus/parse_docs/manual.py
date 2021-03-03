#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from types import SimpleNamespace
from parse_corpus.parse_docs.page import IstioPage


class IstioManual(object):
    def __init__(self, pages=None):
        self.pages = pages
        self.indexer_to_id = None

        self.corpus = None
        self.adjacency = None
        self.terms = None

    def build(self, manual_constructor, pages=None, page_parser=None):
        manual_constructor.build(self, pages, page_parser)

    def to_json(self, indent=4):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=indent)

    def from_json(self, json_data):
        json_obj = json.loads(json_data, object_hook=lambda d: SimpleNamespace(**d))
        self.indexer_to_id = json_obj.indexer_to_id
        self.corpus = json_obj.corpus
        self.adjacency = json_obj.adjacency
        self.terms = json_obj.terms
        self.pages = list()
        for i in range(len(json_obj.pages)):
            page = IstioPage().from_namespace(json_obj.pages[i])
            self.pages.append(page)
        return self
