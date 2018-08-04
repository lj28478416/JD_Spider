# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
class JdSpiderPipeline(object):
    def open_spider(self,spider):
        client = MongoClient('127.0.0.1',27017)
        self.jd_collection = client.JD.jd_full
        self.jd_collection.drop()
    def process_item(self, item, spider):
        if item['count'] >= 100:
            dict1 = {}
            dict1.update(item.__dict__['_values'])
            self.jd_collection.insert(dict1)
        return item
from scrapy_redis.pipelines import RedisPipeline
class JDRedisPipeline(RedisPipeline):
    def _process_item(self, item, spider):
        if item['count'] >= 100:
            key = self.item_key(item, spider)
            data = self.serialize(item)
            self.server.rpush(key, data)
        return item
