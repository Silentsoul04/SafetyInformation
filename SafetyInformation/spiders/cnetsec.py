# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request
from loguru import logger
from urllib.parse import urljoin

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class CnetsecSpider(scrapy.Spider):
    name = 'cnetsec'
    allowed_domains = ['cnetsec.com']
    start_urls = ['http://www.cnetsec.com/list/1_1.html']
    page = 1
    headers = {
        'Referer': 'http://www.cnetsec.com/',
        'Host': 'www.cnetsec.com',
    }
    source = 'http://www.cnetsec.com/'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[@class="bd pb8 clear_fix"]/ul/li')
        for info in info_list:
            title = info.xpath('./a/span[@class="t"]/text()').extract_first('')
            link = urljoin(self.source, info.xpath('./a/@href').extract_first(''))
            intro = info.xpath('./p/text()').extract_first('')
            source = self.source
            type = 'news'
            item['title'] = title
            item['link'] = link
            item['intro'] = intro
            item['source'] = source
            item['type'] = type
            time.sleep(SLEEP_TIME)
            logger.info(item)
            yield Request(url=link, meta={'item': item}, headers=self.headers, callback=self.parse_detail)

        time.sleep(SLEEP_TIME)
        self.page += 1
        next_url = 'http://www.cnetsec.com/list/1_{}.html'.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta.get('item')
        author = response.xpath('//div[contains(@class,"col_c left")]/div/span/em/text()').extract_first('')
        date_list = response.xpath('//div[contains(@class,"col_c left")]/div/span/text()').extract()
        date = [date.strip() for date in date_list if date.strip()][-1].split(' ')[0].split('｜')[-1]
        item['author'] = author
        item['date'] = date
        yield item




















