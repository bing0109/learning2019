# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
from bs4 import BeautifulSoup
import logging
import time
from myscrapy.items import Jd_nianhuoItem


class JdNianhuoSpider(scrapy.Spider):
    """
    爬京东年货，练习scrapy和selenium对接
    """

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'myscrapy.middlewares.SeleniumDownloaderMiddleware': 404,
        },
        # 运行这个项目的时候，要注释settings里面的 DEFAULT_REQUEST_HEADERS 内容，不然会出错，原因未知
    }

    name = 'jd_nianhuo'
    allowed_domains = ['www.jd.com']
    start_urls = ['http://www.jd.com/']

    def start_requests(self):
        key_word = quote(self.settings.get('KEY_WORD'))
        search_url = 'https://search.jd.com/Search?keyword=' + key_word + '&enc=utf-8&wq=' + key_word
        page = self.settings.get('MAX_PAGE')
        for pg in range(1, page+1):
            yield scrapy.Request(url=search_url, callback=self.parse, meta={'page': pg}, dont_filter=True)

    def parse(self, response):
        # self.logger.error(str(response.status)+'--------res status-------')
        # print(response.body, '-------res-----process-request---------')
        soup = BeautifulSoup(response.body, 'html.parser')
        goods_list = soup.select('#J_goodsList > ul > li')
        print(len(goods_list),'----len goods_list----')
        for good in goods_list:
            try:
                img_url = 'https:' + good.select('div > div.p-img > a > img')[0].attrs['src']
            except Exception:
                # logging.warning('get img url through src failed;' + str(pg) + '-' + str(li_index))
                img_url = ''

            if img_url == '':
                try:
                    img_url = 'https:' + good.select('div > div.p-img > a > img')[0].attrs['data-lazy-img']
                except Exception:
                    img_url = ''
                    # logging.warning('get img url through data-lazy-image failed;' + str(pg) + '-' + str(li_index))

            price = good.select('div > div.p-price > strong > i')[0].get_text()
            title = good.select('div > div.p-name.p-name-type-2 > a > em')[0].get_text().strip()
            comment_num = good.select('div > div.p-commit > strong > a')[0].string
            try:
                shop_name = good.select('div > div.p-shop > span > a')[0].get_text()
            except Exception:
                shop_name = ''

            tags = good.select('div > div.p-icons')[0].get_text().strip().replace('\n', '/')

            item = Jd_nianhuoItem()
            item['img_url'] = img_url
            item['price'] = price
            item['title'] = title
            item['comment_num'] = comment_num
            item['shop_name'] = shop_name
            item['tags'] = tags
            item['img_path'] = ''
            yield item

            # print(info_detail)

    def get_img(self, url):
        res =
