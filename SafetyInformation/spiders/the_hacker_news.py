# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class TheHackerNewsSpider(scrapy.Spider):
    name = 'the_hacker_news'
    allowed_domains = ['thehackernews.com']
    start_urls = ['https://thehackernews.com/']
    page = 1
    source = 'https://thehackernews.com/'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[@id="Blog1"]/div/div[contains(@class, "body-post clear")]')
        for info in info_list:
            title = info.xpath('./a/div/div[contains(@class,"clear home-right")]/h2/text()').extract_first('')
            link = info.xpath('./a[@class="story-link"]/@href').extract_first('')
            date = info.xpath('./a/div/div[contains(@class,"clear home-right")]/div[@class="item-label"]/text()').extract_first('')
            date = time.strftime('%Y-%m-%d', time.strptime(date, '%B %d, %Y'))
            author = info.xpath('./a/div/div[contains(@class,"clear home-right")]/div[@class="item-label"]/span/text()').extract_first('').strip()
            source = self.source
            intro = info.xpath('./a/div/div[contains(@class,"clear home-right")]/div[@class="home-desc"]/text()').extract_first('').strip()
            info_type = 'news'
            item['title'] = title
            item['link'] = link
            item['date'] = date
            item['author'] = author
            item['source'] = source
            item['intro'] = intro
            item['type'] = info_type
            logger.info(item)
            yield item

        time.sleep(SLEEP_TIME)
        self.page += 1
        next_url = response.xpath('//a[@id="Blog1_blog-pager-older-link"]/@href').extract_first('')
        if not next_url:
            return
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, callback=self.parse)













