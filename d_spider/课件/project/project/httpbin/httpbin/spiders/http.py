# -*- coding: utf-8 -*-
import scrapy


class HttpSpider(scrapy.Spider):
    name = 'http'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/get']

    # def start_requests(self):
    #     yield scrapy.FormRequest(url='http://httpbin.org/post',formdata={'nidate':'nimei'},callback=self.parse_fengxiong,method='POST',headers={'user-agent':'aaa'},meta={'a':'b'})

    def parse(self, response):
        self.logger.debug(response.status)

    def close(self,reason):
        self.logger.info(reason)
