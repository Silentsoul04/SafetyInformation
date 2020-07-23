# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy.http import Request
from loguru import logger
from urllib.parse import urljoin

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class AnzerclubSpider(scrapy.Spider):
    name = 'anzerclub'
    allowed_domains = ['anzerclub.com']
    start_urls = ['http://www.anzerclub.com/']
    page = 1
    source = 'http://www.anzerclub.com/'
    headers = {
        'Referer': 'http://www.anzerclub.com/',
        'Host': 'www.anzerclub.com',
    }

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[contains(@class,"recommend_list mod_list")]/ul[@class="article-list"]/li[@class="post_part clear"]')
        for info in info_list:
            title = info.xpath('./div[@class="cont"]/h3/a/text()').extract_first('')
            link = info.xpath('./div[@class="cont"]/h3/a/@href').extract_first('')
            link = urljoin(self.source, link)
            data_list = info.xpath('./div[@class="cont"]/div[@class="info"]/span/text()').extract()
            data = [_.strip() for _ in data_list if _.strip()]
            date = data[-1]
            author = data[-2]
            resource = data[0]
            source = self.source
            info_type = 'news'
            intro = info.xpath('./div[@class="cont"]/p/text()').extract_first('')
            item['title'] = title
            item['link'] = link
            item['date'] = date
            item['author'] = author
            item['source'] = source
            item['type'] = info_type
            item['intro'] = intro
            logger.info(item)
            yield item







