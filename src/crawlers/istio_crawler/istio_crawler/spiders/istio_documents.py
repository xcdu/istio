import scrapy
from scrapy_splash import SplashRequest
import re
from scrapy.linkextractors import LinkExtractor
from crawlers.istio_crawler.istio_crawler.items import IstioCrawlerItem


class IstioDocumentsSpider(scrapy.Spider):
    name = 'istio_documents'
    allowed_domains = ['istio.io']
    docs_prefix = "https://istio.io/latest"
    docs_url = "https://istio.io/latest/docs"
    start_urls = [docs_url]
    parse_start_url = False

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 '
                      'Safari/537.36',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # 'Accept-Language': 'en',
        # "Accept-Encoding": "gzip, deflate",
        # 'Content-Length': '0',
        # "Connection": "keep-alive"
    }

    def parse(self, response):
        if not self.parse_start_url:
            self.parse_start_url = True
            yield SplashRequest(response.url, args={"wait": "5"},
                                headers=self.headers,
                                callback=self.parse_page)
        links = LinkExtractor(allow=()).extract_links(response)
        for link in links:
            if self.docs_url in link.url:
                yield SplashRequest(link.url, args={"wait": "5"},
                                    headers=self.headers,
                                    callback=self.parse_page)

    def parse_page(self, response):
        item = IstioCrawlerItem()
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
        raw = response.body.decode("utf-8")
        item["raw"] = raw
        # self.logger.debug("raw:{}".format(raw))

        # parse header
        headline = response.xpath("//*[@id='title']/text()").get()
        item['headline'] = headline
        # self.logger.debug("headline:{}".format(headline))
        return item

#
