# -*- coding: utf-8 -*-
import scrapy


class GoogleSpider(scrapy.Spider):
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,  # 默认请求失败了会自动重试3次，设置成none后，就不会进行多次请求
            'myscrapy.middlewares.GoogleDownloaderMiddleware': 405
        }
    }
    name = 'google'
    allowed_domains = ['www.google.com']
    start_urls = ['http://www.google.com/']

    def start_requests(self):
        # meta里面的超时时间设置的请求url后1s后超时，配合验证Middleware中的downloadmiddleware里面设置的process_exception方法
        yield scrapy.Request(url=self.start_urls[0],callback=self.parse,meta={'download_timeout': 1}, dont_filter=True)

    def parse(self, response):
        self.logger.info(response.status + '---res status-----')

