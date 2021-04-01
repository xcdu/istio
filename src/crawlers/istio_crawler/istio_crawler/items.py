# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IstioCrawlerItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    page_indexer = scrapy.Field()
    page_id = scrapy.Field()
    raw = scrapy.Field()
    headline = scrapy.Field()
