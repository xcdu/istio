#!/usr/bin/env python
# -*- coding: utf-8 -*-

def test_fuzzy_parser():
    import os
    import numpy as np
    from parse_corpus.parse_template.template_helper import load_templates_from_file
    from parse_corpus.parse_forum.forum_helper import load_forum_corpus_from_dir
    from parse_corpus.parse_template.template_parser import IstioTemplateFuzzyParser

    raw_forum_df = load_forum_corpus_from_dir()
    fuzzy_parser = IstioTemplateFuzzyParser()
    for index, row in raw_forum_df.iterrows():
        if row["template"] != np.nan:
            templates = str(row["template"])
            templates = fuzzy_parser.parse(templates)
            for t in templates:
                print(t)


if __name__ == '__main__':
    test_fuzzy_parser()
