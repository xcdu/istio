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
    name = 'forum5'
    start_urls = ['https://discuss.istio.io/t/configuring-cors/7458']
    #start_urls = ['https://discuss.istio.io/c/security/12']

    def parse(self, response):
        url = str(response.url)
        save_path1 = "../raw_data/forum/post.csv"
        #save_path2 = "../raw_data/forum/templateV2.csv"
        #save_path3 = "../raw_data/forum/postV2.csv"
        #print(save_path1)
        self.logger.info(save_path1)
        save_dir = os.path.abspath(os.path.dirname(save_path1))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        #texts = response.xpath("//p/text()").extract()

        title=response.xpath("//title/text()").extract_first()[:-16]
        #text will extract regular text, short coded text, clickable text links, bullet text, box reference.
        #text=response.xpath("//div[@class='post']/p/text() | //div[@class='post']/p/code/text() | //div[@class='post']/p/a/@href | //div[@class='post']/ol/li/text() | //article[@class='onebox-body']/h3/a/@href").extract()
        #temp=response.xpath("//div[@class='post']/pre/code/text()").extract()
        text = []
        #text.append(title)
        temp = []
        #temp.append(title)
        posting = []
        #posting.append(title)

        for post in response.xpath("//div[@class='post']"):
            text.append(' '.join(post.xpath("./p/text() | ./p/code/text() | ./p/a/@href | ./ol/li/text() | .//article[@class='onebox-body']/h3/a/@href").extract()))
            temp.append(' '.join(post.xpath("./pre/code/text()").extract()))
            posting.append(' '.join(post.xpath("./p/text() | ./p/code/text() | ./p/a/@href | ./ol/li/text() | ./pre/code/text() | .//article[@class='onebox-body']/h3/a/@href").extract()))
        print(title.rsplit('-', 1)[-1])
        print(title.rsplit('-', 1)[0])
        print(text)
        print("temp ---**")
        print(temp)
        print("post----**")
        print(posting)
        numPost=len(text)
        seqid = []
        headline = []
        category = []
        for i in range(len(text)):
            seqid.append(i)
            headline.append(title.rsplit('-', 1)[0])
            category.append(title.rsplit('-', 1)[-1])
        print(seqid)
        print(headline)
        print(category)

        firstRow= [ 'SeqID','Title', 'Category', 'Raw Text', 'Template', 'comment']
        rows = zip ( seqid, headline, category, text, temp, posting)
        with open(save_path1, 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(firstRow) 
            for row in rows:
                writer_object.writerow(row) 
            f_object.close() 
        
        

    '''
    def parse(self, response):
        links = LinkExtractor(allow=()).extract_links(response)
        #print("***show links {}".format(links))
        for link in links:
            if "//discuss.istio.io/t/" in link.url and link.url != "https://discuss.istio.io/t/about-the-security-category/25":
                print("pasring page on {}".format(link))
                yield SplashRequest(link.url, args={"wait": "5"},
                                    callback=self.parse_page)
              
        next_page = response.xpath("//div[@role='navigation']/span/b").extract()
        if next_page:
            next_page_link = response.xpath("//div[@role='navigation']/span/b/a/@href").extract_first()
            next_page_link = 'https://discuss.istio.io' + next_page_link
            print("---Now pasing page on {} ---".format(next_page_link))
            yield SplashRequest(url=next_page_link, callback=self.parse)
    '''
    def parse_page(self, response):
        url = str(response.url)
        save_path1 = "../raw_data/forum/post.csv"
        #save_path2 = "../raw_data/forum/templateV2.csv"
        #save_path3 = "../raw_data/forum/postV2.csv"
        #print(save_path1)
        self.logger.info(save_path1)
        save_dir = os.path.abspath(os.path.dirname(save_path1))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        #texts = response.xpath("//p/text()").extract()

        title=response.xpath("//title/text()").extract_first()
        #text will extract regular text, short coded text, clickable text links, bullet text, box reference.
        #text=response.xpath("//div[@class='post']/p/text() | //div[@class='post']/p/code/text() | //div[@class='post']/p/a/@href | //div[@class='post']/ol/li/text() | //article[@class='onebox-body']/h3/a/@href").extract()
        #temp=response.xpath("//div[@class='post']/pre/code/text()").extract()
        text = []
        text.append(title)
        temp = []
        temp.append(title)
        post = []
        post.append(title)

        for post in response.xpath("//div[@class='post']"):
            text.append(' '.join(post.xpath("./p/text() | ./p/code/text() | ./p/a/@href | ./ol/li/text() | .//article[@class='onebox-body']/h3/a/@href").extract()))
            temp.append(' '.join(post.xpath("./pre/code/text()").extract()))
            post.append(' '.join(post.xpath("./p/text() | ./p/code/text() | ./p/a/@href | ./ol/li/text() | ./pre/code/text() | .//article[@class='onebox-body']/h3/a/@href").extract()))
        print(text)
        print("temp ---**")
        print(temp)
        print("post----**")
        print(post)
            
        '''    
   
        with open(save_path1, 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(text) 
            f_object.close() 
            
            rows = zip (seqid, text, temp, posting)
        with open(save_path1, 'a') as f_object:
            writer_object = writer(f_object)
            for row in rows:
                writer_object.writerow(row) 
            f_object.close() 
            '''



