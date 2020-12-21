# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawldocsItem(scrapy.Item):
    """
    'page_indexer' is the sub_url of page url, which removes the common prefix.
    """
    url = scrapy.Field()
    title = scrapy.Field()
    page_indexer = scrapy.Field()
    raw = scrapy.Field()
    header = scrapy.Field()

    """
    Each page has multiple slices of contents, which have an sequential index 
    numbers from 1 to len(content_dict).
    The indexer 0 is the root of the current page.
    'content_dict' is a list storing sliced page texts in sequence.
    'adjacency' is a dict storing mapping from a string number to a sequence of 
    string number, such as '1' to ' 2 3 4', which means the content 1 has sub 
    nodes of 2, 3, and 4. It maintains the hierarchy of the page.
    'next_links' is a dict storing mapping from indexer number to actual links.
    'templates_hierarchy' is a dict storing mapping from indexer number to the
    content of template.
    
    The reason why we use string number as key and sequential string number as 
    value is because of the compatibility of serialization.
    """
    content_list = scrapy.Field()
    adjacency = scrapy.Field()
    next_links = scrapy.Field()
    templates_hierarchy = scrapy.Field()

