#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy.cmdline

cmd = "scrapy crawl testspider"
scrapy.cmdline.execute(cmd.split())