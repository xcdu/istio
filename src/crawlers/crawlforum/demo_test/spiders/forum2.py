#this file to collect metadata
import os
import scrapy
from scrapy import Spider
from scrapy_splash import SplashRequest
import re, json
import numpy
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

class forum(Spider):
    name = 'forum2'
    start_urls = ['https://discuss.istio.io/t/how-to-connect-namespaces-over-ingress-egress-gateways-only/2298']
    #start_urls = ['https://discuss.istio.io/']

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua": "'Google Chrome';v='87', ' Not;A Brand';v='99', 'Chromium';v='87'",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "same-origin",
        "sec-fetch-site": "same-origin",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    }

    def parse(self, response):
        url = 'https://discuss.istio.io/t/how-to-connect-namespaces-over-ingress-egress-gateways-only/2298'
        
        yield scrapy.Request(url, callback=self.parse_api, headers=self.headers)

    def parse_api(self, response):
        #raw_data = response.body
        save_path1 = "../raw_data/forum/forum2"
        #print(save_path1)
        self.logger.info(save_path1)
        save_dir = os.path.abspath(os.path.dirname(save_path1))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        texts = response.xpath("//div[@id='data-preloaded']/@data-preloaded").extract_first()
        #texts = response.xpath("//p/text()").extract()
        data = json.loads(texts)
        print(json.dumps(data, indent=4, sort_keys=True))


    '''
        save_file = open(save_path1, "w", encoding="utf-8")
        for i in texts:
            save_file.write(value + "\n")
        save_file.close()
'''



