# -*- coding: utf-8 -*-
import datetime
import re
import scrapy
import time

from crawlAutohomeArticle.items import articleItem
import logging
logger = logging.getLogger('SpiderarticleSpider')
class SpiderarticleSpider(scrapy.Spider):
    name = 'spiderarticle'
    allowed_domains = ['www.autohome.com.cn']
    start_urls = [
        # 'http://www.autohome.com.cn/4069/0/0-0-1-0/',
        'http://www.autohome.com.cn/4166/0/0-0-1-0/',#宝骏510
        'http://www.autohome.com.cn/3824/0/0-0-1-0/',#森雅R7
        'http://www.autohome.com.cn/3080/0/0-0-1-0/',#瑞风S3
        'http://www.autohome.com.cn/2778/0/0-0-1-0/'#长安CS35
                  ]

    def __init__(self, **kwargs):
        self.count = 0
    def parse(self, response):
        # response.text
        self.count=self.count+1

        subtitle= response.css('div.content  div.subnav  div.subnav-title  div.subnav-title-name  a::text').extract_first()
        print(subtitle)
        coments= response.css('#maindiv  div.tab-content-cover  div  div.cont-info  ul  li')
        # print(coments)
        for coment in coments:
            item = articleItem()
            topicurl = coment.css('.newpic a::attr(href)').extract_first()  # 主题
            turl = response.urljoin(topicurl)
            #使用正则匹配-all.hmtl
            titleURL = ''
            p = re.compile('(-)\d+(.html$)')
            if re.search(p,turl):
                titleURL = re.sub(p, '-all.html', turl)
                # print(purl)
            else:
                titleURL=turl
            print(titleURL)
            # yield scrapy.Request(url=purl, callback=self.topicParse)
            # dd = scrapy.Request(url=purl, callback=self.topicParse)
            # print(dd)
            title = coment.css('h3 a::text').extract_first()  # 主题
            aus = coment.css('p.name-tx  span *::text').extract()
            if len(aus)>1:
                author=aus[0]
                pubdate=aus[1]
            ##maindiv > div.tab-content-cover > div > div.cont-info > ul > li:nth-child(1) > p.name-tx > span:nth-child(3)
            # author = coment.css('p.name-tx  span a::text').extract_first()  # 作者
            # pubdate = coment.css('p.name-tx  span span::text').extract_first()  # 发布时间
            loocountre = coment.css('p.name-tx  span:nth-child(3)::text').extract_first()  # 发布时间
            replycount = coment.css('p.name-tx  span:nth-child(4)::text').extract_first()  # 发布时间
            # print(title)
            # print(author)
            # print(pubdate)
            # print(loocountre)
            # print(replycount)

            crawldate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            item['title'] = title
            item['titleURL'] = titleURL
            # item['content'] = content
            # item['articletitle'] = articletitle
            item['pubdate'] = pubdate
            item['author'] = author
            item['fromurl'] = response.url
            item['crawldate'] = crawldate
            item['subtitle'] = subtitle

            logger.log(logging.INFO, '文章主题：%s' % title)
            logger.log(logging.INFO, '当前页数:%s' % self.count)
            logger.log(logging.INFO, '文章主题所在URL:%s' % response.url)

            request= scrapy.Request(url=titleURL, callback=self.topicParse)
            request.meta['item']=item
            yield  request
        # logger.info()





        #分页
        next = response.css('.page .page-item-next::attr(href)').extract_first()
        nurl=next.strip() if next  else '';
        url = response.urljoin(nurl);
        #print('下一页', url);
        logger.log(logging.INFO, '下一页:%s'% response.url)
        # self._wait()
        yield scrapy.Request(url=url, callback=self.parse);
    def topicParse(self,response):
        print('111111111111')
        logger.log(logging.INFO, '文章内容URL:%s' % response.url)
        item= response.meta['item']
        topic=response.css('.article-content')
        topictext=topic.css('p *::text').extract()
        articletitles=topic.css('.allread-title h2::text').extract()
        content = ''
        for text in topictext:
            content =content+text.strip()
            # print(text.strip())
        # print(content)

        articletitle = ''
        for t in articletitles:
            articletitle=articletitle+t.strip()+","
        # print(articletitle)
        item['content'] = content
        item['articletitle'] = articletitle
        yield  item

        # return  coment
    def _wait(self):
        for i in range(0, 3):
            print('.' * (i % 3 + 1))
            time.sleep(1)


