#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from lxml import etree
import logging


class IstioPageParser(object):
  def __init__(self):
    pass

  def parse(self, page):
    if self._is_index_page(page):
      self._parse_index_page(page)
    else:
      self._parse_intro_page(page)

  def _is_index_page(self, page):
    selector = etree.HTML(page.content)
    has_section_index = selector.xpath("boolean(//*[@class='section-index'])")
    return has_section_index

  def _slice_intro_page(self, page):
    sliced_body = None
    return sliced_body

  def _parse_index_page(self, page):
    self._slice_intro_page(page)
    return

  def _parse_intro_page(self, page):
    return
