#!/usr/bin/env python
# -*- coding: utf-8 -*-
from manual import IstioManual

from parsedocs.data_helper import load_pages_from_dir

in_path = "../../.data"

raw_pages = load_pages_from_dir(in_path)

manual = IstioManual()
manual.build(pages=raw_pages)
