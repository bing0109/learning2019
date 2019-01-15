# -*- coding: utf-8 -*-
import scrapy


class GoogleSpider(scrapy.Spider):
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,  # 默认请求失败了会自动重试3次，设置成none后，就不会进行多次请求
        }
    }
    name = 'google'
    allowed_domains = ['www.google.com']
    start_urls = ['http://www.google.com/']

    def parse(self, response):
        self.logger.info(response.status + '---res status-----')

