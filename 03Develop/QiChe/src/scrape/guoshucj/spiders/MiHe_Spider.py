# -*- coding: utf-8 -*-
import re
import json
import urlparse

from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy import log

from guoshucj.items import *


class MiHeSpider(CrawlSpider):
    siteid=3#采集数据的站点id
    sitename=u'米禾'#采集数据的站点名称
    name = "MiHe"
    allowed_domains = ["ranlixu.com"]
    start_urls = [
        "http://www.ranlixu.com/class.asp?larCode=1",
        "http://www.ranlixu.com/class.asp?larCode=701"
        # "http://www.ranlixu.com/list.asp?ProdId=A03026"
    ]
    rules = [ # 定义爬取URL的规则
        Rule(sle(allow=("/class.asp\?larCode=1&Page=\d{,4}")), follow=True),
        Rule(sle(allow=("/class.asp\?larCode=701&Page=\d{,4}")), follow=True),
        Rule(sle(allow=("/list.asp\?ProdId=G\d{,10}")), follow=True, callback='parse_item'),
        Rule(sle(allow=("/list.asp\?ProdId=A\d{,10}")), follow=True, callback='parse_item')
    ]

    def parse_item(self, response): # 提取数据到Items里面，主要用到XPath和CSS选择器提取网页数据 parse_item
        log.start(logfile='log.txt', loglevel=log.WARNING)
        items = []
        sel = Selector(response)
        base_url = get_base_url(response)
        catalog=sel.css('div.cc').xpath('text()').extract()[2]
        catalog=catalog[catalog.index(u'品牌：'):].replace("\r\n","").replace("品牌：","").lstrip().rstrip()
        item = GuoShuItem()
        item['siteid'] =self.siteid
        item['sitename'] =self.sitename
        item['name'] = sel.css('div.cc h2').xpath('text()').extract()[0]
        item['detailurl'] =base_url
        item['catalog'] = catalog
        item['guige'] = sel.css('div.cc b').xpath('text()').extract()[0]
        price = sel.css('div.cc').xpath('.//font[@color="red"]/text()').extract()[0]
        item['price'] = price
        item['danwei'] =item['guige']
        items.append(item)
        # print repr(item).decode("unicode-escape") + '\n'
        # log.msg('item %s' % repr(item).decode("unicode-escape"),level=log.WARNING)


        # info('parsed ' + str(response))
        return items

    def _process_request(self, request):
        # info('process ' + str(request))
        return request

# from guoshucj.items import *
#
#
# class TencentSpider(CrawlSpider):
#     name = "tencent"
#     allowed_domains = ["tencent.com"]
#     start_urls = [
#         "http://hr.tencent.com/position.php"
#     ]
#     rules = [ # 定义爬取URL的规则
#         Rule(sle(allow=("/position.php\?&start=\d{,4}#a")), follow=True, callback='parse_item')
#     ]
#
#     def parse_item(self, response): # 提取数据到Items里面，主要用到XPath和CSS选择器提取网页数据
#         items = []
#         sel = Selector(response)
#         base_url = get_base_url(response)
#         sites_even = sel.css('table.tablelist tr.even')
#         for site in sites_even:
#             item = TencentItem()
#             item['name'] = site.css('.l.square a').xpath('text()').extract()
#             relative_url = site.css('.l.square a').xpath('@href').extract()[0]
#             item['detailLink'] = urljoin_rfc(base_url, relative_url)
#             item['catalog'] = site.css('tr > td:nth-child(2)::text').extract()
#             item['workLocation'] = site.css('tr > td:nth-child(4)::text').extract()
#             item['recruitNumber'] = site.css('tr > td:nth-child(3)::text').extract()
#             item['publishTime'] = site.css('tr > td:nth-child(5)::text').extract()
#             items.append(item)
#             #print repr(item).decode("unicode-escape") + '\n'
#
#         sites_odd = sel.css('table.tablelist tr.odd')
#         for site in sites_odd:
#             item = TencentItem()
#             item['name'] = site.css('.l.square a').xpath('text()').extract()
#             relative_url = site.css('.l.square a').xpath('@href').extract()[0]
#             item['detailLink'] = urljoin_rfc(base_url, relative_url)
#             item['catalog'] = site.css('tr > td:nth-child(2)::text').extract()
#             item['workLocation'] = site.css('tr > td:nth-child(4)::text').extract()
#             item['recruitNumber'] = site.css('tr > td:nth-child(3)::text').extract()
#             item['publishTime'] = site.css('tr > td:nth-child(5)::text').extract()
#             items.append(item)
#             #print repr(item).decode("unicode-escape") + '\n'
#
#         # info('parsed ' + str(response))
#         return items
#
#
#     def _process_request(self, request):
#         # info('process ' + str(request))
#         return request
