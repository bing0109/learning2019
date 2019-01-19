# -*- coding: utf-8 -*-
import scrapy
import time
import json
from jdbra.items import BraItem

#分析网页的主要思路
    #（1）我们主要是为了获取商品的销售数据（评论数据），首先找到商品的销售数据，跟网页呈现的相同
    #（2）找到对应的链接，分析链接里面包含的主要信息：有商品的ID——ProductId、评论数据的页码——page
    #（3）接下来主要考虑不同的商品对应的ID，看网站的URL会发现有ProductID的信息，就可以以此确定通过京东搜索页面，
    #     输入关键字，我们可以基于呈现的页面来分析，可以获取商品的ProductID

#爬虫的主要思路：
    #（1）通过搜索商品关键字，来得到关于商品的页面，点击“销量”进行排序，基于该页面的URL完成，发送请求，获取商品ProductID
    #（2）得到商品ProductID之后，构建评论数据对应的链接，进行请求，获得该商品的评论数据最大页码maxpage
    #（3）得到最大页码之后，可以重新基于商品ProductId和页数page，重新构建评论数据的URL，进行请求，获得每个商品，每页下面的销售数据
    #（4）获得响应进行解析，提取感兴趣的数据，并进行保存。

class BraSpider(scrapy.Spider):
    name = 'bra'
    # allowed_domains = ['www.jd.com']
    start_urls = ['http://www.jd.com/']

    def start_requests(self):
        '''
        初始请求
        :return:
        '''
        url = 'https://search.jd.com/search?keyword=%E8%83%B8%E7%BD%A9&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E8%83%B8%E7%BD%A9&psort=4&cid2=1345&cid3=1364&uc=0'
        yield scrapy.Request(url=url,callback=self.parse_prodcut)

    def parse_prodcut(self, response):
        '''
        获取商品ID，以及确定下一步请求，用来获取商品评论
        :param response:
        :return:
        '''
        #提取商品ID
        products=response.xpath('//*[@id="J_goodsList"]/ul/li[contains(@class,"gl-item")]/@data-sku').extract()
        products = list(set(products))#去重
        for product in products:
            #请求
            product_url='https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv2059&productId='+product+'&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
            yield scrapy.Request(url=product_url,callback=self.parse_page,meta={'product':product})


    def parse_page(self, response):
        '''
        提取当前商品的对应的评论页码数，以及商品第一页的评论信息
        确定翻页请求
        :param response:
        :return:
        '''
        result = response.text.replace('fetchJSON_comment98vv2059(','').replace(');','')
        result=json.loads(result)
        comments = result['comments']
        for comment in comments:
            yield self.get_item(comment)

        page = result['maxPage']
        for pn in range(1,page):
            page_url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv2059&productId='+response.meta['product']+'&score=0&sortType=5&page='+str(pn)+'&pageSize=10&isShadowSku=0&fold=1'
            time.sleep(1)
            yield scrapy.Request(url=page_url,callback=self.parse_rate)


    def parse_rate(self, response):
        '''
        提取评论信息
        :param response:
        :return:
        '''
        result = response.text.replace('fetchJSON_comment98vv2059(', '').replace(');', '')
        result = json.loads(result)
        comments = result['comments']
        for comment in comments:
            yield self.get_item(comment)


    def get_item(self,comment):
        '''
        将获取的信息转化为item结构，方便复用
        :param comment:
        :return:
        '''
        item = BraItem()
        item['id'] = comment['id']
        item['productColor'] = comment['productColor']
        item['productSize'] = comment['productSize']
        item['content'] = comment['content']
        item['referenceName'] = comment['referenceName']
        return item
