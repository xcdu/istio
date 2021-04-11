#!/usr/bin/env python
# -*- coding: utf-8 -*-
from prepare_data.forum.forum_helper import load_forum_corpus_from_dir
from preprocess_corpus.preprocess_forum import format_forum

forum_df = load_forum_corpus_from_dir()
format_forum(forum_df)
