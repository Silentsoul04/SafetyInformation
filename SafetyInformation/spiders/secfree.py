# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request
from loguru import logger
from urllib.parse import urljoin

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class SecfreeSpider(scrapy.Spider):
    name = 'secfree'
    allowed_domains = ['secfree.com']
    start_urls = ['https://www.secfree.com/news/']
    page = 1
    headers = {
        'Referer': 'https://www.secfree.com/news/',
        'Host': 'www.secfree.com',
    }
    source = 'https://www.secfree.com'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//ul[@id="itemContainer"]/div')
        for info in info_list:
            title = info.xpath('./div/h3/a/text()').extract_first('')
            link = urljoin(self.source, info.xpath('./div/h3/a/@href').extract_first(''))
            author = info.xpath('./div/div[1]/a/text()').extract_first('')
            date = info.xpath('./div/div[1]/span[@class="date"]/text()').extract_first('').split(' ')[0]
            intro = info.xpath('./div/div[@class="recommend_article_list_simple"]/text()').extract_first('').strip()
            source = self.source
            type = 'news'
            item['title'] = title
            item['link'] = link
            item['author'] = author
            item['date'] = date
            item['intro'] = intro
            item['source'] = source
            item['type'] = type
            logger.info(item)
            yield item

        time.sleep(SLEEP_TIME)
        self.page += 1
        next_url = 'https://www.secfree.com/news/index.php?page={}'.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)











