# -*- coding: utf-8 -*-
import scrapy
import time
import re
import feedparser
from loguru import logger

from SafetyInformation.items import SafeInfoItem


class SolidotSpider(scrapy.Spider):
    name = 'solidot'
    allowed_domains = ['solidot.org']
    start_urls = ['https://www.solidot.org/index.rss']
    source = 'https://www.solidot.org'
    page = 1

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        buf = feedparser.parse(self.start_urls[0])
        result_list = buf['entries']
        for result in result_list:
            link = result['link']
            date = time.strftime('%Y-%m-%d', result['published_parsed'])
            title = result['title']
            intro = result['summary']
            description = re.findall(r'(.*?)<a.*?>(.*?)</a>(.*?)<p>.*?', intro)
            intro = ''.join(list(description[0]))
            source = self.source
            info_type = 'news'
            author = ''
            item['title'] = title
            item['link'] = link
            item['date'] = date
            item['intro'] = intro
            item['source'] = source
            item['type'] = info_type
            item['author'] = author
            logger.info(item)
            yield item











