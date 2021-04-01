#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib
import os

# Project root directory path
PROJECT_ROOT = pathlib.Path(__file__).parent.absolute()

# Data root directory path
DATA_ROOT = os.path.join(PROJECT_ROOT, ".data")

# DATA
# Folder for raw data
RAW_DATA_DIR = os.path.join(DATA_ROOT, ".raw_data")

# Sub-folder for raw istio documentations
RAW_ISTIO_DIR = os.path.join(RAW_DATA_DIR, "istio_docs")

# Sub-folder for raw forum corpus
RAW_FORUM_DIR = os.path.join(RAW_DATA_DIR, "forum")

# Folder to save processed data
PROCESSED_DATA_DIR = os.path.join(DATA_ROOT, ".data/.processed_data")

# Sub-folder to save parsed docs in processed data folder
PARSED_DOCS_DIR = os.path.join(PROCESSED_DATA_DIR, "parsed_docs")

# Sub-folder to save pre-processed and formatted corpus and template for models
PREPROCESSED_CORPUS_FORUM_DIR = os.path.join(PROCESSED_DATA_DIR, "preprocessed_corpus_and_forum")

# BERT
BERT_PRE_TRAINED_MODEL_DIR = os.path.join(DATA_ROOT, ".bert/uncased_L-12_H-768_A-12")
