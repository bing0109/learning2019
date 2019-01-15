# -*- coding: utf-8 -*-
import scrapy
from myscrapy.items import RoborockItem
import json
import re
import time
import random


class RoborockSpider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {'myscrapy.pipelines.MongoPipeline': 301, }
    }

    name = 'roborock'
    allowed_domains = ['item.jd.com/8249826.html#none']
    # first_url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3927&productId=8249826&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&rid=0&fold=1'
    # start_urls = [first_url]

    def start_requests(self):
        # start_urls = [
        #     'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3927&productId=8249826&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&rid=0&fold=1',
        #     'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3927&productId=8249826&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&rid=0&fold=1',
        #     'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3927&productId=8249826&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1',
        #     'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3927&productId=8249826&score=0&sortType=5&page=2&pageSize=10&isShadowSku=0&rid=0&fold=1'
        # ]
        # for url in start_urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

        i = 0
        while i < 100:
            start_urls = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3927&productId=8249826&score=0&sortType=5&page=' + str(i) + '&pageSize=10&isShadowSku=0&rid=0&fold=1'
            yield scrapy.Request(url=start_urls, callback=self.parse)
            time.sleep(random.randint(1, 2))
            i += 1

    # 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3927&productId=8249826&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&rid=0&fold=1'
    # 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3927&productId=8249826&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1'
    # 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3927&productId=8249826&score=0&sortType=5&page=2&pageSize=10&isShadowSku=0&rid=0&fold=1'

    def parse(self, response):
        print(response.status, '------------------------------------------')
        response_temp = re.sub(r'^.*?\(', '', response.text)[:-2]       # 去掉Response中的...( 和末尾的） 变成标准的json格式进行处理
        # print(response_temp)
        res = json.loads(response_temp)['comments']
        # print('----------------------res---------------------')
        # print(res[1])
        for comm in res:
            item = RoborockItem()
            item['id'] = comm['id']
            item['comm_star'] = comm['score']
            item['comm_content'] = comm['content']
            item['goods_type'] = comm['productColor']
            item['comm_time'] = comm['creationTime']
            item['comm_nice_num'] = comm['usefulVoteCount']
            item['comm_reply_num'] = comm['replyCount']
            # print(len(item), '------------------------------')
            yield item

        # i = 1
        # next_page_url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3927&productId=8249826&score=0&sortType=5&page=' + str(i) +'&pageSize=10&isShadowSku=0&rid=0&fold=1'
