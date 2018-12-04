# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

from douban.settings import (mongo_authMechanism, mongo_authSource, mongo_host,
                             mongo_password, mongo_username)


class DoubanPipeline(object):
  def __init__(self):
    host = mongo_host
    username = mongo_username
    password = mongo_password
    authSource = mongo_authSource
    authMechanism = mongo_authMechanism
    client = MongoClient(host=host,
                        username=username,
                        password=password,
                        authSource=authSource,
                        authMechanism=authMechanism)
    db = client["douban"]
    self.collection = db["douban_spider"]      
  def process_item(self, item, spider):
    data = dict(item)
    self.collection.insert(data)
    # return item
