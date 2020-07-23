# -*- coding: utf-8 -*-
import scrapy
import time
import re
from scrapy.http import Request
from urllib.parse import urlencode
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class SihouSpider(scrapy.Spider):
    name = 'sihou'
    allowed_domains = ['4hou.com']
    start_urls = ['https://www.4hou.com/category/news?']
    page = 1
    param = {
        'page': page,
        'category': 'news',
    }
    headers = {
        'Host': 'www.4hou.com',
        'Referer': 'https://www.4hou.com/category/news',
    }
    start_url = start_urls[0] + urlencode(param)
    source = 'https://www.4hou.com'

    def start_requests(self):
        yield Request(url=self.start_url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[@id="post-data"]/div[@class="main-box"]')
        for info in info_list:
            title = info.xpath('./li/div/a/h1/text()').extract_first('')
            link = info.xpath('./li/div/a/@href').extract_first('')
            date = info.xpath('./li/div/div/p/text()').extract_first('').split(' ')[0]
            author = info.xpath('./li/div/div/div/a/p/text()').extract_first('')
            try:
                # python UCS-4 build的处理方式
                high_points = re.compile(u'[\U00010000-\U0010ffff]')
            except re.error:
                # python UCS-2 build的处理方式
                high_points = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
            author = high_points.sub(u'', author)
            intro = '无'
            source = self.source
            info_type = 'news'
            item['title'] = title
            item['link'] = link
            item['date'] = date
            item['author'] = author
            item['intro'] = intro
            item['source'] = source
            item['type'] = info_type
            logger.info(item)
            yield item

        time.sleep(SLEEP_TIME)
        self.page += 1
        self.param['page'] = self.page
        next_url = self.start_urls[0] + urlencode(self.param)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)


