# -*- coding: utf-8 -*-
import re
import json
import urlparse
import simplejson
import httplib
import urllib
import scrapy
import requests

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
from scrapy.http import Request


class JustEasySpider(CrawlSpider):
    siteid=4 #采集数据的站点id
    sitename='家易事'#采集数据的站点名称
    name = "JustEasy"
    allowed_domains = ["justeasy.com.cn"]
    for i in range(1,3):

        start_urls = [
            #
            "http://www.justeasy.com.cn/merchandise/merchandiseList_1320",
            "http://www.justeasy.com.cn/merchandise/merchandiseList_1321",
            "http://www.justeasy.com.cn/merchandise/merchandiseList_1322",
            "http://www.justeasy.com.cn/merchandise/merchandiseList_1701",
            "http://www.justeasy.com.cn/merchandise/merchandiseList_1703",
            "http://www.justeasy.com.cn/merchandise/merchandiseList_1704",
            "http://www.justeasy.com.cn/merchandise/merchandiseList_1705"

        ]

    def parse_item(self, response): # 提取数据到Items里面，主要用到XPath和CSS选择器提取网页数据 parse_item
        log.start(logfile='log.txt', loglevel=log.WARNING)
        items = []
        prurl = get_base_url(response)
        sel = Selector(response)
        # log.msg(response.body.decode(response.encoding),level=log.WARNING)
        price_name=sel.css('#merprice').xpath('text()').extract()
        guige=sel.xpath('//li[@class="selected"]/a/span/text()').extract()
        if len(guige)>0:
            catalog=sel.css("div.sectionTop > a:nth-child(3)").xpath('text()').extract()
            # log.msg('catalog'+str(catalog[0]),level=log.WARNING)
            if len(catalog)>0 and catalog[0]  in ("国产水果","进口水果","生态蔬菜","有机蔬菜","精品菌菇","田园套餐","水果礼盒"):
                item = GuoShuItem()
                item['siteid'] =self.siteid
                item['sitename'] =self.sitename

                name=sel.xpath('//*[@id="mername"]/text()').extract()[0]
                item['name'] = name
                item['detailurl'] =prurl
                item['catalog'] = catalog[0]
                # guige=sel.xpath('//li[@class="selected"]/a/span/text()').extract()[0]
                item['guige'] = guige[0]
                item['danwei'] =item['guige']
                zhehouprice=item['price']=sel.css("#zhehouprice > i").xpath('text()').extract()
                price=sel.css("#merprice > i").xpath('text()').extract()
                if zhehouprice:
                    item['price']=zhehouprice[0][1:-3]
                else:
                    item['price']=price[0][1:-3]

                items.append(item)
        return items


    def parse(self, response):
        # log.msg('response %s' % repr(response.body.decode("utf-8")).decode("unicode-escape"),level=log.WARNING)
        log.start(logfile='log.txt', loglevel=log.WARNING)
        item = GuoShuItem()
        sel = Selector(response)
        totalpages=int(sel.css('div.fLeft.mentBox_r').xpath('text()').extract()[0].lstrip().rstrip().split('/')[1][:-1])#[0].replace("\r\n","").replace("共","").replace("页","").replace(" ","").lstrip().rstrip()
        # log.msg('totalpages:'+str(totalpages),level=log.WARNING)

        if totalpages>=1:

            base_url = get_base_url(response)
            for cpage in range(1,totalpages+1):#totalpages+1
                params = {
                    "lines":'20',
                    "page":cpage
                     }
                #定义一些文件头
                headers = {
                    # "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    # "Accept-Encoding":"gzip, deflate",
                    # "X-Requested-With":"XMLHttpRequest",
                    # "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
                    # "Connection":"Keep-Alive",
                    # "Cookies":"a4295_times=6; getdatecookie831=\"22556,9,36,\"; JSESSIONID=C14EAA9CCE0CF78A59EF1F3AFD7C1DC7.tomcat3; popped=yes; a4295_pages=3",
                    "Referer":base_url,
                    # "Host":"www.justeasy.com.cn",
                    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0",
                    "Content-Type":"application/x-www-form-urlencoded",
                    }
                cookies = dict(	a4295_times='6',getdatecookie831="22556,9,36,", JSESSIONID='C14EAA9CCE0CF78A59EF1F3AFD7C1DC7.tomcat3', popped="yes",a4295_pages='3')
                re=requests.post(base_url,data=params,headers=headers,cookies=cookies)

                if re.status_code == 200:
                    respp=scrapy.http.HtmlResponse(url=base_url,status=200,body=repr(re.text))
                    sel = Selector(respp)

                    link=sel.xpath('//ul/li/a[@class="textlink"]/@href').extract()
                    for li in link:
                        # log.msg('product:'+li,level=log.WARNING)
                        request = scrapy.Request("http://www.justeasy.com.cn%s"%(li),callback=self.parse_item)

                        request.meta['item'] = item

                        yield request
                    print "发布成功!^_^!"
                else:
                    print "发布失败\^0^/"





    def _process_request(self, request):
        # info('process ' + str(request))
        return request
