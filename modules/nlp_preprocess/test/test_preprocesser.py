#!/usr/bin/env python
# -*- coding: utf-8 -*-

from manual import IstioManual

from parsedocs.data_helper import load_pages_from_dir
from modules.nlp_preprocess.input_adapter import IstioManualInputAdaptor
from modules.nlp_preprocess.preprocessor import PipelinePreprocessor
from modules.nlp_preprocess.feature import SpacyFeature
from modules.nlp_preprocess.feature import BertFeature

in_path = "../../../.data"

raw_pages = load_pages_from_dir(in_path)

manual = IstioManual()
manual.build(pages=raw_pages)

input_adapter = IstioManualInputAdaptor()
data = input_adapter.multilevel_format(manual.manual)

preprocessor = PipelinePreprocessor()
preprocessor.set_features([SpacyFeature, BertFeature])
data = preprocessor.process(in_data=data["indexer"])