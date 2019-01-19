# -*- coding: utf-8 -*-
import scrapy


class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['www.google.com']
    start_urls = ['http://www.google.com/']

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],callback=self.parse,meta={'download_timeout':1},dont_filter=True)

    def parse(self, response):
        print(response.url)
