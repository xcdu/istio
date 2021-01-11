# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawldocsItem(scrapy.Item):
    """
    'page_indexer' is the sub_url of page url, which removes the common prefix.
    'page_id' is the index number.
    """
    url = scrapy.Field()
    title = scrapy.Field()
    page_indexer = scrapy.Field()
    page_id = scrapy.Field()
    raw = scrapy.Field()
    headline = scrapy.Field()
