# -*- coding: utf-8 -*-
import scrapy
import time
import datetime
from scrapy.http import Request
from loguru import logger
from urllib.parse import urljoin

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class IjiandaoSpider(scrapy.Spider):
    name = 'ijiandao'
    allowed_domains = ['ijiandao.com']
    start_urls = ['http://www.ijiandao.com/safe']
    page = 1
    headers = {
        'Referer': 'http://www.ijiandao.com',
        'Host': 'www.ijiandao.com',
    }
    source = 'http://www.ijiandao.com'
    current_year = datetime.datetime.today().date().year
    current_month = datetime.datetime.today().date().month

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[@class="main_center"]/ul/li')
        for info in info_list:
            title = info.xpath('./h3/a/text()').extract_first('')
            link = urljoin(self.source, info.xpath('./h3/a/@href').extract_first(''))
            intro = info.xpath('./p/a/text()').extract_first('')
            author = info.xpath('./div/span[1]/a/text()').extract_first('')
            date_md = info.xpath('./div/span[@class="time"]/text()').extract_first('')
            if int(date_md.split('-')[0]) > self.current_month:
                self.current_year -= 1
            date = str(self.current_year) + '-' + date_md
            source = self.source
            type = 'news'
            item['title'] = title
            item['link'] = link
            item['intro'] = intro
            item['author'] = author
            item['date'] = date
            item['source'] = source
            item['type'] = type
            logger.info(item)
            yield item

        time.sleep(SLEEP_TIME)
        self.page += 1
        next_url = 'http://www.ijiandao.com/safe/page/{}'.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)















