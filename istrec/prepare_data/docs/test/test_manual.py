#!/usr/bin/env python
# -*- coding: utf-8 -*-
from default_config import RAW_ISTIO_DIR
from prepare_data.docs.manual import IstioManual
from prepare_data.docs.manual_constructor import IstioManualConstructor
from prepare_data.docs.manual_helper import load_pages_from_dir

in_path = RAW_ISTIO_DIR

raw_pages = load_pages_from_dir(in_path)

manual = IstioManual()
manual_constructor = IstioManualConstructor()
manual.build(manual_constructor=manual_constructor, pages=raw_pages)
