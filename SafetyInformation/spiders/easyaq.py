# -*- coding: utf-8 -*-
import scrapy
import time
import json
from loguru import logger
from scrapy.http import Request
from urllib.parse import urljoin

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class EasyaqSpider(scrapy.Spider):
    name = 'easyaq'
    allowed_domains = ['easyaq.com']
    start_urls = ['https://www.easyaq.com/type/0/1.shtml']
    page = 1
    headers = {
        'Referer': 'https://www.easyaq.com/?nsoad.com',
        'Host': 'www.easyaq.com',
    }
    source = 'https://www.easyaq.com/'

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[@class="layui-tab-item layui-show"]/div[contains(@class,"listnews")]')
        for info in info_list:
            title = info.xpath('./div/h3/a/text()').extract_first('')
            link = urljoin(self.source, info.xpath('./div/h3/a/@href').extract_first(''))
            intro = info.xpath('./div/p/text()').extract_first('')
            tags = json.dumps(info.xpath('./div/ul/span/li/a/text()').extract())
            author = info.xpath('./div/div/a/text()').extract_first('')
            date = info.xpath('./div/div/span[last()]/span/text()').extract_first('')
            source = self.source
            info_type = 'news'
            item['title'] = title
            item['link'] = link
            item['intro'] = intro
            item['author'] = author
            item['date'] = date
            item['source'] = source
            item['type'] = info_type
            logger.info(item)
            yield item

        time.sleep(SLEEP_TIME)
        self.page += 1
        next_url = 'https://www.easyaq.com/type/0/{}.shtml'.format(self.page)
        if self.page <= TOTAL_PAGES:
            yield Request(url=next_url, headers=self.headers, callback=self.parse)











