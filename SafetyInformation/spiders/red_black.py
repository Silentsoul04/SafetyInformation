# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy.http import Request
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class RedBlackSpider(scrapy.Spider):
    name = 'red_black'
    allowed_domains = ['2cto.com']
    start_urls = ['http://www.2cto.com/news/safe/']
    page = 1
    headers = {
        'Referer': 'http://www.2cto.com/news/safe/',
        'Host': 'www.2cto.com',
    }
    source = 'http://www.2cto.com'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[@id="fontzoom"]/ul/li')
        for info in info_list:
            title = info.xpath('./a/text()').extract_first('')
            link = info.xpath('./a/@href').extract_first('')
            intro = info.xpath('./div/p[@class="intro"]/text()').extract_first('')
            tags = json.dumps(info.xpath('./div/p[@class="tags"]/a/text()').extract())
            source = self.source
            author = ''
            type = 'news'
            item['title'] = title
            item['link'] = link
            item['intro'] = intro
            item['source'] = source
            item['author'] = author
            item['type'] = type
            logger.info(item)
            time.sleep(SLEEP_TIME)
            yield Request(url=link, meta={'item': item}, headers=self.headers, callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta.get('item')
        date = response.xpath('//div[@class="box_left"]/dl/dd[@class="frinfo"]/text()').extract_first('').split(' ')[0]
        item['date'] = date
        yield item











