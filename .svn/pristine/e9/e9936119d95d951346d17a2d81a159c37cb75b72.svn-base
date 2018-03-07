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
    res = ''
    try:
        res = urllib2.urlopen("http://www.eofan.com/admin/check_activity_order_timeout").read()

    except Exception, e:
        email = {u'receiver': ['kouzhikai@kingrocket.com','liuxiaoming@kingrocket.com'],
                 u'subject':u'系统删除秒杀超时订单错误',u'body': u"错误信息：" + e.message + res}
        create_msg(simplejson.dumps(email), 'email')