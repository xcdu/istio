#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import codecs
from prepare_data.docs.manual import IstioManual
from prepare_data.docs.page import IstioPage
from default_config import RAW_ISTIO_DIR, PARSED_DOCS_DIR


def load_pages_from_dir(dir_path=RAW_ISTIO_DIR):
    page_list = list()
    for root, _, filenames in os.walk(dir_path):
        for filename in filenames:
            in_file_path = os.path.join(root, filename)
            in_file = codecs.open(in_file_path, "r", encoding="utf-8")
            item = json.load(in_file)
            in_file.close()
            page = IstioPage()
            page_list.append(page.load_from_dict(item))
    if not page_list or len(page_list) == 0:
        raise RuntimeError(f"No pages found in directory {dir_path}")
    return page_list


def save_terms(manual: IstioManual, dir_path=PARSED_DOCS_DIR, filename="terms.txt"):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    save_path = os.path.join(dir_path, filename)
    with codecs.open(save_path, "w", encoding="utf-8") as save_file:
        for term in manual.terms:
            save_file.write(term + "\n")


def save_manual(manual: IstioManual, dir_path=PARSED_DOCS_DIR, filename="manual.json"):
    save_path = os.path.join(dir_path, filename)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with codecs.open(save_path, "w", encoding="utf-8") as save_file:
        save_file.write(manual.to_json())


def load_manual(dir_path=PARSED_DOCS_DIR, filename="manual.json") -> IstioManual:
    load_path = os.path.join(dir_path, filename)
    with codecs.open(load_path, "r", encoding="utf-8") as load_file:
        content = load_file.read()
    manual = IstioManual()
    return manual.from_json(content)
