#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy.cmdline

cmd = "scrapy crawl istio_documents"
scrapy.cmdline.execute(cmd.split())
