# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy.http import Request
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class YouxiaSpider(scrapy.Spider):
    name = 'youxia'
    allowed_domains = ['youxia.org']
    start_urls = ['http://www.youxia.org/tag/%e6%af%8f%e6%97%a5%e5%ae%89%e5%85%a8%e8%b5%84%e8%ae%af/']
    page = 1
    headers = {
        'Referer': 'http://www.youxia.org/tag/%e6%af%8f%e6%97%a5%e5%ae%89%e5%85%a8%e8%b5%84%e8%ae%af/',
        'Host': 'www.youxia.org',
    }
    source = 'http://www.youxia.org'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[@class="content"]/ul/li')
        for info in info_list:
            title = info.xpath('./a/text()').extract_first('')
            link = info.xpath('./a/@href').extract_first('')
            date = info.xpath('./span/text()').extract_first('')
            source = self.source
            info_type = 'news'
            author = ''
            intro = ''
            tags = json.dumps(['安全咨询'])
            item['title'] = title
            item['link'] = link
            item['date'] = date
            item['source'] = source
            item['type'] = info_type
            item['author'] = author
            item['intro'] = intro
            logger.info(item)
            yield item

        time.sleep(SLEEP_TIME)
        self.page += 1
        next_url = 'http://www.youxia.org/tag/%e6%af%8f%e6%97%a5%e5%ae%89%e5%85%a8%e8%b5%84%e8%ae%af/page/{}'.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)







