import re
import os
from scrapy import Spider
#from crawldocs.items import CrawldocsItem
from scrapy_splash import SplashRequest

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor


class DocspiderSpider(Spider):
  name = 'docspider'
  allowed_domains = ['istio.io']
  start_urls = ['https://istio.io/latest/docs']

  def parse(self, response):
    links = LinkExtractor(allow=()).extract_links(response)
    for link in links:
      if "//istio.io/latest/docs" in link.url:
        yield SplashRequest(link.url, args={"wait": "5"},
                            callback=self.parse_page)

  def parse(self, response):
    url = str(response.url)
    pattern = re.compile("([-\w]+)")
    filename = pattern.findall(url[len(self.start_urls[0]):])
    save_path = "../raw_data/docs/" + ".".join(filename)
    self.logger.info(save_path)
    save_dir = os.path.abspath(os.path.dirname(save_path))
    if not os.path.exists(save_dir):
      os.makedirs(save_dir)

    texts = response.xpath("//p/text()").extract()
    #print(texts)
    save_file = open(save_path, "w", encoding="utf-8")
    self.logger.info(texts)
    for i in texts:
      save_file.write(i + "\n")
    save_file.close()