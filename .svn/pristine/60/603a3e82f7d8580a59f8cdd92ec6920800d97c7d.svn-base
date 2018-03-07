# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import sys
from model import CjData
from scrapy import log
import scrapy
import time

reload(sys)
sys.setdefaultencoding('utf8')

class GuoshucjPipeline(object):
    def __init__(self):
        scrapy.log.start(logfile='log.txt', loglevel=log.WARNING)

    def process_item(self, item, spider):
        cjdb= CjData()
        cjdb.cjtime=int(time.time())
        cjdb.cjrq=time.strftime('%Y-%m-%d', time.localtime(time.time()))
        detailurl=''
        name=''
        sitename=''
        catalog=''
        guige=''
        price=0.0
        danwei=''
        siteid=0
        for i in range(len(item)):
            vv=item.values()[i]
            if item.keys()[i]=='detailurl':
                detailurl=str(vv).lower()
            elif item.keys()[i]=='price':
                price=vv
            elif item.keys()[i]=='danwei':
                danwei=vv
            elif item.keys()[i]=='name':
                name=vv
            elif item.keys()[i]=='sitename':
                sitename=vv
            elif item.keys()[i]=='siteid':
                siteid=int(vv)
            elif item.keys()[i]=='catalog':
                catalog=vv
            elif item.keys()[i]=='guige':
                guige=vv
        # log.msg("name:"+name+",siteid:"+str(siteid)+",catalog:"+catalog+",guige:"+guige,level=log.WARNING)
        q = CjData.select().where(CjData.detailurl==detailurl,CjData.cjrq==cjdb.cjrq)
        if(q.count()>0):
            for n in q:
                cjdb.id=n.id
        cjdb.detailurl=detailurl
        cjdb.price=price
        cjdb.danwei=danwei
        cjdb.name=name
        cjdb.sitename=sitename
        cjdb.siteid=siteid
        cjdb.catalog=catalog
        cjdb.guige=guige
        cjdb.save()
        return item

    # def spider_closed(self, spider):
    #     self.file.close()
    # def process_item(self, item, spider):
    #     return item

# from scrapy import signals
# import json
# import codecs
# class JsonWithEncodingTencentPipeline(object):
#
#     def __init__(self):
#         self.file = codecs.open('tencent.json', 'w', encoding='utf-8')
#
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item), ensure_ascii=False) + "\n"
#         self.file.write(line)
#         return item
#
#     def spider_closed(self, spider):
#         self.file.close(
# )