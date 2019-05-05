#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


class LianjiaSpider(scrapy.Spider):
    name = 'lianjiaspider'
    start_urls = ['https://sh.lianjia.com/ershoufang/']

    def parse(self, response):
        for district in response.css('[data-role=ershoufang] > div > a'):
            yield response.follow(district, self.parse_district, meta={'district': district.css('::text').get()})

    def parse_district(self, response):
        for subdistrict in response.css('[data-role=ershoufang] > div:nth-child(2) > a'):
             yield response.follow(subdistrict, self.parse_subdistrict, meta={
                 'district': response.meta['district'],
                 'subdistrict': subdistrict.css('::text').get()
             })

    def parse_subdistrict(self, response):
        num = int(response.css('.total > span::text').get().strip())
        for i in range(0, (num - 1) // 30 + 1):
            url = response.url if i == 0 else "%spg%d/" % (response.url, i + 1)
            yield response.follow(url, self.parse_page, meta={
                'district': response.meta['district'],
                'subdistrict': response.meta['subdistrict'],
                "page": i + 1
            }, dont_filter=True)

    def parse_page(self, response):
        body = BeautifulSoup(response.body, 'html.parser')
        for item in body.select('.info.clear'):
            yield {
                'district': response.meta['district'],
                'subdistrict': response.meta['subdistrict'],
                'page': response.meta['page'],
                'link': item.select('.title a')[0]['href'],
                'title': item.select('.title a')[0].get_text(),
                'info': item.select('.houseInfo')[0].get_text(),
                'position': item.select('.positionInfo')[0].get_text(),
                'follow': item.select('.followInfo')[0].get_text(),
                'total price': item.select('.totalPrice')[0].get_text(),
                'unit price': item.select('.unitPrice')[0].get_text()
            }