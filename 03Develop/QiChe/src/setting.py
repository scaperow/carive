#!/usr/bin/env python
# coding=utf8

DEBUG = True
GZIP = True
SYNCIMG = False  # 置为True表示需要将后台上传的图片同步到产品前端服务器

DB_HOST = '182.92.188.59'   #182.92.188.59  192.168.1.11
DB_PORT = 3306
DB_USER = 'magento' #root  magento
DB_PASSWD = '1q2w3e4r'
DB_NAME = 'qiche'
MAX_CONNECTIONS = 100 # mysql 连接池最大数量
STALE_TIMEOUT = 20 # mysql 连接池回收时间

MEMCACHE_HOST = '182.92.188.59:11211'

ADMIN_PAGESIZE = 20
USER_PAGESIZE = 10

SMS_URL = 'http://api.bjszrk.com/sdk/BatchSend.aspx'
SMS_PARAM_YZM = 'http://api.bjszrk.com/sdk/BatchSend.aspx,SDK2731,123456@xajz,车装甲' # 验证码短信发送参数
SMS_PARAM_YX = 'http://api.bjszrk.com/sdk/BatchSend.aspx,NSZ2739,123456@xajz,车装甲' # 营销短信发送参数

WEIBO_KEY = ''
WEIBO_SECRET = ''
WEIBO_REDIRECT = 'http://www.xxx.com/oauth/weibo'

ALIPAY_KEY = '84w66i6ugwmzz29fwvnpy0phgy9na6r1' #h42bxscsm77npyq7v8x4erfit31vrhq4
ALIPAY_INPUT_CHARSET = 'utf-8'
ALIPAY_PARTNER = '2088021073686214'                 #2088511883511290
ALIPAY_SELLER_EMAIL = '1169261890@qq.com'          #pay@kingrocket.com
ALIPAY_SIGN_TYPE = 'MD5'
ALIPAY_AUTH_URL = 'http://127.0.0.1:8889/oauth/alipay_return'
ALIPAY_RETURN_URL = 'http://127.0.0.1:8889/alipay/return'
ALIPAY_NOTIFY_URL = 'http://127.0.0.1:8889/alipay/notify'
ALIPAY_RETURN_CZ_URL = 'http://127.0.0.1:8889/alipay/return_cz'
ALIPAY_NOTIFY_CZ_URL = 'http://127.0.0.1:8889/alipay/notify_cz'
ALIPAY_SHOW_URL = ''
ALIPAY_TRANSPORT = 'https'
ALIPAY_RETURN_PAY_NOTIFY_URL = 'http://127.0.0.1:8889/alipay/pay_back/notify'

COM_TEL='400-967-6558' #客服热线

MQSERVER = '123.56.94.179'
MQPORT = '5672'
MQUSER = 'guest'
MQPASSWORD='guest1'
MQEXCHANGENAME='eofan_exchange'
MQQUEUENAME='eofan_queue'
MQROUTINGKEY = 'eofan_routing_key'

PriceHistoryUrl='http://www.eofan.com:8887/pricehistory' #同行业其它网站价格连接

Balance_End_Date='2015-04-20'  #余额充值返现活动 截止时间
Balance_Max_Price='100'         #余额充值返现活动 最高返现金额  正允许为正整数
Old_New_User_Rate='0.30'        #老推新首单返利利率  0.30代表30%，最大为1
Old_New_Max_Price='90000'       #老推新首单返利 最大金额，如：订单金额为x 返利金额 = (x*0.30)>50?50:(x*0.30)

FreeshippingFee='59'          #满多少包邮
ShippingFee='0'               #邮费

CheckInScore ='10,10,10,10,10,10,10,10,10,100,10'  #连续签到天数对应积分
PeiHuoDanSize='2;285,285;285,350;285,435;' #配货单打印尺寸设置 第一个数表示当前应用的是第几个尺寸,从1开始 285,285表示100*100;285,350表示100*120;285,435表示100*150
BaiDuMapAK='OZGvYvXFQM8H0pSb9Ts7nUtw'

Is_Start = 0                # 活动是否开启满减活动 1启动 0停止
Full_Price = '98'          # 满减活动 满多少元
Reduce_Price = '10'        # 满减活动 减多少元
