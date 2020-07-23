# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy.http import Request
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class SecInSpider(scrapy.Spider):
    name = 'sec_in'
    allowed_domains = ['sec-in.com']
    start_urls = ['https://www.sec-in.com/api/v1/Site/index?page=1&page_size=10&tabs=newest']
    page = 1
    headers = {
        'Referer': 'https://www.sec-in.com/index',
        'Host': 'www.sec-in.com',
    }
    source = 'https://www.sec-in.com'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        result_list = json.loads(response.text)['result']['data']
        for result in result_list:
            id = result['id']
            link = 'https://www.sec-in.com/article/{}'.format(id)
            title = result['article_title']
            date = result['passed_time'].split(' ')[0]
            author = result['member_info']['author_name']
            source = self.source
            info_type = 'news'
            intro = result['summary']
            tags = json.dumps([result['article_type_name']])
            item['title'] = title
            item['link'] = link
            item['date'] = date
            item['author'] = author
            item['source'] = source
            item['type'] = info_type
            item['intro'] = intro
            logger.info(item)
            yield item

        time.sleep(SLEEP_TIME)
        self.page += 1
        next_url = 'https://www.sec-in.com/api/v1/Site/index?page={}&page_size=10&tabs=newest'.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)






