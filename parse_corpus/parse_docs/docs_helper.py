#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import codecs
from manual import IstioManual
from page import IstioPage
from default_configs import RAW_ISTIO_DIR, PARSED_DOCS_DIR


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
    return page_list


def save_adjacency(
        manual: IstioManual,
        dir_path=PARSED_DOCS_DIR,
        file_name="adjacency.json"):
    # TODO(xcdu): fix serialization
    save_file_path = os.path.join(dir_path, file_name)
    with codecs.open(save_file_path, "w", encoding="utf-8") as save_file:
        json.dump(manual.adjacency, save_file)


def save_terms(
        manual: IstioManual,
        dir_path=PARSED_DOCS_DIR,
        file_name="terms.txt"):
    save_file_path = os.path.join(dir_path, file_name)
    with codecs.open(save_file_path, "w", encoding="utf-8") as save_file:
        save_file.writelines([term + "\n" for term in manual.terms])


def save_term_relationship(
        manual,
        dir_path=PARSED_DOCS_DIR,
        file_name="term_relationship.txt"):
    # TODO(xcdu): will finish this function when it is in use
    pass


def save_parsed_manual(
        manual,
        dir_path=PARSED_DOCS_DIR,
        file_name="manual.json"):
    save_file_path = os.path.join(dir_path, file_name)
    with codecs.open(save_file_path, "w", encoding="utf-8") as save_file:
        json.dump(manual.manual, save_file)
    return


def save_manual(manual, dir_path=PARSED_DOCS_DIR):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    save_parsed_manual(manual, dir_path=dir_path)
    # save_adjacency(manual, dir_path=dir_path)
    save_terms(manual, dir_path=dir_path)
    # save_term_relationship(manual, dir_path=dir_path)
    return
