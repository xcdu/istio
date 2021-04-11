#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from types import SimpleNamespace


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
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=indent)

    def from_json(self, json_data):
        json_obj = json.loads(json_data, object_hook=lambda d: SimpleNamespace(**d))
        return self.from_namespace(json_obj)

    def from_namespace(self, obj):
        self.url = obj.url
        self.title = obj.title
        self.page_indexer = obj.page_indexer
        self.page_id = obj.page_id
        self.raw = obj.raw
        self.headline = obj.headline
        self.contents = obj.contents
        self.slice_pos_topic_dict = obj.slice_pos_topic_dict
        self.links = obj.links
        self.templates = obj.templates
        return self
