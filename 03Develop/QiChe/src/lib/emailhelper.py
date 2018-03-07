#!/usr/bin/env python
# coding=utf8

import smtplib
from email.mime.text import MIMEText
from email.header import Header


def sendemail(receiver, subject, body):
    sender = 'service@eofan.com'
    smtpserver = '127.0.0.1'

    msg = MIMEText(body, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print 'send success'


if __name__ == '__main__':
    sendemail('liuxiaoming@kingrocket.com', 'python email test 测试', '你好')
