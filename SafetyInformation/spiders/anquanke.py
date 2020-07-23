# -*- coding: utf-8 -*-
import scrapy
import json
import time
from scrapy.http import Request
from urllib.parse import urlencode
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class AnquankeSpider(scrapy.Spider):
    name = 'anquanke'
    allowed_domains = ['anquanke.com']
    start_urls = ['https://api.anquanke.com/data/v1/posts?']
    page = 1
    param = {
        'size': 10,
        'page': page,
        'category': 'news',
    }
    start_url = start_urls[0] + urlencode(param)
    headers = {
        'Referer': 'https://www.anquanke.com/news',
        'Origin': 'https://www.anquanke.com',
    }
    source = 'https://www.anquanke.com'

    def start_requests(self):
        yield Request(url=self.start_url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        result = json.loads(response.text)
        info_list = result['data']
        for info in info_list:
            url_id = info.get('id')
            title = info.get('title')
            intro = info.get('desc')
            date = info.get('date')
            author = info['author'].get('nickname')
            source = self.source
            link = 'https://www.anquanke.com/post/id/' + str(url_id)
            info_type = 'news'
            item['title'] = title
            item['intro'] = intro
            item['date'] = date
            item['author'] = author
            item['source'] = source
            item['link'] = link
            item['type'] = info_type
            logger.info(item)
            yield item

        time.sleep(SLEEP_TIME)
        self.page += 1
        next_url = result.get('next')
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)




