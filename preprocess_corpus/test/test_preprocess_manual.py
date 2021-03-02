#!/usr/bin/env python
# -*- coding: utf-8 -*-
from parse_corpus.parse_docs.docs_helper import load_manual
from preprocess_manual import prepare_page_content_and_related_templates_from_manual

manual = load_manual()
prepare_page_content_and_related_templates_from_manual(manual)
