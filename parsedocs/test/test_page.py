#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from parsedocs.page import IstioPage

path = "../../.data/docs$concepts"
in_file = open(path, "r", encoding="utf-8")
item = json.load(in_file)
in_file.close()

page = IstioPage()
page.load_from_dict(item)
print(page.to_json())
