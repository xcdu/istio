#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parse_corpus.parse_docs.manual import IstioManual
from parse_corpus.parse_docs.manual_constructor import IstioManualConstructor

from parse_corpus.parse_docs.docs_helper import load_pages_from_dir
from components.nlp_preprocess.input_adapter import IstioManualInputAdaptor
from components.nlp_preprocess.preprocessor import PipelinePreprocessor
from components.nlp_preprocess.feature import SpacyFeature
from components.nlp_preprocess.feature import BertFeature

from default_config import RAW_ISTIO_DIR


in_path = RAW_ISTIO_DIR

raw_pages = load_pages_from_dir(in_path)

manual = IstioManual()
manual_constructor = IstioManualConstructor()
manual.build(pages=raw_pages, manual_constructor=manual_constructor)

input_adapter = IstioManualInputAdaptor()
data = input_adapter.multilevel_format(manual.corpus)

preprocessor = PipelinePreprocessor()
preprocessor.set_features([SpacyFeature, BertFeature])
data = preprocessor.process(in_data=data["indexer"])
print(data)
