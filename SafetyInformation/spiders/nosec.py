# -*- coding: utf-8 -*-
import scrapy
import json
import time
from scrapy.http import FormRequest
from loguru import logger

from SafetyInformation.items import SafeInfoItem
from SafetyInformation.settings import SLEEP_TIME, TOTAL_PAGES


class NosecSpider(scrapy.Spider):
    name = 'nosec'
    allowed_domains = ['nosec.org']
    start_urls = ['https://nosec.org/home/ajaxindexdata']
    page = 1
    headers = {
        'Referer': 'https://nosec.org/home/index',
        'Host': 'nosec.org',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRF-TOKEN': 'xx7Ivf9c0KCZOptafzkAvZNXMcOQ4ptZ6SbDgWkM',
        'Cookie': 'Hm_lvt_176023972b5e615deb22d97a52557032=1589855362,1589878474; XSRF-TOKEN=eyJpdiI6IkVUYUpcL0s2eTVhU0p2UlBDenhabElRPT0iLCJ2YWx1ZSI6IkZ5b3pJR1R4K3ZYNllaMmNVTmpFa1dqTDNGdmpUMFNVNk5XckNJVDFRU0diSFRxWEhaYXBqRTVLVGlrWXJmYUxmbmIwdHpIcm1sb0h1Z3p6dWlxS0tRPT0iLCJtYWMiOiIwMzUzYjEwMmY1NWQwNzBmNTIzZmI0ZDE3ZjJlZjI0N2E3NDNhNGFiNTNkZWQ5YzVlNGViNDA3ODA0M2RjYTJlIn0%3D; laravel_session=eyJpdiI6InMwZXBuU1o5cFJ5SWZDaTl3dENzZkE9PSIsInZhbHVlIjoiRmcwd29Ra1J0Z1RONlJ4cWFXeFcxR0FVRUhRXC80YkNkU21vNEVyM2JhcXlcL3BoYk4zbVRHU0VueUFCM0xTS1wvTzZ6dVhRQ0xJbUdVeWZcL0poOGJ2d0JnPT0iLCJtYWMiOiIyNWQ2MTliMWQzM2NkNzI4MDQ1ODcyYzNiN2ZiYjgwZTJlZGU1MjE5ODY1Yzc5NDA2NDI5MWMwZDBmNGNhNmM3In0%3D; Hm_lpvt_176023972b5e615deb22d97a52557032=1589878542'
    }
    param = {
        'keykind': '',
        'page': str(page),
    }
    source = 'https://nosec.org'

    def start_requests(self):
        yield FormRequest(url=self.start_urls[0], headers=self.headers, formdata=self.param, callback=self.parse)

    def parse(self, response):
        logger.info("==========当前正在抓取第{}页==========".format(self.page))
        item = SafeInfoItem()
        result_list = json.loads(response.text)['data']['threatData']['data']
        for result in result_list:
            id = result['id']
            title = result['title']
            link = 'https://nosec.org/home/detail/{}.html'.format(id)
            intro = result['summary']
            date = result['publiced_at'].split(' ')[0]
            author = result['username']
            tags = json.dumps([result['kind_name']])
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
        self.param['page'] = str(self.page)
        if self.page <= TOTAL_PAGES:
            yield FormRequest(url=self.start_urls[0], headers=self.headers, formdata=self.param, callback=self.parse)







