# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy.http import Request
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class SafebaseSpider(scrapy.Spider):
    name = 'safebase'
    allowed_domains = ['safebase.cn']
    start_urls = ['http://www.safebase.cn/list-12-1.html']
    page = 1
    headers = {
        'Referer': 'http://www.safebase.cn',
        'Host': 'www.safebase.cn',
    }
    source = 'http://www.safebase.cn'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[contains(@class,"bm_c xld")]/li[contains(@class,"sxp_picnews cl")]')
        for info in info_list:
            title = info.xpath('./h3/a/text()').extract_first('')
            link = info.xpath('./h3/a/@href').extract_first('')
            intro = info.xpath('./div/div/div[1]/em/text()').extract_first('')
            tags = json.dumps(info.xpath('./div/div/div[2]/label/a/text()').extract())
            date = info.xpath('./div/div/div[2]/span/text()').extract_first('').strip().split(' ')[0]
            source = self.source
            info_type = 'news'
            author = ''
            item['title'] = title
            item['link'] = link
            item['intro'] = intro
            item['date'] = date
            item['source'] = source
            item['type'] = info_type
            item['author'] = author
            logger.info(item)
            yield item

        time.sleep(SLEEP_TIME)
        self.page += 1
        next_url = 'http://www.safebase.cn/list-12-{}.html'.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)













