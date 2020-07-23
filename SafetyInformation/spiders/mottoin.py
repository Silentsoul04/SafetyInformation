# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy.http import FormRequest
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class MottoinSpider(scrapy.Spider):
    name = 'mottoin'
    allowed_domains = ['mottoin.com']
    start_urls = ['http://www.mottoin.com/getPostByCategory']
    page = 1
    headers = {
        'Referer': 'http://www.mottoin.com/',
        'Host': 'www.mottoin.com',
        'X-Requested-With': 'XMLHttpRequest',
    }
    param = {
        'page': str(page),
        'categoryId': '31'
    }
    source = 'http://www.mottoin.com/'

    def start_requests(self):
        yield FormRequest(url=self.start_urls[0], headers=self.headers, formdata=self.param, callback=self.parse)

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        result_list = json.loads(response.text)['data']
        for result in result_list:
            title = result['name']
            author = result['userName']
            date = result['publishedAtDesc']
            link = result['postUrl']
            source = self.source
            info_type = 'news'
            tags = json.dumps([_['name'] for _ in result['category']])
            intro = result['summaryDesc']
            item['title'] = title
            item['author'] = author
            item['date'] = date
            item['link'] = link
            item['source'] = source
            item['type'] = info_type
            item['intro'] = intro
            logger.info(item)
            yield item

        time.sleep(SLEEP_TIME)
        self.page += 1
        self.param['page'] = str(self.page)
        if self.page <= TOTAL_PAGES:
            yield FormRequest(url=self.start_urls[0], headers=self.headers, formdata=self.param, callback=self.parse)













