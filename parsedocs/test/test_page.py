#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from parsedocs.page import IstioPage
from parsedocs.page_parser import IstioPageParser

path = "../../.data/docs$tasks$traffic-management$fault-injection"
in_file = open(path, "r", encoding="utf-8")
item = json.load(in_file)
in_file.close()

page = IstioPage()
page.load_from_dict(item)
page_parser = IstioPageParser()
print("index page: {}".format(page_parser.is_index_page(page)))
page.build(page_parser=page_parser)
print(f"page links: {page.links}")
