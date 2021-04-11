#!/usr/bin/env python
# -*- coding: utf-8 -*-
from prepare_data.template.template_parser import IstioTemplateFuzzyParser
import yaml


def prepare_page_content_and_related_templates_from_manual(manual):
    indexer_level_corpus = construct_indexer_level_corpus(manual)
    page_template_dict = extract_templates(manual)
    return indexer_level_corpus, page_template_dict


def construct_indexer_level_corpus(manual):
    corpus = vars(manual.corpus)
    indexer_level_corpus = dict()
    for page_indexer, contents in corpus.items():
        content_dict = vars(contents)
        if page_indexer not in indexer_level_corpus:
            indexer_level_corpus[page_indexer] = dict()
        for content_title, content_context in content_dict.items():
            if content_title not in indexer_level_corpus[page_indexer]:
                indexer_level_corpus[page_indexer][content_title] = list()
            indexer_level_corpus[page_indexer][content_title].append(content_context)
    return indexer_level_corpus


def extract_templates(manual):
    pages = manual.pages
    parser = IstioTemplateFuzzyParser()

    page_template_dict = dict()
    for page in pages:
        template_pos_dict = vars(page.templates)
        if not template_pos_dict:
            continue
        templates = list()
        for value in template_pos_dict.values():
            templates = "\n".join(value)
            templates = parser.parse(templates)
        if not templates or len(templates) == 0:
            continue
        templates = [yaml.load(template, Loader=yaml.FullLoader) for template in templates]
        page_template_dict[page.page_indexer] = templates
    return page_template_dict
