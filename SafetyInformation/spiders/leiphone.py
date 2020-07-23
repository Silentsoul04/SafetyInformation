# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy.http import Request
from loguru import logger
from urllib.parse import urljoin

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class LeiphoneSpider(scrapy.Spider):
    name = 'leiphone'
    allowed_domains = ['leiphone.com']
    start_urls = ['https://www.leiphone.com/category/letshome']
    page = 1
    headers = {
        'Referer': 'https://www.leiphone.com/category/letshome',
        'Host': 'www.leiphone.com',
    }
    source = 'https://www.leiphone.com'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[@class="list"]/ul[@class="clr"]/li')
        for info in info_list:
            title = info.xpath('./div/div[@class="word"]/h3/a/text()').extract_first('').strip()
            link = info.xpath('./div/div[@class="word"]/h3/a/@href').extract_first('')
            intro = info.xpath('./div/div[@class="word"]/div[@class="des"]/text()').extract_first('').strip()
            author = info.xpath('./div/div[@class="word"]/div[contains(@class,"msg")]/a/text()').extract()[-1].strip()
            date = info.xpath('./div/div[@class="word"]/div[contains(@class,"msg")]/div[@class="time"]/text()').extract_first('').split(' ')[0]
            tags = json.dumps(info.xpath('./div/div[@class="word"]/div[contains(@class,"msg")]/div[@class="tags"]/a/text()').extract())
            info_type = 'news'
            source = self.source
            item['title'] = title
            item['link'] = link
            item['intro'] = intro
            item['author'] = author
            item['date'] = date
            item['type'] = info_type
            item['source'] = source
            logger.info(item)
            yield item

        time.sleep(SLEEP_TIME)
        self.page += 1
        next_url = self.start_urls[0] + '/page/{}'.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)












