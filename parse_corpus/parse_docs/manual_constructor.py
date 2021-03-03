#!/usr/bin/env python
# -*- coding: utf-8 -*-
from parse_corpus.parse_docs.manual import IstioManual
from parse_corpus.parse_docs.page_parser import IstioPageParser


class IstioManualConstructor(object):
    def build(self, manual: IstioManual, pages=None, page_parser=None):
        if pages is not None:
            manual.pages = pages

        self.reindex_pages(manual)

        if not page_parser:
            page_parser = IstioPageParser()

        if not manual.indexer_to_id:
            manual.indexer_to_id = dict()

        for i, page in enumerate(manual.pages):
            page.page_id = i
            manual.indexer_to_id[page.page_indexer] = i
            page.build(page_parser=page_parser)

        self.construct_corpus(manual)
        self.update_adjacency(manual)
        self.update_terms(manual)

    @staticmethod
    def reindex_pages(manual: IstioManual):
        if not manual.pages:
            return
        manual.pages = sorted(manual.pages, key=lambda x: x.page_indexer)

    @staticmethod
    def update_adjacency(manual: IstioManual):
        if not manual.adjacency:
            manual.adjacency = dict()
        for page in manual.pages:
            if page.links:
                for link_id in page.links:
                    for indexer in page.links[link_id].values():
                        if page.page_indexer not in manual.adjacency:
                            manual.adjacency[page.page_indexer] = list()
                        if indexer not in manual.adjacency[page.page_indexer]:
                            manual.adjacency[page.page_indexer].append(indexer)

    @staticmethod
    def construct_corpus(manual: IstioManual):
        if manual.corpus is None:
            manual.corpus = dict()
        for page in manual.pages:
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
                if page.page_indexer not in manual.corpus:
                    manual.corpus[page.page_indexer] = dict()
                if topic not in manual.corpus[page.page_indexer]:
                    manual.corpus[page.page_indexer][topic] = list()
                manual.corpus[page.page_indexer][topic] += contents

    @staticmethod
    def update_terms(manual: IstioManual):
        for page in manual.pages:
            for pos, link_dict in page.links.items():
                if not manual.terms:
                    manual.terms = list()
                if not link_dict.keys():
                    continue
                manual.terms += list(link_dict.keys())
        manual.terms = list(set(manual.terms))
