#import scrapy
import os
from scrapy import Spider
from scrapy_splash import SplashRequest
import re
import numpy
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from csv import writer 

class forum(Spider):
    name = 'forum4'
    #start_urls = ['https://istio.io/latest/docs/concepts/']
    #start_urls = ['https://discuss.istio.io/t/forward-source-ip-of-https-request/6246']
    start_urls = ['https://discuss.istio.io/c/security/12']
    #start_urls = ['https://discuss.istio.io/']
    
    def parse(self, response):
        post = []
        views = []
        title=response.xpath("//meta[@itemprop='name']/@content").extract()
        reply=response.xpath("//span[@class='posts']/text()").extract()
        view=response.xpath("//span[@class='views']/text()").extract()      
        #print("title:{}, replies:{}, views:{}".format(title, replies, views))
        save_path1 = "../raw_data/forum/reply-view.csv"
        with open(save_path1, 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerows(zip(title,reply,view)) 
            f_object.close() 
              
        next_page = response.xpath("//div[@role='navigation']/span/b").extract()
        if next_page:
            next_page_link = response.xpath("//div[@role='navigation']/span/b/a/@href").extract_first()
            next_page_link = 'https://discuss.istio.io' + next_page_link
            print("---Now pasing page on {} ---".format(next_page_link))
            yield SplashRequest(url=next_page_link, callback=self.parse)
    '''        
    def parse(self, response):
        parse_page(start_urls)
        #print("***show links {}".format(links))
        

        next_page = response.xpath("//div[@role='navigation']/span/b").extract()
    
        
        if next_page:
            next_page_link = response.xpath("//div[@role='navigation']/span/b/a/@href").extract_first()
            next_page_link = 'https://discuss.istio.io' + next_page_link
            print("---Now pasing page on {} ---".format(next_page_link))
            parse(next_page_link)
        '''




