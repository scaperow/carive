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
    try:
        res = urllib2.urlopen("http://admin.eofan.com/admin/checkwl").read()
        #o_result = urllib2.urlopen("http://www.eofan.com/admin/change_order_status").read()
    except Exception, e:
        #email = {u'receiver': ['kouzhikai@kingrocket.com','liuxiaoming@kingrocket.com'], u'subject':u'定时执行提醒',u'body': u"执行结果为：" + res.decode('utf-8')}
        email = {u'receiver': ['kouzhikai@kingrocket.com','liuxiaoming@kingrocket.com'], u'subject':u'定时执行物流出错',u'body': u"错误信息：" + e.message}
        create_msg(simplejson.dumps(email), 'email')
        file_object = open('/home/timerwl.txt', 'w+')
        file_object.writelines('cz-err = ' + e.message)
        file_object.close()
