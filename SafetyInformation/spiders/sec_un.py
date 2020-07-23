# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class SecUnSpider(scrapy.Spider):
    name = 'sec_un'
    allowed_domains = ['sec-un.org']
    start_urls = ['https://www.sec-un.org/all-posts/']
    page = 1
    headers = {
        'Referer': 'https://www.sec-un.org/all-posts/',
        'Host': 'www.sec-un.org'
    }
    source = 'https://www.sec-un.org'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[@class="elementor-widget-container"]/div[contains(@class,"elementor-posts--skin-classic")]/article')
        for info in info_list:
            title = info.xpath('./div/h3/a/text()').extract_first('').strip()
            link = info.xpath('./div/h3/a/@href').extract_first('')
            author = info.xpath('./div/div[@class="elementor-post__meta-data"]/span[@class="elementor-post-author"]/text()').extract_first('').strip()
            date = info.xpath('./div/div[@class="elementor-post__meta-data"]/span[@class="elementor-post-date"]/text()').extract_first('').strip()
            source = self.source
            info_type = 'news'
            intro = info.xpath('./div/div[@class="elementor-post__excerpt"]/p/text()').extract_first('')
            item['title'] = title
            item['link'] = link
            item['author'] = author
            item['date'] = date
            item['source'] = source
            item['type'] = info_type
            item['intro'] = intro
            logger.info(item)
            yield item

        time.sleep(SLEEP_TIME)
        self.page += 1
        next_url = 'https://www.sec-un.org/all-posts/page/{}/'.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)











