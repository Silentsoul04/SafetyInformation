# -*- coding: utf-8 -*-
import scrapy
import time
import json
from scrapy.http import FormRequest, Request
from loguru import logger
from urllib.parse import urljoin

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class ToolsSpider(scrapy.Spider):
    name = 'tools'
    allowed_domains = ['t00ls.net']
    start_urls = ['https://www.t00ls.net/news.html?page=1']
    page = 1
    headers = {
        'Referer': 'https://www.t00ls.net/news.html',
        'Host': 'www.t00ls.net',
        'X-Requested-With': 'XMLHttpRequest',
    }
    source = 'https://www.t00ls.net'
    param = {
        'page': str(page)
    }

    def start_requests(self):
        yield FormRequest(url=self.start_urls[0], headers=self.headers, formdata=self.param, callback=self.parse)

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        info_list = response.xpath('//div[@id="articleslist"]/div')
        for info in info_list:
            tags = json.dumps(info.xpath('./div[@class="layout_post_2 clearfix"]/div/div[@class="item_thumb"]/div[@class="thumb_meta"]/span[1]/a/text()').extract())
            title = info.xpath('./div[@class="layout_post_2 clearfix"]/div/div[@class="item_content"]/h4/a/text()').extract_first('')
            link = info.xpath('.//div[@class="layout_post_2 clearfix"]/div/div[@class="item_content"]/h4/a/@href').extract_first('')
            link = urljoin(self.source, link)
            intro = info.xpath('./div[@class="layout_post_2 clearfix"]/div/div[@class="item_content"]/p/text()').extract_first('')
            date1 = info.xpath('./div[@class="layout_post_2 clearfix"]/div/div[@class="item_content"]/div[@class="item_meta clearfix"]/span[@class="meta_date"]/span/@title').extract_first('')
            date2 = info.xpath('./div[@class="layout_post_2 clearfix"]/div/div[@class="item_content"]/div[@class="item_meta clearfix"]/span[@class="meta_date"]/text()').extract_first('')
            date = date1.split(' ')[0] if date1 else date2.split(' ')[0]
            author = ''
            source = self.source
            info_type = 'news'
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
        next_url = 'https://www.t00ls.net/news.html?page={}'.format(self.page)
        self.param['page'] = str(self.page)
        if self.page <= TOTAL_PAGES:
            yield FormRequest(url=next_url, headers=self.headers, formdata=self.param, callback=self.parse)








