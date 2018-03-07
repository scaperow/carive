#!/usr/bin/env python
# coding=utf-8

from peewee import *
from lib.dbhelper import db
import logging


# logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())


# 采集数据表
class CjData(db.Model):
    id = PrimaryKeyField()
    siteid = IntegerField(default=0)
    sitename = CharField(max_length=100, default='')
    name = CharField(max_length=500, default='')
    catalog = CharField(max_length=100, default='')
    detailurl = CharField(max_length=2000, default='')
    guige = CharField(max_length=300, default='')
    price = FloatField(default=0.0)
    danwei = CharField(max_length=30, default='')
    cjrq = CharField(max_length=30, default='')
    cjtime =IntegerField(default=0)

    class Meta:
        db_table = 'jz_scrape_data'


if __name__ == '__main__':
    #CjData.drop_table()
    CjData.create_table()
    print 'created table'
    #数据insert  1
    # item = CjData()
    # item.siteid = 1
    # item.name = u'adsfsda厅'
    # item.price = 4775.32
    # item.save()
    #数据insert  2
    # CjData.create(siteid=4)
    #数据insert  查询
    # q = CjData.select().where(CjData.siteid==1)
    # print q.count()
    # for n in q:
    #     print n.price
