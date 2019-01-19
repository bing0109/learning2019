# -*- coding: utf-8 -*-
import scrapy
from myscrapy.items import QuoteItem


class QuoteSpider(scrapy.Spider):
    name = 'quote'      # 当前spider爬取的项目名字,要保证唯一
    allowed_domains = ['quotes.toscrape.com']        # 可选项,后续请求允许的url范围
    start_urls = ['http://quotes.toscrape.com/']     # 开初始请求,在genspider时输入的网址,可以自己修改

    custom_settings = {
        'ITEM_PIPELINES': {'myscrapy.pipelines.QuoteItemPipeline': 300, 'myscrapy.pipelines.MongoPipeline': 301, }
    }

    def parse(self, response):
        res = response.css('.quote')
        for re in res:
            item = QuoteItem()
            item['text'] = re.css('.text::text').extract_first()
            item['author'] = re.css('.author::text').extract_first()
            item['tags'] = re.css('.tag::text').extract()               # 返回一个列表

            print(item)
            yield item

        next_page_url_temp = response.css('.next a::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url_temp)
        print(next_page_url)
        # yield scrapy.Request(url=next_page_url, callable=self.parse, dont_filter=True)   # dont_filter=True 表示scheduler不会对url去重处理,
        yield scrapy.Request(url=next_page_url, callback=self.parse)
        print(response.status)
