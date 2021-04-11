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
import csv
import pandas as pd

class forum(Spider):
    name = 'forum3'
    #start_urls = ['https://discuss.istio.io/t/configuring-cors/7458']
    start_urls = ['https://discuss.istio.io/c/uncategorized/1']


    def parse(self, response):
        links = LinkExtractor(allow=()).extract_links(response)
        for link in links:
            if "//discuss.istio.io/t/" in link.url and (link.url != "https://discuss.istio.io/t/join-the-bi-weekly-istio-community-video-meeting-now-at-10am/7530" or link.url != "https://discuss.istio.io/t/welcome-to-discourse/9"):
                print("pasring page on {}".format(link))
                yield SplashRequest(link.url, args={"wait": "5"},
                                    callback=self.parse_page)
              
        next_page = response.xpath("//div[@role='navigation']/span/b").extract()
        if next_page:
            next_page_link = response.xpath("//div[@role='navigation']/span/b/a/@href").extract_first()
            next_page_link = 'https://discuss.istio.io' + next_page_link
            print("---Now pasing page on {} ---".format(next_page_link))
            yield SplashRequest(url=next_page_link, callback=self.parse)

    def parse_page(self, response):
        url = str(response.url)
        save_path1 = "/home/xiaowang/nlp/demo_test/demo_test/raw_data/forum/post.csv"

        self.logger.info(save_path1)
        save_dir = os.path.abspath(os.path.dirname(save_path1))
        
        if os.path.exists(save_path1):
            with open(save_path1, "r") as lastFile:
                postID = int(list(csv.reader(lastFile))[-1][0]) + 1
        else:
            postID = 0
        
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        title=response.xpath("//title/text()").extract_first()[:-16]
        text = []
        temp = []
        posting = []

        for post in response.xpath("//div[@class='post']"):
            text.append(' '.join(post.xpath("./p/text() | ./p/code/text() | ./p/a/@href | ./ol/li/text() | .//article[@class='onebox-body']/h3/a/@href").extract()))
            temp.append(' '.join(post.xpath("./pre/code/text()").extract()))
            posting.append(' '.join(post.xpath("./p/text() | ./p/code/text() | ./p/a/@href | ./ol/li/text() | ./pre/code/text() | .//article[@class='onebox-body']/h3/a/@href").extract()))
     
        numPost=len(text)
        seqid = []
        headline = []
        category = []
        postid = []
        for i in range(len(text)):
            postid.append(str(postID))
            seqid.append(i)
            headline.append(title)
            #category.append(title.rsplit('-', 1)[-1])
            category.append('General')


        #firstRow= ['ID', 'SeqID','Title', 'Category', 'Raw Text', 'Template', 'comment']
        rows = zip (postid, seqid, headline, category, text, temp, posting)
        with open(save_path1, 'a') as f_object:
            writer_object = writer(f_object)
            #writer_object.writerow(firstRow) 
            for row in rows:
                writer_object.writerow(row) 
            f_object.close() 


