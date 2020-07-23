# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SafetyinformationItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SafeInfoItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    intro = scrapy.Field()
    source = scrapy.Field()
    type = scrapy.Field()


