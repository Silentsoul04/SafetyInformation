# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy.http import Request
from loguru import logger
from urllib.parse import urljoin

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class SecNewsSpider(scrapy.Spider):
    name = 'sec_news'
    allowed_domains = ['wiki.ioin.in']
    start_urls = ['http://wiki.ioin.in/page-1']
    page = 1
    headers = {
        'Referer': 'http://wiki.ioin.in',
        'Host': 'wiki.ioin.in',
    }
    source = 'http://wiki.ioin.in'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//table[contains(@class,"width-auto")]/tbody/tr')
        for info in info_list:
            date = info.xpath('./td[1]/text()').extract_first('')
            title = info.xpath('./td[2]/a/text()').extract_first('').strip()
            link = info.xpath('./td[2]/a/@href').extract_first('')
            link = urljoin(self.source, link)
            author = ''
            intro = ''
            source = self.source
            info_type = 'news'
            tags = json.dumps(info.xpath('./td[3]/a/text()').extract())
            # print(tags)
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
        next_url = urljoin(self.source, '/page-{}'.format(self.page))
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)







