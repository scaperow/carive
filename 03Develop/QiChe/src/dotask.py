#!/usr/bin/env python
# coding=utf-8

import rabbitpy
import time
import setting
from lib.util import sendmsg
from lib.send_sms import send_sms_for_all_users
from lib.send_sms import send_sms_for_group_users
from lib.send_sms import send_jpush_for_all_users
from lib.send_sms import send_jpush_for_group_users
from lib.emailhelper import sendemail
from lib.jpushhelper import pushmsg
from lib.imgHelper import SaveAdminImage2Local
import simplejson
import logging

logger = logging.getLogger('dotask')
logger.addHandler(logging.StreamHandler())

url = 'amqp://' + setting.MQUSER + ':' + setting.MQPASSWORD + '@' + setting.MQSERVER + ':' + setting.MQPORT + '/%2f'

with rabbitpy.Connection(url) as conn:
    with conn.channel() as channel:
        logging.error('start process tasks...')
        queue = rabbitpy.Queue(channel, setting.MQQUEUENAME)
        try:
            for message in queue.consume_messages():
                try:
                    if message.properties['message_type'] == 'sms':
                        sms = simplejson.loads(message.body)
                        try:
                            logging.error(u'发送短信：('+sms['mobile'] + u')' +sms['body'])
                            sendmsg( sms['mobile'], sms['body'], sms['isyzm'])
                        except Exception, e:
                            logging.error(e.message)

                    elif message.properties['message_type'] == 'email':
                        email = simplejson.loads(message.body)
                        sendemail(email['receiver'], email['subject'], email['body'])

                    elif message.properties['message_type'] == 'all_sms':
                        sms = simplejson.loads(message.body)
                        logging.error(u'群发短信：' + sms['body'])
                        try:
                            send_sms_for_all_users(sms['body'])
                        except Exception, e:
                            logging.error(e.message)
                    elif message.properties['message_type'] == 'group_sms':
                        sms = simplejson.loads(message.body)
                        logging.error(u'分组短信：' + sms['body'])
                        try:
                            send_sms_for_group_users(sms['body'], sms['grade'])
                        except Exception, e:
                            logging.error(e.message)
                    elif message.properties['message_type'] == 'jpush':
                        pushcontent = simplejson.loads(message.body)
                        try:
                            logging.error(pushcontent['apptype'])
                            logging.error(pushcontent['body'])
                            logging.error(pushcontent['receiver'])
                            #apptype:1易凡网 2易凡网采购 3易凡网采价
                            pushmsg(pushcontent['apptype'],pushcontent['body'],pushcontent['receiver'])
                        except Exception, e:
                            logging.error(e.message)
                    elif message.properties['message_type'] == 'all_jpush':
                        sms = simplejson.loads(message.body)
                        logging.error(u'群发推送：' + sms['body'])
                        try:
                            send_jpush_for_all_users(sms['body'])
                        except Exception, e:
                            logging.error(e.message)
                    elif message.properties['message_type'] == 'group_jpush':
                        sms = simplejson.loads(message.body)
                        logging.error(u'群发推送：' + sms['body'])
                        try:
                            send_jpush_for_group_users(sms['body'], sms['grade'])
                        except Exception, e:
                            logging.error(e.message)
                    elif message.properties['message_type'] == 'img':
                        try:
                            urls = simplejson.loads(message.body)
                            for url in urls:
                                SaveAdminImage2Local(url)
                        except Exception, e:
                            logging.error('img '+e.message)
                    else:
                        str = 'unknown msg type: ' + message.properties['message_type'] + ' body:' + message.body
                        logging.error(str)
                    message.ack()
                    time.sleep(1)
                except Exception, ex:
                    logging.error(ex.message)
        except KeyboardInterrupt:
            logging.error('Exited consumer')
