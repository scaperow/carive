# -*- coding: utf-8 -*-
import re
import json
import urlparse
import time
import scrapy
import simplejson
import httplib,urllib;  #加载模块
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


class BenLaiSpider(CrawlSpider):
    siteid=2#采集数据的站点id
    sitename=u'本来生活'#采集数据的站点名称
    name = "BenLai"
    allowed_domains = ["benlai.com"]
    start_urls = [
        "http://www.benlai.com/list-1-2.html"
        # "http://www.benlai.com/item-45338.html"
    ]
    rules = [ # 定义爬取URL的规则
        Rule(sle(allow=("/list-\d{,4}-\d{,4}-\d{,4}.html")), follow=True, callback='parse_ajaxpage'),
        Rule(sle(allow=("/item-\d{,10}.html")), follow=True, callback='parse_item')
    ]
    def parse_ajaxpage(self,response):#
        log.start(logfile='log.txt', loglevel=log.WARNING)
        # hxs = HtmlXPathSelector(response)
        item = GuoShuItem()
        sel = Selector(response)
        # totalpages=sel.css('div.fr.pdr15').xpath('text()').extract()#[0].replace("\r\n","").replace("共","").replace("页","").replace(" ","").lstrip().rstrip()
        totalnum=int( sel.css('div.eb6100 span').xpath('text()').extract()[0])
        totalpages=totalnum/28
        if totalnum%28>0:
            totalpages=totalpages+1
        # log.msg('totalpages %s' % repr(totalpages),level=log.WARNING)
        #这里url是虚构的,使用时需要修改
        # url = "http://www.benlai.com/Category/GetC3List?page=2&filter=&sort=0&c3SysNo=11&startPrice=&endPrice=&_=1424826954248"#+str(time.time())
        # request = scrapy.Request(url,callback=self.parse_ajax)
        # request.meta['item'] = item
        #这里将ajax的url找出来,然后够找请求,框架执行请求收到返回后再回调
        # yield request

        # conn = httplib.HTTPConnection("http://www.benlai.com")
        # conn.request(method="GET",url=url)
        # response = conn.getresponse()
        # res= response.read()
        base_url = get_base_url(response)
        # log.msg('base_url:'+base_url,level=log.WARNING)
        SysNo=base_url.split('-')[3].split('.')[0];
        # log.msg('SysNo:'+SysNo,level=log.WARNING)
        log.msg('base_url:'+base_url+' totalnum:' + str(totalnum),level=log.WARNING)
        if totalpages>1:
            #定义一些文件头
            headers = {"Content-Type":"application/json; charset=utf-8",
                       "Connection":"Keep-Alive",
                       "Referer":base_url,
                       "Accept-Encoding":"gzip, deflate",
                       "X-Requested-With":"XMLHttpRequest",
                       "Accept":"*/*",
                       "Host":"www.benlai.com",
                       "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0",
                       "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
                       "Cookie":"userGuid=4398c964-24c8-4e14-a046-f051280e3bcf; _pk_id.1.0671=223584ab66d3c401.1423619008.13.1424826911.1424760235.; IsAutoSelected=1; WebSiteSysNo=1; DeliverySysNo=2; PHPStat_First_Time_ahhhffgh=1423619003066; PHPStat_Cookie_Global_User_Id=_ck15021109432310705758788768118; PHPStat_Return_Time_ahhhffgh=1424826910240; PHPStat_Msrc_ahhhffgh=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%25b1%25be%25c0%25b4%25c9%25fa%25bb%25ee%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; PHPStat_Msrc_Type_ahhhffgh=pmf_from_free_search; Hm_lvt_a6b20d1b3b2571f43355b57c2c746eab=1423619007,1424420879,1424826911; _pk_ref.1.0671=%5B%22%22%2C%22%22%2C1424826911%2C%22http%3A%2F%2Fwww.baidu.com%2Fbaidu%3Fwd%3D%25B1%25BE%25C0%25B4%25C9%25FA%25BB%25EE%26tn%3Dmonline_4_dg%22%5D; _jzqa=1.3458688639465196000.1423619009.1424760235.1424826911.13; _jzqy=1.1423619009.1423619009.1.jzqsr=baidu|jzqct=%B1%BE%C0%B4%C9%FA%BB%EE.-; _ga=GA1.2.741275614.1423619010; ag_fid=WPpXxA4DtZ8b5pAF; __ag_cm_=1424420879707; tma=209502081.80923192.1423619013587.1424760238305.1424826913396.8; tmd=45.209502081.80923192.1423619013587.; city=*u897F*u5B89; PHPStat_Return_Count_ahhhffgh=7; _jzqx=1.1423721221.1424760235.5.jzqsr=benlai%2Ecom|jzqct=/.jzqsr=benlai%2Ecom|jzqct=/list-1-9-108%2Ehtml; 4398c964-24c8-4e14-a046-f051280e3bcf_LstFiveProdIDKey=36937%7C1118012035C%2C6784%7C0101050202C%2C40682%7C0101032102C%2C6787%7C0101050205C%2C15633%7C0102020964C; ASP.NET_SessionId=mdv2vmxfg5br1yd4q2k3ldoi; __RequestVerificationToken_Lw__=XnrFgRN0VuEviedHlLdfsipgHXAuIbnpxRhciTU5xt22fYvSh7ZIRzRprB1A4RwO/JQpJnK7C2wvuCX4twGRL4mo//a+kvA1WaiqLvmYjYWq6WZ5db+/TsVi/QKjC6/pePdUdipcmbUYsiyEBgkpCyRNFFIgbAP6pKF0RnusnBA=; sess_web=2; _pk_cvar.1.0671=%7B%221%22%3A%5B%224398c964-24c8-4e14-a046-f051280e3bcf%22%2C%22uid%22%5D%2C%222%22%3A%5B%221%22%2C%22%3A%3A%3A%3A%3A%22%5D%7D; _pk_ses.1.0671=*; Hm_lpvt_a6b20d1b3b2571f43355b57c2c746eab=1424826911; _qzja=1.636168760.1423619012112.1424760235163.1424826911052.1424760235163.1424826911052..0.0.48.13; _qzjb=1.1424826911051.1.0.0.0; _qzjc=1; _qzjto=1.1.0; _jzqb=1.1.10.1424826911.1; _jzqc=1; _jzqckmp=1; bfd_session_id=bfd_g=8110c81f66bcaf0f000012f7002d2bd3549a6a12&bfd_s=209502081.84399694.1424826913382; tmc=1.209502081.55227366.1424826913387.1424826913387.1424826913387"};
            #与网站构建一个连接
            conn = httplib.HTTPConnection("www.benlai.com")
            for cpage in range(1,totalpages):
                url = "http://www.benlai.com/Category/GetC3List?page="+str(cpage+1)+"&filter=&sort=0&c3SysNo="+str(SysNo)+"&startPrice=&endPrice=&_="+str(time.time())
                # log.msg('url:'+url,level=log.WARNING)
                #开始进行数据提交   同时也可以使用get进行
                conn.request(method="GET",url=url,headers=headers);#
                #返回处理后的数据
                response = conn.getresponse()
                if response.status==200:
                    res= response.read()
                    # log.msg('data %s' % res.decode("utf-8"),level=log.WARNING)#.decode("unicode-escape")
                    productlist = []
                    productlist=simplejson.loads(res.decode("utf-8"))
                    for product in productlist['Content']:
                        # log.msg('ProductLink %s' % repr(product['ProductLink']),level=log.WARNING)
                        # log.msg('ProductName %s' % repr(product["ProductName"]).decode("unicode-escape"),level=log.WARNING)
                        request = scrapy.Request("http://www.benlai.com"+product['ProductLink'],callback=self.parse_item)
                        request.meta['item'] = item
                        yield request
            #关闭连接
            conn.close();

    # def parse_ajax(self, response):
    #     data = response.body
    #     log.start(logfile='log.txt', loglevel=log.WARNING)
    #     log.msg('data %s' % repr(data).decode("utf-8"),level=log.WARNING)
        #这里写正则匹配或者选择XPathSelector获取需要捕获的数据,略
        # ajaxdata = get_data(data)
        #
        # #由于返回可能是js,可以采用python来模拟js解释器,不过这里偷懒就用json来进行转换
        # if ajaxdata:
        #     x = '{"data": "' + ajaxdata.replace('\n', '') + '"}'
        #     ajaxdata = simplejson.loads(x)['data']
        # else:
        #     ajaxdata = ''
        #
        # item = response.meta['item']
        # item['ajaxdata'] = ajaxdata
        # for key in item:
        #     if isinstance(item[key], unicode):
        #         item[key] = item[key].encode('utf8')
        # #到这里一个Item的全部元素都抓齐了,所以返回item以供保存
        # return item

    def parse_item(self, response): # 提取数据到Items里面，主要用到XPath和CSS选择器提取网页数据   parse_item
        log.start(logfile='log.txt', loglevel=log.WARNING)
        items = []
        sel = Selector(response)
        base_url = get_base_url(response)
        catalog=sel.css('div.myseatnew a')[3].xpath('text()').extract()[0]
        item = GuoShuItem()
        item['siteid'] =self.siteid
        item['sitename'] =self.sitename
        item['name'] = sel.css('div.myseatnew').xpath('//font[@id="ProductNameMenu"]/text()').extract()[0]
        # relative_url = base_url
        item['detailurl'] =base_url#urlparse.urljoin(base_url, relative_url)
        item['catalog'] = catalog
        guigep=sel.css('p.goods_gdmis.pdl15').xpath('text()').extract()
        if guigep:
            if guigep[0] !='':
                item['guige'] = guigep[0].replace("\r\n","").replace("规格：","").lstrip().rstrip()
            else:
                item['guige'] =''
        else:#http://www.benlai.com/item-36937.html
            guigelist=sel.css('div.gdproperty_n a.propon').xpath('span/text()').extract()
            if guigelist:
                item['guige'] =guigelist[0]
            else:
                item['guige'] =''
        # price =sel.xpath('//div[@id="ajax_price"]').css('p.price_n span.oldprice').xpath('text()').extract()#.css('div#ajax_price p.price_n span.newprice span')
        pricebody=sel.css('a#nav_buy_btn span').xpath('text()').extract()
        if pricebody:
            price=sel.css('a#nav_buy_btn span').xpath('text()').extract()[0]
        else:
            price=sel.css('div.fctl_font div.p-price').xpath('text()').extract()[0].replace("\r\n","").replace("￥","").lstrip().rstrip()

        # log.msg('price %s' % repr(price).decode("unicode-escape"),level=log.WARNING)
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
