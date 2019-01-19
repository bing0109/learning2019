# -*- coding: utf-8 -*-
import scrapy
from fengxiong.items import QuoteItem
from bs4 import BeautifulSoup


class QuoteSpider(scrapy.Spider):
    name = 'quote'#当前spider的名字，要保证独一无二性
    allowed_domains = ['quotes.toscrape.com']#可选项，后续请求允许的url范围
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes=response.css('.quote')#提取包含所有
        for quote in quotes:
            item = QuoteItem()
            item['text']=quote.css('.text::text').extract_first()#提取名言
            item['author'] = quote.css('.author::text').extract_first()#提取作者
            item['tags'] = quote.css('.tags .tag::text').extract()#提取标签
            yield item

        page = response.css('.pager .next a::attr("href")').extract_first()#提取下一页部分的url
        url = response.urljoin(page)#组合成下一页的url
        print(url)
        yield scrapy.Request(url=url,callback=self.parse)#下一步的请求