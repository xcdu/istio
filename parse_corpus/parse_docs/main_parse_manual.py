#!/usr/bin/env python
# -*- coding: utf-8 -*-
from parse_corpus.parse_docs.manual import IstioManual

from parse_corpus.parse_docs.docs_helper import load_pages_from_dir
from parse_corpus.parse_docs.docs_helper import load_manual
from parse_corpus.parse_docs.docs_helper import save_manual
from parse_corpus.parse_docs.docs_helper import save_terms
from default_config import RAW_ISTIO_DIR
from parse_corpus.parse_docs.manual_constructor import IstioManualConstructor

in_path = RAW_ISTIO_DIR

raw_pages = load_pages_from_dir(in_path)

manual = IstioManual()
manual_constructor = IstioManualConstructor()
manual.build(manual_constructor=manual_constructor, pages=raw_pages)
save_manual(manual)
save_terms(manual)
manual = load_manual()
for page in manual.pages:
    print(type(page))
    print(page.to_json())
