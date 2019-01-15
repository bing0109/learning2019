# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()


class RoborockItem(scrapy.Item):
    id = scrapy.Field()
    comm_star = scrapy.Field()
    comm_content = scrapy.Field()
    goods_type = scrapy.Field()
    comm_time = scrapy.Field()
    comm_nice_num = scrapy.Field()
    comm_reply_num = scrapy.Field()


class Jd_nianhuoItem(scrapy.Item):
    img_url = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    comment_num = scrapy.Field()
    shop_name = scrapy.Field()
    tags = scrapy.Field()
    img_path = scrapy.Field()