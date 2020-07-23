# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class SecWikiSpider(scrapy.Spider):
    name = 'sec_wiki'
    allowed_domains = ['sec-wiki.com']
    start_urls = ['https://www.sec-wiki.com/event']
    page = 1
    sub_url = 'https://www.sec-wiki.com/event?Event_page={}&ajax=yw0'
    headers = {
        'Referer': 'https://www.sec-wiki.com/event',
        'Host': 'www.sec-wiki.com',
    }
    source = 'https://www.sec-wiki.com'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[@id="yw0"]/table/tbody/tr')
        for info in info_list:
            date = info.xpath('./td[1]/text()').extract_first('')
            title = info.xpath('./td[2]/a/text()').extract_first('')
            link = info.xpath('./td[2]/a/@href').extract_first('')
            author = info.xpath('./td[3]/a/text()').extract_first('')
            source = self.source
            info_type = 'news'
            intro = '无'
            item['title'] = title
            item['author'] = author
            item['link'] = link
            item['date'] = date
            item['source'] = source
            item['type'] = info_type
            item['intro'] = intro
            logger.info(item)
            yield item

        time.sleep(SLEEP_TIME)
        self.page += 1
        next_url = self.sub_url.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)









