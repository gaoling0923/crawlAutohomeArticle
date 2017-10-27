# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from _md5 import md5

import happybase
import pymongo
from datetime import datetime
# from twisted.enterprise import adbapi

# import importlib,sys
from scrapy.conf import settings

import datetime
import random

from crawlAutohomeArticle.items import articleItem


class randomRowKey(object):
    # 生产唯一key
    def getRowKey(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum
class HBaseArticlePipeline(object):
    def __init__(self):
        host = settings['HBASE_HOST']
        self.port = settings['HBASE_PORT']
        self.table_name = settings['HBASE_TABLE']
        # port = settings['HBASE_PORT']
        self.connection = happybase.Connection(host=host,port=self.port,timeout=None, autoconnect=False)



    def process_item(self, item, spider):
        # cl = dict(item)
        randomrkey = randomRowKey()
        rowkey = randomrkey.getRowKey()
        self.connection.open()
        table = self.connection.table(self.table_name)
        # b= self.table.batch()
        if isinstance(item, articleItem):
            # self.table.put('text', cl)
            print('进入pipline')
            title = item['title']
            titleURL = item['titleURL']
            content = item['content']
            articletitle = item['articletitle']
            pubdate = item['pubdate']
            author = item['author']
            fromurl = item['fromurl']
            crawldate = item['crawldate']
            subtitle = item['subtitle']
            table.put(md5(str(rowkey).encode('utf-8')).hexdigest(), {
                'cf1:title': title,
                'cf1:titleURL': titleURL,
                'cf1:content': content,
                'cf1:articletitle': articletitle,
                'cf1:pubdate': pubdate,
                'cf1:author': author,
                'cf1:fromurl': fromurl,
                'cf1:crawldate': crawldate,
                'cf1:subtitle': subtitle
                                     })
            # b.send()
        self.connection.close()
        return item
class CrawlautohomearticlePipeline(object):
    def process_item(self, item, spider):
        return item
