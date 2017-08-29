# -*- coding: utf-8 -*-
import scrapy
from FirstScrapyPrj.items import FirstscrapyprjItem

class TestSpider(scrapy.Spider):
    name = 'Test'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def __init__(self, UrlAddr=None, *args, **kwargs):
        super(TestSpider, self).__init__(*args, **kwargs)
        
        UrlList = UrlAddr.split('|')
        for i in UrlList:
            print( '[USR DBG ]Url to Crawl : %s' % i )
        if(UrlAddr != None):
            self.start_urls = UrlList

    def parse(self, response):
        item = FirstscrapyprjItem()
        item['UrlTitle'] = response.xpath('/html/head/title/text()')
        print(item['UrlTitle'])
        pass
