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
    filename='/home/zelin/data/joblist/job_analysis.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - line:%(lineno)d: %(message)s',
)

class Jobanalysis0223Pipeline(object):
    def process_item(self, item, spider):
        return item


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

