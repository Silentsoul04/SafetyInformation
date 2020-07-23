# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy.http import FormRequest
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class SecjiaSpider(scrapy.Spider):
    name = 'secjia'
    allowed_domains = ['secjia.com']
    start_urls = ['http://api.secjia.com/article/news_list']
    page = 1
    notice = 0
    limit = 10
    headers = {
        'Referer': 'http://toutiao.secjia.com/',
        # 'Host': 'api.secjia.com',
    }
    param = {
        'limit': str(limit),
        'notice': '',
    }
    source = 'http://toutiao.secjia.com/#/'

    def start_requests(self):
        yield FormRequest(url=self.start_urls[0], headers=self.headers, formdata=self.param, callback=self.parse)

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        result_list = json.loads(response.text)['data']
        for result in result_list:
            title = result['title']
            date = result['publish_time'].split(' ')[0]
            id = result['id']
            link = 'http://toutiao.secjia.com/article/page?topid={}'.format(id)
            intro = result['summary']
            author = ''
            source = self.source
            info_type = 'news'
            item['title'] = title
            item['date'] = date
            item['link'] = link
            item['intro'] = intro
            item['author'] = author
            item['source'] = source
            item['type'] = info_type
            logger.info(item)
            yield item

        time.sleep(SLEEP_TIME)
        self.page += 1
        self.notice += self.limit
        self.param['notice'] = str(self.notice)
        if self.page <= TOTAL_PAGES:
            yield FormRequest(url=self.start_urls[0], headers=self.headers, formdata=self.param, callback=self.parse)












