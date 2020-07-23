# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy.http import Request
from loguru import logger
from urllib.parse import urljoin

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class XctfSpider(scrapy.Spider):
    name = 'xctf'
    allowed_domains = ['xctf.org.cn']
    start_urls = ['https://www.xctf.org.cn/library/?page=1']
    page = 1
    headers = {
        'Referer': 'https://www.xctf.org.cn/library/',
        'Host': 'www.xctf.org.cn',
    }
    source = 'https://www.xctf.org.cn'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[contains(@class,"col-md-12 pad10T")]/div[contains(@class,"mrg15B rose")]')
        for info in info_list:
            title = info.xpath('./article/div/div[2]/p[1]/a/text()').extract_first('').strip()
            link = info.xpath('./article/div/div[2]/p[1]/a/@href').extract_first('')
            link = urljoin(self.source, link)
            intro = info.xpath('./article/div/div[2]/a/text()').extract_first('').strip()
            date = info.xpath('./article/div/div[2]/p[@class="x_botts"]/span[last()]/span[@class="font14"]/text()').extract_first('').split(' ')[0]
            author = ''
            source = self.source
            info_type = 'news'
            tags = json.dumps(info.xpath('./article/div/div[2]/p[@class="x_botts"]/span[contains(@class,"blueColor font14")]/text()').extract())
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
        next_url = urljoin(self.source, '/library/?page={}'.format(self.page))
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)





