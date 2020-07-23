# -*- coding: utf-8 -*-
import scrapy
import time
import re
import datetime
from scrapy.http import Request
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class SecpulseSpider(scrapy.Spider):
    name = 'secpulse'
    allowed_domains = ['secpulse.com']
    start_urls = ['https://www.secpulse.com/archives/category/news']
    page = 1
    headers = {
        'Host': 'www.secpulse.com',
        'Referer': 'https://www.secpulse.com/archives/category/news',
    }
    source = 'https://www.secpulse.com'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[@id="main"]/div[2]/div[2]/ul/li')
        for info in info_list:
            title = info.xpath('./div/div[@class="slide_text fl"]/p/a/text()').extract_first('')
            link = info.xpath('./div/div[@class="slide_text fl"]/p/a/@href').extract_first('')
            intro = info.xpath('./div/div[@class="slide_text fl"]/p[2]/text()').extract_first('').strip()
            date = info.xpath('./div/div[@class="slide_text fl"]/div[@class="top"]/div[1]/a[contains(@class,"time")]/text()').extract_first('').strip()
            days = re.findall(r'\d{0,2}', date, re.S)[0]
            delta = datetime.timedelta(days=int(days))
            current_date = datetime.datetime.today().date()
            if len(date.split('-')) == 3:
                date = date.split(' ')[0]
            elif len(date.split('-')) == 1:
                date = (current_date - delta).strftime('%Y-%m-%d')
            author = info.xpath('./div/div[@class="slide_text fl"]/div[@class="top"]/div[1]/a[2]/span/text()').extract_first('').strip()
            source = self.source
            info_type = 'news'
            item['title'] = title
            item['link'] = link
            item['intro'] = intro
            item['date'] = date
            item['author'] = author
            item['source'] = source
            item['type'] = info_type
            logger.info(item)
            yield item
        
        time.sleep(SLEEP_TIME)
        self.page += 1
        next_url = self.start_urls[0] + '/page/{}'.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)




