# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy.http import Request
from loguru import logger
from urllib.parse import urljoin

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class HackernewsSpider(scrapy.Spider):
    name = 'hackernews'
    allowed_domains = ['hackernews.cc']
    start_urls = ['http://hackernews.cc/']
    page = 1
    headers = {
        'Referer': 'http://hackernews.cc/',
        'Host': 'hackernews.cc',
    }
    source = 'http://hackernews.cc/'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//section[@id="classic-list"]/div/article')
        for info in info_list:
            title = info.xpath('./div[2]/h3/a/text()').extract_first('')
            link = info.xpath('./div[2]/h3/a/@href').extract_first('')
            date = info.xpath('./div[2]/div[@class="light-post-meta"]/span[2]/a/text()').extract_first('')
            author = info.xpath('./div[2]/div[@class="light-post-meta"]/span[1]/a/text()').extract_first('')
            source = self.source
            info_type = 'news'
            intro = info.xpath('./div[2]/div[@class="m-post-excepert"]/text()').extract_first('').strip()
            tags = json.dumps(info.xpath('./div[2]/div[@class="light-post-meta"]/span[3]/a/text()').extract())
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
        next_url = urljoin(self.start_urls[0], '/page/{}'.format(self.page))
        logger.info(next_url)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)










