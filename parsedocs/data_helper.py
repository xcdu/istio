#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from page import IstioPage


def load_pages_from_dir(dir_path):
  page_list = list()
  for root, _, filenames in os.walk(dir_path):
    for filename in filenames:
      in_file_path = os.path.join(root, filename)
      in_file = open(in_file_path, "r", encoding="utf-8")
      item = json.load(in_file)
      in_file.close()
      page = IstioPage()
      page_list.append(page.load_from_dict(item))
  return page_list
