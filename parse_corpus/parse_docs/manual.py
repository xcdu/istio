#!/usr/bin/env python
# -*- coding: utf-8 -*-
from parse_corpus.parse_docs.page_parser import IstioPageParser


class IstioManual(object):
    def __init__(self, pages=None):
        self.pages = pages
        self.manual = None
        self.adjacency = None
        self.indexer_to_id = None

        self.terms = None

    def build(self, pages=None, page_parser=None):
        if pages is not None:
            self.pages = pages

        self.__reindex_pages()

        if not page_parser:
            page_parser = IstioPageParser()

        if not self.indexer_to_id:
            self.indexer_to_id = dict()

        for i, page in enumerate(self.pages):
            page.page_id = i
            self.indexer_to_id[page.page_indexer] = i
            page.build(page_parser=page_parser)

        self.__update_adjacency()
        self.__update_terms()
        self.__construct_manual()

    def __reindex_pages(self):
        if not self.pages:
            return
        self.pages = sorted(self.pages, key=lambda x: x.page_indexer)

    def __update_adjacency(self):
        if not self.adjacency:
            self.adjacency = dict()
        for page in self.pages:
            if page.links:
                for link_id in page.links:
                    for indexer in page.links[link_id].values():
                        if page.page_indexer not in self.adjacency:
                            self.adjacency[page.page_indexer] = set()
                        self.adjacency[page.page_indexer].add(indexer)

    def __construct_manual(self):
        if self.manual is None:
            self.manual = dict()
        for page in self.pages:
            slice_positions = list(sorted(page.slice_pos_topic_dict.keys()))
            for i in range(len(slice_positions) - 1):
                start = i
                end = i + 1 if (i + 1) <= len(slice_positions) else len(slice_positions)
                topic = page.slice_pos_topic_dict[slice_positions[start]]
                contents = list()
                contents_list = page.contents[
                                slice_positions[start]:slice_positions[end]]
                for c in contents_list:
                    contents += c
                if page.page_indexer not in self.manual:
                    self.manual[page.page_indexer] = dict()
                if topic not in self.manual[page.page_indexer]:
                    self.manual[page.page_indexer][topic] = list()
                self.manual[page.page_indexer][topic] += contents

    def __update_terms(self):
        for page in self.pages:
            for pos, link_dict in page.links.items():
                if not self.terms:
                    self.terms = list()
                if not link_dict.keys():
                    continue
                self.terms += list(link_dict.keys())
        self.terms = list(set(self.terms))
