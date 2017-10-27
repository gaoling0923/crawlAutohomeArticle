# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class articleItem(scrapy.Item):

    title = scrapy.Field()#标题
    titleURL = scrapy.Field()  # 标题
    content = scrapy.Field()#内容
    articletitle = scrapy.Field()#内容
    pubdate = scrapy.Field()#发布时间
    author = scrapy.Field()#作者
    fromurl = scrapy.Field()#url
    crawldate = scrapy.Field()
    subtitle = scrapy.Field()
    # reg_time = scrapy.Field()#注册时间
    # addr = scrapy.Field()#来自
    # attent_vehicle = scrapy.Field()#关注车型

    # author_url = scrapy.Field()#作者url
class CrawlautohomearticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
