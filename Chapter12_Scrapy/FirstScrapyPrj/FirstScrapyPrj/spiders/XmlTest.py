# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
from FirstScrapyPrj.items import FirstscrapyprjItem

class XmltestSpider(XMLFeedSpider):
    name = 'XmlTest'
    allowed_domains = ['https://donaldzhuang.wordpress.com/feed']
    start_urls = ['https://donaldzhuang.wordpress.com/feed']
    iterator = 'iternodes' # you can change this; see the docs
    itertag = 'rss' # change it accordingly

    def parse_node(self, response, selector):
        TestItem = FirstscrapyprjItem()
        TestItem['RssTitle'] = selector.xpath('//item/title/text()').extract()

        for i in TestItem['RssTitle']:
            print(i)
        #i['name'] = selector.select('name').extract()
        #i['description'] = selector.select('description').extract()
        return TestItem
