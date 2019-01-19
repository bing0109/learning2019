# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from pymongo import MongoClient

class TextPipeline(object):
    '''
    处理文本
    对item中的每个文本信息最多保留50个字符
    '''
    def __init__(self):
        self.limit=50

    def process_item(self, item, spider):
        if item:
            if len(item['text'])>self.limit:
                item['text']=item['text'][:self.limit].rstrip()+'...'
            return item
        else:
            DropItem('出现异常！！')

class MongoPipeline(object):
    '''
    保存数据到MongoDB
    '''

    def __init__(self,mongo_url,mongo_db):
        self.mongo_url=mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client = MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        name = item.__class__.__name__
        print(name)
        self.db[name].insert_one(dict(item))
        return item




