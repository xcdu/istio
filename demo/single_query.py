#!/usr/bin/env python
# -*- coding: utf-8 -*-
from parsedocs.data_helper import load_raw_from_dir
from parsedocs.graph import IstioGraph

input_query = "How to start the application services"

tfidfmodel = None

model = tfidfmodel

output = model.query()

print(output)
