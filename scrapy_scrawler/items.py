# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GuaziItem(scrapy.Item):
    # define the fields for your item here like:
    brand_value = scrapy.Field()
    #
    brand_name = scrapy.Field()
    #
    car_id = scrapy.Field()
    #
    car_name = scrapy.Field()
    # 里程
    road_haul = scrapy.Field()
    # 排量
    displacement = scrapy.Field()
    # 变速箱
    transmission = scrapy.Field()
    #
    first_pay = scrapy.Field()
    #
    license_date = scrapy.Field()
    #
    price = scrapy.Field()
    #
    img_list = scrapy.Field()


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