#!/usr/bin/env python
# coding=utf8

import datetime
import urllib2
import simplejson
import logging
import time
from sys import path

path.append(r'../')
from lib.mqhelper import create_msg

if __name__ == '__main__':
    #res = urllib2.urlopen("http://127.0.0.1:8889/admin/checkwl").read()
    try:
        remoteUrl="http://admin.eofan.com" #远程 http://admin.eofan.com 本地http://127.0.0.1:8890
        res = urllib2.urlopen(remoteUrl + "/admin/check_order_timeout").read()
        result = urllib2.urlopen(remoteUrl + "/admin/change_price").read()
        resultRecompute = urllib2.urlopen(remoteUrl + "/admin/recompute_avg_quantity").read()
        email = {u'receiver': ['kouzhikai@kingrocket.com','liuxiaoming@kingrocket.com','tanliping@kingrocket.com'], u'subject':u'定时执行提醒',u'body': u"执行结果为："
                        + result.decode('utf-8') +u' 系统删除超时订单：'+ res.decode('utf-8')
                  +u' 最近7天日均销量统计：'+ resultRecompute.decode('utf-8')
        }
        create_msg(simplejson.dumps(email), 'email')
    except Exception, e:
        email = {u'receiver': ['kouzhikai@kingrocket.com','liuxiaoming@kingrocket.com','tanliping@kingrocket.com'], u'subject':u'定时执行价格错误',u'body': u"错误信息：" + e.message}
        create_msg(simplejson.dumps(email), 'email')
        file_object = open('/home/timerwl.txt', 'w+')
        file_object.writelines('cz-err = ' + e.message)
        file_object.close()