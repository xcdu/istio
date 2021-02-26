#!/usr/bin/env python
# -*- coding: utf-8 -*-
from parse.parse_docs.manual import IstioManual

from parse.parse_docs.docs_helper import load_pages_from_dir
from parse.parse_docs.docs_helper import save_manual
from default_configs import RAW_ISTIO_DIR

in_path = RAW_ISTIO_DIR

raw_pages = load_pages_from_dir(in_path)

manual = IstioManual()
manual.build(pages=raw_pages)
save_manual(manual)
