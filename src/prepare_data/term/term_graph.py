#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO(xcdu): finish the term graph

class TermNode(object):
    def __init__(self):
        self.term = None
        self.page_id = None
        self.next = None


class TermGraph(object):
    def __init__(self):
        self.adjacency_heads = list()

    def add_node(self, term_node):
        pass

    def del_node(self, idx):
        pass
