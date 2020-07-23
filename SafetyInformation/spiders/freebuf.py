# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request
from urllib.parse import urljoin
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import TOTAL_PAGES, SLEEP_TIME


class FreebufSpider(scrapy.Spider):
    name = 'freebuf'
    allowed_domains = ['freebuf.com']
    page = 1
    start_urls = ['https://www.freebuf.com/news/page/1']
    headers = {
        'Origin': 'https://www.freebuf.com',
        'Referer': 'https://www.freebuf.com/news',
    }
    source = 'https://www.freebuf.com'

    def start_requests(self):
        yield Request(url=self.start_urls[0], headers=self.headers, callback=self.parse)

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        news_list = response.xpath("//div[contains(@class, 'news-wapper')]/div[@id='timeline']/div")
        for news in news_list:
            title = news.xpath('./div[@class="news-info"]/dl/dt/a/text()').extract_first('')
            # link = news.xpath('/div[@class="news-info"]/dl/dt/a/@href').extract_first('')
            link = news.xpath('./div[@class="news-img"]/a/@href').extract_first('')
            author = news.xpath('./div[@class="news-info"]/dl/dd[1]/span[1]/a/text()').extract_first('')
            date = news.xpath('./div[@class="news-info"]/dl/dd[1]/span[3]/text()').extract_first('').strip()
            intro = news.xpath('./div[@class="news-info"]/dl/dd[2]/text()').extract_first('')
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
        next_url = urljoin(self.source, '/news/page/{}'.format(self.page))
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)


