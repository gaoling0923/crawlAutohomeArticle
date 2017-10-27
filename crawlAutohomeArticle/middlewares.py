# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import requests
import time

from scrapy import signals
from scrapy.conf import settings
import random
# from crawAutohomebbsdetail.dbpackage.dbresdis import RedisClient
from selenium.webdriver.common.proxy import ProxyType

from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait





class JavaScriptMiddleware(object):

    def process_request(self, request, spider):

        # if spider.name in("spiderb30bbs","crawlb30bbsdetail"):
        print("execute PhantomJS spiderName", spider.name);
        print("PhantomJS is starting...")
        driver = webdriver.PhantomJS() #指定使用的浏览器
        #driver =webdriver.Chrome()
        # driver = webdriver.Firefox()
        driver.get(request.url)
        #driver.p
        # time.sleep(1)
        # js = "var q=document.documentElement.scrollTop=10000"
        # driver.execute_script(js) #可执行js，模仿用户操作。此处为将页面拉至最底端。
        time.sleep(2)
        body = driver.page_source
        print ("访问："+request.url)
        return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
class JavaScriptProxyMiddleware(object):

    def process_request(self, request, spider):
        # conn = RedisClient();
        # proxy = conn.pop();
        # print('当前使用的IP:', proxy);
        # request.meta['proxy'] = "http://%s" % proxy

        # proxy=self.get_proxy()
        if spider.name in("spiderarticle"):
            print("execute PhantomJS spiderName", spider.name);
            print("PhantomJS is starting..")
            driver = webdriver.PhantomJS() #指定使用的浏览器
            #driver =webdriver.Chrome()
            # driver = webdriver.Firefox()
            # 利用DesiredCapabilities(代理设置)参数值，重新打开一个sessionId，我看意思就相当于浏览器清空缓存后，加上代理重新访问一次url
            proxy = webdriver.Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxyip=self.get_proxy()
            print('PROXY_IP:', proxyip)

            if proxyip:
                print('进入:', proxyip)
                proxy.http_proxy = proxyip

                # 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
                proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
                driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
                driver.get(request.url)
                # print('1: ', driver.session_id)
                # print('2: ', driver.page_source)
                # print('3: ', driver.get_cookies())
                # js = "var q=document.documentElement.scrollTop=10000"
                # browser.execute_script(js) #可执行js，模仿用户操作。此处为将页面拉至最底端。
                # time.sleep(3)
                body = driver.page_source
                # print ("访问2="+body)
                print ("访问="+request.url)
                return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
            else:
                proxy = webdriver.Proxy()
                proxy.proxy_type = ProxyType.DIRECT
                proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
                driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
                driver.get(request.url)
                body = driver.page_source
                return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)

        else:
            return
class CrawlautohomearticleSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
