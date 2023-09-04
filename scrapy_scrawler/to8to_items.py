# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class To8toItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #
    content_name = scrapy.Field()
    #
    content_id = scrapy.Field()
    #
    content_url = scrapy.Field()
    #
    img_list = scrapy.Field()
