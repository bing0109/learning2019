# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo
import logging

logging.basicConfig(
    level=logging.INFO,
    filename='/home/zelin/data/jd_nianhuo/jdnianhuo.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - line:%(lineno)d: %(message)s',
)

class QuoteItemPipeline(object):
    """
    自定义的pipeline
    格式化item中的text字段
    """
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item:                                    # 判断item是否为空,为空就不处理
            if len(item['text']) > self.limit:
                item['text'] = item['text'][:self.limit].strip() + '...'    # text长度超过50,就进行截断处理

            item['tags'] = ','.join(item['tags'])

            return item
        else:
            DropItem('occur error')


class MongoPipeline(object):
    def __init__(self, mongo_url_a, mongo_db_a):
        self.mongo_url = mongo_url_a
        self.mongo_db = mongo_db_a

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url_a=crawler.settings.get('MONGO_URL'),
            mongo_db_a=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        """
        打开spider的时候,链接数据库
        :param spider:
        :return:
        """
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
        logging.info('open mongo')

    def close_spider(self, spider):
        """
        关闭spider的时候,要执行的动作
        :param spider:
        :return:
        """
        self.client.close()
        logging.info('close mongo')

    def process_item(self, item, spider):
        name = item.__class__.__name__      # 获取item对应的类的名字
        # print(name)
        self.db[name].insert_one(dict(item))
        logging.info('save data to mongo success' + name + str(dict(item)))



class RoborockyItemPipeline(object):
    pass