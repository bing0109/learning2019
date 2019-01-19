# -*- coding: utf-8 -*-
import scrapy


class HttpbinSpider(scrapy.Spider):
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'myscrapy.middlewares.HttpbinDownloaderMiddleware': 303
        }
    }

    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/post']

    def start_requests(self):
        header_data = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
        }
        meta_data = {
            'a': 'b',
        }
        form_data = {
            'xiaomi': 'damin'
        }
        # yield scrapy.Request(url=self.start_urls[0], callback=self.parse, method='POST', headers=header_data, meta=meta_data)
        yield scrapy.FormRequest(url=self.start_urls[0], callback=self.parse, method='POST', headers=header_data, meta=meta_data, formdata=form_data)

    # 改写了start_request后，下面的parse就可以改名字，否则不能改
    def parse(self, response):
        print(response.headers, '---re headers----')
        print(response.status, '----status----')
        self.logger.info(response.meta['a'] + '------res meta---')
        self.logger.info(response.text + '------res---')

    def close(self, reason):
        self.logger.info(reason)
