# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy.http import Request
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class SecuritySpider(scrapy.Spider):
    name = 'security'
    allowed_domains = ['5ecurity.cn']
    start_urls = ['http://www.5ecurity.cn/index.php/page/1/']
    page = 1
    headers = {
        'Referer': 'http://www.5ecurity.cn/index.php',
        'Host': 'www.5ecurity.cn',
    }
    source = 'http://www.5ecurity.cn'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[@class="content"]/article[@class="excerpt"]')
        for info in info_list:
            tags = json.dumps([info.xpath('./header/a/text()').extract_first('')])
            title = info.xpath('./header/h2/a/text()').extract_first('')
            link = info.xpath('./header/h2/a/@href').extract_first('')
            date = info.xpath('./p[@class="meta"]/time/text()').extract()[-1].strip()
            author = info.xpath('./p[@class="meta"]/span[@class="author"]/text()').extract()[-1].strip()
            intro = info.xpath('./p[@class="note"]/text()').extract_first('')
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
        next_url = 'http://www.5ecurity.cn/index.php/page/{}/'.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)













