import re
import os
from scrapy import Spider
from crawldocs.items import CrawldocsItem
from scrapy_splash import SplashRequest

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
import logging


class DocspiderSpider(Spider):
  name = 'docspider'
  allowed_domains = ['istio.io']
  docs_prefix = "https://istio.io/latest"
  docs_url = "https://istio.io/latest/docs"
  start_urls = [docs_url]
  parse_start_url = False

  # save_path = "./.rawdata"

  def parse(self, response):
    if not self.parse_start_url:
      self.parse_start_url = True
      yield SplashRequest(response.url, args={"wait": "5"},
                          callback=self.parse_page)
    links = LinkExtractor(allow=()).extract_links(response)
    for link in links:
      if self.docs_url in link.url:
        yield SplashRequest(link.url, args={"wait": "5"},
                            callback=self.parse_page)

  def parse_page(self, response):
    item = CrawldocsItem()
    # parse url
    url = str(response.url)
    item["url"] = url
    # self.logger.debug("url:{}".format(url))

    # parse title
    title = response.xpath("//title/text()").get()
    item["title"] = title
    # self.logger.debug("title:{}".format(title))

    # parse page indexer
    pattern = re.compile("([-\w]+)")
    sub_urls = pattern.findall(url[len(self.docs_prefix):])
    page_indexer = "$".join(sub_urls)
    item["page_indexer"] = page_indexer
    # self.logger.debug("page_indexer:{}".format(page_indexer))

    # parse body
    body = response.body.decode("utf-8")
    item["body"] = body
    # self.logger.debug("raw:{}".format(raw))

    # parse header
    headline = response.xpath("//*[@id='title']/text()").get()
    item['headline'] = headline
    # self.logger.debug("headline:{}".format(headline))
    return item

#
