#!/usr/bin/env python
# -*- coding: utf-8 -*-


class IstioForumComment(object):
    def __init__(self,
                 comment_id=None,
                 comment_seq_id=None,
                 raw_text=None,
                 template=None,
                 category=None,
                 annotation=None,
                 annotated_terms=None):
        self.comment_id = comment_id
        self.comment_seq_id = comment_seq_id
        self.raw_text = raw_text
        self.template = template
        self.category = category
        self.annotation = annotation
        self.annotated_terms = annotated_terms
