import re
import os
from scrapy import Spider
from crawldocs.items import CrawldocsItem
from scrapy_splash import SplashRequest

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
import logging


class TestspiderSpider(Spider):
  name = 'testspider'
  allowed_domains = ['istio.io']
  docs_url = "https://istio.io/latest/docs"
  start_urls = [docs_url]

  def parse(self, response):
    links = LinkExtractor(allow=()).extract_links(response)
    for link in links:
      if self.docs_url in link.url:
        yield SplashRequest(link.url, args={"wait": "5"},
                            callback=self.parse_page)

  def parse_page(self, response):
    has_section_index = response.xpath("boolean(//*[@class='section-index'])").get()
    self.logger.info("url:{} has:{}".format(response.url, has_section_index))





#