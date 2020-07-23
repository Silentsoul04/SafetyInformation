# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request
from loguru import logger
from urllib.parse import urljoin

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class Myhack58Spider(scrapy.Spider):
    name = 'myhack58'
    allowed_domains = ['myhack58.com']
    start_urls = ['http://www.myhack58.com/Article/html/1/4/Article_004_1.htm']
    page = 1
    headers = {
        'Referer': 'http://www.myhack58.com/',
        'Host': 'www.myhack58.com',
    }
    source = 'http://www.myhack58.com/'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[@class="ArticleListBox"]/ul')
        for info in info_list:
            title = info.xpath('./li[@class="Noptitle"]/a/text()').extract_first('')
            link = info.xpath('./li[@class="Noptitle"]/a/@href').extract_first('')
            link = urljoin(self.source, link)
            intro = info.xpath('./li[@class="Noptdes"]/text()').extract_first('')
            n_info = info.xpath('./li[@class="Noptinfo"]/text()').extract_first('').split(' ')
            nopt_info = [n for n in n_info if n.strip()]
            tags = nopt_info[0].split('：')[-1]
            date = nopt_info[1].split('：')[-1]
            info_type = nopt_info[2].split('：')[-1] if nopt_info[2].split('：')[-1] else 'news'
            source = self.source
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
        next_url = 'http://www.myhack58.com/Article/html/1/4/Article_004_{}.htm'.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)


















