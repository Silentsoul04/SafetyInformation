# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class AnquanniuSpider(scrapy.Spider):
    name = 'anquanniu'
    allowed_domains = ['aqniu.com']
    start_urls = ['https://www.aqniu.com/category/news-views']
    page = 1
    headers = {
        'Referer': 'https://www.aqniu.com/category/news-views',
        'Host': 'www.aqniu.com',
    }
    source = 'https://www.aqniu.com'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[contains(@class, "col-sm-7")]/div[contains(@class, "row post")]')
        for info in info_list:
            title = info.xpath('./div/div[2]/h4/a/text()').extract_first('')
            link = info.xpath('./div/div[2]/h4/a/@href').extract_first('')
            intro = info.xpath('./div/div[2]/p/text()').extract_first('')
            author = info.xpath('./div/div[2]/div/span/a/text()').extract_first('')
            date = info.xpath('./div/div[2]/div/span[2]/text()').extract_first('')
            source = self.source
            info_type = 'news'
            item['title'] = title
            item['link'] = link
            item['intro'] = intro
            item['author'] = author
            item['date'] = date
            item['source'] = source
            item['type'] = info_type
            logger.info(item)
            yield item

        time.sleep(SLEEP_TIME)
        self.page += 1
        next_url = self.start_urls[0] + '/page/{}'.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)



