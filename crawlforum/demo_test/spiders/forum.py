
#this file to collect userlike, likes and links
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
    name = 'forum'
    #start_urls = ['https://istio.io/latest/docs/concepts/']
    #start_urls = ['https://discuss.istio.io/t/forward-source-ip-of-https-request/6246']
    start_urls = ['https://discuss.istio.io/c/security/12']
    #start_urls = ['https://discuss.istio.io/']

    
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
    


    def parse_page(self, response):
        url = str(response.url)
        save_path1 = "../raw_data/forum/users.csv"
        save_path2 = "../raw_data/forum/userLinks.csv"
        save_path3 = "../raw_data/forum/likes.csv"
        #print(save_path1)
        self.logger.info(save_path1)
        save_dir = os.path.abspath(os.path.dirname(save_path1))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        #texts = response.xpath("//p/text()").extract()

        title=response.xpath("//title/text()").extract_first()
        users=response.xpath("//span[@class='creator']/a/span/text()").extract()
        users.insert(0,title)
        userLinks=response.xpath("//span[@class='creator']/a/@href").extract()
        userLinks.insert(0,title)
        likes2=response.xpath("//span[@class='post-likes']").extract()
        likes=[]
        likes.append(title)

        #for user, userLink in users, userLinks:
        #    postList.append((user, userLink))
            #print((user, userLink))
        for i in likes2:
            temp = re.search('>(.*)<', i).group(1)
            if temp == '':
                temp=0
            else:
                temp = temp.split(' ', 1)[0]
            likes.append(str(temp))

        print(users)
        print(likes)
        #print(likes)
        #postrcd = numpy.array((users, userLinks, likes2), dtype=str).tolist()
    
        '''
        save_file = open(save_path1, "a", encoding="utf-8")
        save_file.write(title  + ":" )
        for index, value in enumerate(users):
            if index < (len(users)-1):
                save_file.write(value + ",")
            else:
                save_file.write(value)
        save_file.write("\n")
        save_file.close()

'''
        with open(save_path1, 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(users) 
            f_object.close() 
        with open(save_path2, 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(userLinks) 
            f_object.close() 
        with open(save_path3, 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(likes) 
            f_object.close() 
        

