# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy.http import Request
from urllib.parse import urljoin
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class NsoadSpider(scrapy.Spider):
    name = 'nsoad'
    allowed_domains = ['nsoad.com']
    start_urls = ['http://www.nsoad.com/news/']
    page = 1
    headers = {
        'Referer': 'http://www.nsoad.com/news/',
        'Host': 'www.nsoad.com',
    }
    source = 'http://www.nsoad.com'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[contains(@class,"main-mid main-index")]/div[contains(@class,"news_index")]')
        for info in info_list:
            title = info.xpath('./div[@class="nsoad_news-info"]/dl/dt/a/text()').extract_first('')
            link = info.xpath('./div[@class="nsoad_news-info"]/dl/dt/a/@href').extract_first('')
            link = urljoin(self.source, link)
            author = info_list.xpath('./div[@class="nsoad_news-info"]/dl/dd[1]/span[1]/text()').extract_first('')
            date = info.xpath('./div[@class="nsoad_news-info"]/dl/dd[1]/span[2]/text()').extract_first('').split(' ')[0]
            intro = info.xpath('./div[@class="nsoad_news-info"]/dl/dd[2]/text()').extract_first('')
            tags = json.dumps([info.xpath('./div[@class="nsoad_news-info"]/div/span/text()').extract_first('').strip()])
            source = self.source
            info_type = 'news'
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
        next_url = 'http://www.nsoad.com/news/index_{}.html'.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)












