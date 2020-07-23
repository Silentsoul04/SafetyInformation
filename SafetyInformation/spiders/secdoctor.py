# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request
from urllib.parse import urljoin
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class SecdoctorSpider(scrapy.Spider):
    name = 'secdoctor'
    allowed_domains = ['secdoctor.com']
    start_urls = ['http://www.secdoctor.com/html/sec/list_833_1.html']
    page = 1
    headers = {
        'Referer': 'http://www.secdoctor.com/html/sec/index.html',
        'Host': 'www.secdoctor.com',
    }
    source = 'http://www.secdoctor.com'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[@class="left_content"]/ul')
        for info in info_list:
            title = info.xpath('./li/a/text()').extract_first('')
            link = info.xpath('./li/a/@href').extract_first('')
            link = urljoin(self.source, link)
            date = info.xpath('./li/span/text()').extract_first('')
            author = ''
            intro = '无'
            source = self.source
            info_type = 'news'
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
        next_url = 'http://www.secdoctor.com/html/sec/list_833_{}.html'.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)







