#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml

path = "app.yaml"

in_file = open(path, "r",encoding="utf-8")

for token in yaml.scan(in_file):
    print(token)
