#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
from default_config import RAW_ISTIO_DIR
from prepare_data.docs.page import IstioPage
from prepare_data.docs.page_parser import IstioPageParser

istio_dir = RAW_ISTIO_DIR
in_file_name = "docs$tasks$traffic-management$fault-injection"
in_file_path = os.path.join(istio_dir, in_file_name)
in_file = open(in_file_path, "r", encoding="utf-8")
item = json.load(in_file)
in_file.close()

page = IstioPage()
page.load_from_dict(item)
page_parser = IstioPageParser()
print("index page: {}".format(page_parser.is_index_page(page)))
page.build(page_parser=page_parser)
print(f"page links: {page.links}")
print(page.to_json())
