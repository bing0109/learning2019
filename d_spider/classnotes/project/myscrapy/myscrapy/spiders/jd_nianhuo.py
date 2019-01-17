# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
from bs4 import BeautifulSoup
import logging
import time
import random
from myscrapy.items import Jd_nianhuoItem
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    filename='/home/zelin/data/jd_nianhuo/jdnianhuo.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - line:%(lineno)d: %(message)s',
)


class JdNianhuoSpider(scrapy.Spider):
    """
    爬京东年货，练习scrapy和selenium对接
    利用selenium搜索和翻页，并返回结果
    爬取图片时用requests库
    爬取的对象包括 按 年货 搜索后，搜索结果列表，包括图片，商品名称，价格，评论数，店名，标签等信息，并保存图片
    """

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'myscrapy.middlewares.SeleniumDownloaderMiddleware': 406,
        },
        # 运行这个项目的时候，要注释settings里面的 DEFAULT_REQUEST_HEADERS 内容，不然会出错，原因未知
        'ITEM_PIPELINES': {
            'myscrapy.pipelines.MongoPipeline': 501,
        }
    }

    name = 'jd_nianhuo'
    # allowed_domains = ['www.jd.com']
    start_urls = ['http://www.jd.com/']

    def start_requests(self):
        key_word = quote(self.settings.get('KEY_WORD'))
        search_url = 'https://search.jd.com/Search?keyword=' + key_word + '&enc=utf-8&wq=' + key_word
        page = self.settings.get('MAX_PAGE')

        # 每次都请求搜索 年货 的页面，在middleware中的pipeline中的process_request用selenium翻页
        for i in range(1, page):
            # pg_url = 'https://search.jd.com/Search?keyword=%E5%B9%B4%E8%B4%A7&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E5%B9%B4%E8%B4%A7&stock=1&page='+str(2*i-1)+'&s=1&click=0'
            time.sleep(random.randint(1,3))
            logging.info('start request'+ search_url +'  pg:'+ str(i))
            yield scrapy.Request(url=search_url, callback=self.parse_page, meta={'pg': i}, dont_filter=True)


    def parse_page(self, response):
        goods_list = response.css('#J_goodsList > ul > li').extract()
        pg_id = response.meta['pg']
        for goods in goods_list:
            # yield self.parse_goods_info(goods, pg_id)
            # print('---goods----',goods_list.index(goods))
            # 直接返生成器会报错，需返回request等

    # def parse_goods_info(self, goods, pg_id):
    #     print('1111111111111111111111111111111111111')

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
            # print(info,'-----info------')
            logging.info('paras page, pgid:'+str(pg_id)+'; goods_id:'+ str(goods_list.index(goods)))
            yield scrapy.Request(url=info['img_url'], callback=self.get_img, meta={'detail': info, 'pg':pg_id, 'type': 'img'})

            # print(info_detail)

    def get_img(self, response):
        res = response.body
        pg_id = response.meta['pg']
        item_temp = response.meta['detail']

        img_name = str(item_temp['id']) +'.jpg'
        img_path = '/home/zelin/data/jd_nianhuo/img/'+ str(pg_id)
        if not os.path.exists(img_path):
            os.makedirs(img_path)
            logging.info('mkdir success'+ img_path)
            # print(img_path,'------imgpath------')

        with open(img_path+'/'+img_name, 'wb') as f:
            f.write(res)
            logging.info('save img success;' + img_path+'/'+img_name)
            # print(img_name,'--------imgname----')

        # print(img_path+'/'+img_name,'----img-----')

        item = Jd_nianhuoItem()
        item['id'] = item_temp['id']
        item['img_url'] = item_temp['img_url']
        item['price'] = item_temp['price']
        item['title'] = item_temp['title']
        item['comment_num'] = item_temp['comment_num']
        item['shop_name'] = item_temp['shop_name']
        item['tags'] = item_temp['tags']
        item['img_path'] = img_path
        return item
