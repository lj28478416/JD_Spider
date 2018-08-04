# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    item_id = scrapy.Field()
    title = scrapy.Field()
    price_wap = scrapy.Field()
    buy_num = scrapy.Field()
    rate = scrapy.Field()
    count = scrapy.Field()
