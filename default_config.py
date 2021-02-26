#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib
import os

# Project root directory path
PROJECT_ROOT = pathlib.Path(__file__).parent.absolute()

# Folder for raw data
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, ".raw_data")

# Sub-folder for raw istio documentations
RAW_ISTIO_DIR = os.path.join(RAW_DATA_DIR, "istio_docs")

# Sub-folder for raw forum corpus
RAW_FORUM_DIR = os.path.join(RAW_DATA_DIR, "forum")

# Folder to save processed data
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, ".processed_data")

# Sub-folder to save parsed docs in processed data folder
PARSED_DOCS_DIR = os.path.join(PROCESSED_DATA_DIR, "parsed_docs")
