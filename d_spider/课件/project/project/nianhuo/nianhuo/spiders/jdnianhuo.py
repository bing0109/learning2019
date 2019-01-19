# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote


class JdnianhuoSpider(scrapy.Spider):
    name = 'jdnianhuo'
    # allowed_domains = ['www.jd.com']
    start_urls = ['http://www.jd.com/']

    #初始请求
    def start_requests(self):
        #从settings获取搜索关键字
        key_word = quote(self.settings.get('KEY_WORD'))
        #构建url
        page = self.settings.get('MAX_PAGE')
        for pn in range(1,page+1):#翻页
            p = 2*pn-1
            url = 'https://search.jd.com/Search?keyword='+key_word+'&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq='+key_word+'&stock=1&page='+str(p)+'&s=112&click=0'
            yield scrapy.Request(url=url,callback=self.parse_item,meta={'page':pn},dont_filter=True)


    def parse_item(self, response):
        print(response.status)
