#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy.cmdline

cmd = "scrapy crawl docspider"
scrapy.cmdline.execute(cmd.split())
