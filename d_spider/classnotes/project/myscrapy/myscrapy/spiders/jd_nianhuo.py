# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
from bs4 import BeautifulSoup
import logging
import time
import random
from myscrapy.items import Jd_nianhuoItem


class JdNianhuoSpider(scrapy.Spider):
    """
    爬京东年货，练习scrapy和selenium对接
    爬取的对象包括 按 年货 搜索后，搜索结果列表，包括图片，商品名称，价格，评论数，店名，标签等信息，并保存图片
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

        # 每次都请求搜索 年货 的页面，在middleware中的pipeline中的process_request用selenium翻页
        for i in range(1,page):
            # pg_url = 'https://search.jd.com/Search?keyword=%E5%B9%B4%E8%B4%A7&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E5%B9%B4%E8%B4%A7&stock=1&page='+str(2*i-1)+'&s=1&click=0'
            time.sleep(random.randint(1,3))
            yield scrapy.Request(url=search_url, callback=self.parse_page, meta={'pg': i}, dont_filter=True)


    def parse_page(self, response):
        res_list = scrapy.Selector(response=response).css('#J_goodsList > ul > li').extract()
        pg_id = response.meta['pg']
        for goods in res_list:
            yield self.parse_goods_info(goods, pg_id)



    def parse_goods_info(self, goods, pg_id):
        good = BeautifulSoup(goods, 'html.parser')

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
        id = good.select('li.gl-item')[0].attrs['data-pid']

        info = {}
        info['id'] = id
        info['img_url'] = img_url
        info['price'] = price
        info['title'] = title
        info['comment_num'] = comment_num
        info['shop_name'] = shop_name
        info['tags'] = tags
        info['img_path'] = ''
        print(info,'-----info------')
        yield scrapy.Request(url=info['img_url'], callback=self.get_img, meta={'detail': info, 'pg':pg_id})

            # print(info_detail)

    def get_img(self, response):
        res = response.content
        pg_id = response.meta['pg']
        img_path = '/home/zelin/data/jd_nianhuo/img/'+ str(pg_id)

        print(img_path,'----imgpath-----')

        item_temp = response.meta['detail']
        print(item_temp, '----item temp-----')
        item = Jd_nianhuoItem()
        item['id'] = item_temp['id']
        item['img_url'] = item_temp['id']
        item['price'] = item_temp['id']
        item['title'] = item_temp['id']
        item['comment_num'] = item_temp['id']
        item['shop_name'] = item_temp['id']
        item['tags'] = item_temp['id']
        item['img_path'] = img_path
        return item
