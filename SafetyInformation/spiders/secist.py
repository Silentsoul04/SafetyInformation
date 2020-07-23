# -*- coding: utf-8 -*-
import scrapy
import time
import datetime
import re
import json
from scrapy.http import Request
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class SecistSpider(scrapy.Spider):
    name = 'secist'
    allowed_domains = ['secist.com']
    start_urls = ['http://www.secist.com/']
    page = 1
    headers = {
        'Referer': 'http://www.secist.com/',
        'Host': 'www.secist.com',
    }
    source = 'http://www.secist.com/'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[@class="content"]/article')
        for info in info_list:
            title = info.xpath('./header/h2/a/text()').extract_first('')
            link = info.xpath('./header/h2/a/@href').extract_first('')
            author = info.xpath('./p/span[1]/a/text()').extract_first('')
            date = info.xpath('./p/span[2]/text()').extract_first('').strip()
            n = int(re.findall(r'\d{0,2}', date, re.S)[0])
            date = re.findall(r'[(](.*?)[)]', date, re.S)[0]
            if len(date.split('-')) == 2:
                now_date = datetime.datetime.today().date()
                date_year = get_the_month(now_date, n)
                date = str(date_year) + '-' + date
            intro = info.xpath('./p[2]/text()').extract_first('').strip()
            source = self.source
            info_type = 'news'
            tags = json.dumps(info.xpath('./header/a/text()').extract())
            item['title'] = title
            item['link'] = link
            item['author'] = author
            item['date'] = date
            item['intro'] = intro
            item['source'] = source
            item['type'] = info_type
            logger.info(item)
            yield item

        time.sleep(SLEEP_TIME)
        self.page += 1
        next_url = 'http://www.secist.com/page/{}'.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)


def get_the_month(now_date, n):
    month = now_date.month
    year = now_date.year
    for i in range(n):
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
    # return datetime.date(year, month, 1).strftime('%Y-%m')
    return year










