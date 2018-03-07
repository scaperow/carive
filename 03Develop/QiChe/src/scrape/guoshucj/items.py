# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field


class GuoShuItem(Item):
    siteid = Field()                # 采集站点
    sitename = Field()                # 站点名称
    name = Field()                # 果蔬名称
    catalog = Field()             # 果蔬分类
    detailurl = Field()             # 采集地址
    guige = Field()        # 规格
    price = Field()       # 价格
    danwei = Field()       # 价格
