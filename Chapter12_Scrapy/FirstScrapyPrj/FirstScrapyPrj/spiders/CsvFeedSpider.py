# -*- coding: utf-8 -*-
from scrapy.spiders import CSVFeedSpider
from FirstScrapyPrj.items import FirstscrapyprjItem

class CsvfeedspiderSpider(CSVFeedSpider):
    name = 'CsvFeedSpider'
    allowed_domains = ['iqianyue.com']
    start_urls = ['http://yum.iqianyue.com/weisuenbook/pyspd/part12/mydata.csv']
    headers = ['name', 'sex', 'addr', 'email']
    delimiter = ','

    # Do any adaptations you need here
    #def adapt_response(self, response):
    #    return response

    def parse_row(self, response, row):
        i = FirstscrapyprjItem()
        i['Name']   = row['name'].encode()
        i['Sex']    = row['sex'].encode()
        print(i['Name'])
        print(i['Sex'])
        #i['name'] = row['name']
        #i['description'] = row['description']
        return i
