#!/usr/bin/env python
# coding=utf8

import re
from suds.client import Client
import time
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import *
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
import reportlab.rl_config

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import fonts, colors
import urllib
import urllib2
import httplib
import sys
reload(sys)
from sys import path
# path.append(r'../')
import setting

sys.setdefaultencoding('utf-8')

def setting_from_object(obj):
    setting = dict()
    for key in dir(obj):
        if key.isupper():
            setting[key.lower()] = getattr(obj, key)
    return setting


def find_subclasses(klass, include_self=False):
    accum = []
    for child in klass.__subclasses__():
        accum.extend(find_subclasses(child, True))
    if include_self:
        accum.append(klass)
    return accum


def vmobile(mobile):
    return re.match(r"1[0-9]{10}", mobile)


def vemail(email):
    return re.match(r"^(\w)+(\.\w+)*@(\w)+((\.\w{2,3}){1,3})$", email)


def sendmsg( mobile, content, isyzm):
    # client = Client(sms_url)
    if isyzm:
        sms_param = setting.SMS_PARAM_YZM.split(',')
        sms_url = sms_param[0]
        username = sms_param[1]
        pwd = sms_param[2]
        signname=sms_param[3]
        # result = client.service.SendSMSYZM(mobile, content, signtype, isyzm)
    else:
        sms_param = setting.SMS_PARAM_YX.split(',')
        sms_url = sms_param[0]
        username = sms_param[1]
        pwd = sms_param[2]
        signname=sms_param[3]
        # result = client.service.SendSMSYX(mobile, content)
    # print result
    # http://api.bjszrk.com/sdk/BatchSend.aspx?CorpID=test&Pwd=test&Mobile=13999999999&Content=ABC&Cell=&SendTime=&encode=utf-8
    content = content + '【' + signname + '】'
    values={'CorpID':username,'Pwd':pwd,'Mobile':mobile,'Content':content,'encode':'utf-8'}
    data = urllib.urlencode(values)
    req = urllib2.Request(sms_url, data)
    response = urllib2.urlopen(req)
    result = response.read()
    print result

def mkdir(path):
    import os

    try:
        path = path.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        return True
    except:
        return False


def calprice(cost, function):
    if cost and function:
        if len(function) > 0:
            s = function.replace('A', (cost.comment if cost.comment and not cost.comment == '' else '0')). \
                replace('B', str(cost.wlprice)).replace('C', str(cost.bzprice)). \
                replace('D', str(cost.rgprice)).replace('E', str(cost.shprice)).replace('F', str(cost.ccprice)). \
                replace('G', str(cost.glprice))
            result = eval(s)
            return round(result, 1)
    return None


def calpriceajax(cost, function):
    if cost and function:
        if len(function) > 0:
            s = function.replace('A', (cost['comment'] if cost['comment'] and not cost['comment'] == '' else '0')). \
                replace('B', str(cost['wlprice'])).replace('C', str(cost['bzprice'])). \
                replace('D', str(cost['rgprice'])).replace('E', str(cost['shprice'])).replace('F',
                                                                                              str(cost['ccprice'])). \
                replace('G', str(cost['glprice']))
            return eval(s)
    return None


def createpdf(orders, fname, count):
    reportlab.rl_config.warnOnMissingFontGlyphs = 0

    pdfmetrics.registerFont(TTFont('hei', 'simhei.ttf'))
    fonts.addMapping('hei', 0, 0, 'hei')
    fonts.addMapping('hei', 0, 1, 'hei')
    ts = [('FONT', (0, 0), (-1, -1), 'hei'),
          ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
          ('LEFTPADDING', (0, 0), (-1, -1), 1),
          ('RIGHTPADDING', (0, 0), (-1, -1), 1),
          ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
          ('TOPPADDING', (0, 0), (-1, -1), 3),
          ('LINEABOVE', (0, 0), (-1, 1), 0.5, colors.black),
          ('FONTSIZE', (0, 0), (-1, -1), 9)]

    ts2 = [('FONT', (0, 0), (-1, -1), 'hei'),
          ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
          ('LEFTPADDING', (0, 0), (-1, -1), 1),
          ('RIGHTPADDING', (0, 0), (-1, -1), 1),
          ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
          ('TOPPADDING', (0, 0), (-1, -1), 3),
          ('FONTSIZE', (0, 0), (-1, -1), 9)]

    phdsize= setting.PeiHuoDanSize.split(';')  #配货单打印尺寸设置 第一个数表示当前应用的是第几个尺寸
    arrsize=phdsize[int(phdsize[0])].split(',')
    width=int(arrsize[0]) #285
    height = int(arrsize[1]) #350
    doc = SimpleDocTemplate('upload/' + fname, pagesize=(width, height), leftMargin=3, rightMargin=3, topMargin=8,
                            bottomMargin=2)

    stylesheet = getSampleStyleSheet()
    stylesheet.add(ParagraphStyle(name='p', alignment=TA_JUSTIFY, fontSize=9))
    stylesheet.add(ParagraphStyle(name='hh1', alignment=TA_CENTER, fontSize=18))
    stylesheet.add(ParagraphStyle(name='td1', alignment=TA_JUSTIFY, fontSize=9, wordWrap='CJK'))

    stylesheet['hh1'].fontName = 'hei'
    stylesheet['p'].fontName = 'hei'
    stylesheet['td1'].fontName = 'hei'

    elements = []
    for o in orders:
        elements.append(Paragraph('易 凡 网 配 货 单', stylesheet['hh1']))
        elements.append(Spacer(1, 16))
        title = []
        title.append(['订单号:'+ str(o.ordernum), '日期:' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(o.ordered)))])
        table = Table(title, (133, 133), 18, ts2)
        elements.append(table)
        elements.append(Spacer(1, 3))

        data = []
        data.append(['名称（规格）', '单价', '数量', '小计'])
        for item in o.items:
            if item.item_type == 2:
                gift = u'(积分换购)'
            elif item.item_type == 9:
                gift = u'(赠品)'
            else:
                gift = ''
            if item.product_standard_name:
                td = [Paragraph(item.product.name+u'('+item.product_standard_name+u')'+gift, stylesheet['td1']), item.price,
                         item.quantity, item.quantity * item.price]
            else:
                td = [Paragraph(item.product.name+u'('+item.product_standard.name+u')'+gift, stylesheet['td1']), item.price,
                         item.quantity, item.quantity * item.price]
            # styleTd  = Paragraph(td[0], stylesheet['BodyText'])
            data.append(td)
        table = Table(data, (176, 30, 30, 30), 18, ts)
        elements.append(table)
        elements.append(
            flowables.Preformatted('-----------------------------------------------------------', stylesheet['p']))
        elements.append(Spacer(1, 3))

        total = []
        total.append(['商品费用(元):'+ str(o.price), '物流费用(元):' + str(o.shippingprice)])
        total.append(['本次优惠(元):'+ str(o.price + o.shippingprice - o.currentprice), '合计(元):' + str(o.currentprice)])

        if o.payment == 0:
            collect_price = o.currentprice - o.pay_balance
        else:
            collect_price = 0
        total.append(['使用余额(元):'+  str(o.pay_balance), '代收金额(元):' + str(collect_price)])

        table2 = Table(total, (133, 133), 18, ts2)
        elements.append(table2)
        elements.append(Spacer(1, 3))
        elements.append(
            flowables.Preformatted('-----------------------------------------------------------', stylesheet['p']))
        elements.append(Spacer(1, 3))
        elements.append(
            flowables.Preformatted(u'客户：' + o.take_name + u' (' + o.take_tel + u')', stylesheet['p']))
        elements.append(Spacer(1, 3))
        elements.append(
            flowables.Preformatted(u'地址：' + o.take_address,
                                   stylesheet['p']))
        elements.append(flowables.PageBreak())

    doc.build(elements)


def exportcsv(orders, fname, tel):
    f = open('upload/' + fname, 'w')
    #重量自动通过订单计算，代收款
    try:
        f.write(u'工作单号,客户单号,品名,原包装,受理人,件数,重量,结算方式,体积,配载要求,到达地,委托人,委托单位,委托地址,'
                u'委托电话,委托传真,委托手机,收货人,收货单位,收货地址,收货人电话,收货人传真,收货人手机,签收是否反馈,'
                u'签单返回要求,保险类型,保险费,声明价值,包装要求,代收款,到付款,重要提示,是否COD,是否可操作,是否可操作COD,'
                u'委托人邮编,委托人国家或地区,收货人邮编,收货人国家,货物的详细描述,原产地国家,海关编码,海关申报总值,'
                u'币种\n'.encode('gb18030') )
        dvnumbers = []
        grouporders = []
        for o in orders:
            pay = 0
            if o.group_orders.count() > 0:
                grouporders.append(o)
            else:
                if o.payment == 0:
                    pay = o.currentprice-o.pay_balance
                weight = sum([n.product_standard.weight*n.quantity for n in o.items])/1000.0

                line = (o.deliverynum if o.deliverynum else u'') + u','+ o.ordernum + u',食品,纸箱,三桥营业厅,1,'+str(weight)+\
                       u',月结,1*1*1*1,无,陕西,车装甲,宅急送,立丰国际407,'+tel+u',,,' + \
                       o.take_name + u',,'+ o.take_address + u',' + o.take_tel + u',,' + \
                       o.address.mobile + u',否,无,不保险,0,0,,'+str(pay)+u',0,' + o.message + u' ('+o.distributiontime+u') '+tel+u',否,否,否,' \
                       u',,,,,,,,,\n'
                f.write(line.encode('gb18030'))

        for o in grouporders:
            if dvnumbers.count(o.deliverynum) == 0:
                dvnumbers.append(o.deliverynum)
        for n in dvnumbers:
            suborders = [o for o in grouporders if o.deliverynum == n]
            mainorder = suborders[0]
            pay = 0
            weight = 0
            msg = u''
            for o in suborders:
                if o.payment == 0:
                    pay += o.currentprice-o.pay_balance
                msg = msg + u' ' + o.message
                weight += sum([n.product_standard.weight*n.quantity for n in o.items])/1000.0

            line = (mainorder.deliverynum if mainorder.deliverynum else u'') + u','+ mainorder.ordernum + u',食品,纸箱,三桥营业厅,1,'+str(weight)+\
                       u',月结,1*1*1*1,无,陕西,车装甲,宅急送,立丰国际407,'+tel+u',,,' + \
                       mainorder.take_name + u',,'+ mainorder.take_address + u',' + mainorder.take_tel + u',,' + \
                       mainorder.take_tel + u',否,无,不保险,0,0,,'+str(pay)+u',0,' + msg + u' '+tel+u',否,否,否,' \
                       u',,,,,,,,,\n'
            f.write(line.encode('gb18030'))
    except:
        pass
    finally:
        f.close()


#业务对接数据csv导出
def exportbizcsv(orders, fname, tel):
    f = open('upload/' + fname, 'w')
    #重量自动通过订单计算，代收款
    try:
        f.write(u'工作单号,业务通知单号,品名,原包装,实际包装,件数,实际重量,结算方式,体积(尺寸),配载要求,到达地,是否COD,'
                u'快普类型,产品时限,客户编号,寄件人,寄件单位,合同时限,寄件人地址,寄件人传真,寄件人电话,寄件人手机,'
                u'专项报价编号,收货人,收货单位,收货地址,收货人电话,收货人传真,收货人手机,节假日是否收货,签收是否反馈,'
                u'签单返回要求,保险类型,保险费,声明价值,包装要求,包装费,处理方式,代收款,到付款,重要提示,'
                u'客户单号,计费件数(原件数),收货签收人(收货客户)\n'.encode('gb18030') )
        dvnumbers = []
        grouporders = []
        for o in orders:
            pay = 0
            if o.group_orders.count() > 0:
                grouporders.append(o)
            else:
                if o.payment == 0:
                    pay = o.currentprice-o.pay_balance
                weight = sum([n.product_standard.weight*n.quantity for n in o.items])/1000.0

                line = (o.deliverynum if o.deliverynum else u'') + u','+ o.ordernum + u',食品,纸箱,纸箱,1,'+str(weight)+\
                       u',月结,1*1*1*1,无,陕西,否,,,客户编号,车装甲,车装甲,,立丰国际407,,'+tel+u',,,' + \
                       o.take_name + u',,'+ o.take_address + u',' + o.take_tel + u',,' + \
                       o.address.mobile + u',是,是,,不保险,0,0,,,,'+str(pay)+u',0,' + o.message + u' ('+o.distributiontime+u') '+tel+u',,1,\n'
                f.write(line.encode('gb18030'))

        for o in grouporders:
            if dvnumbers.count(o.deliverynum) == 0:
                dvnumbers.append(o.deliverynum)
        for n in dvnumbers:
            suborders = [o for o in grouporders if o.deliverynum == n]
            mainorder = suborders[0]
            pay = 0
            weight = 0
            msg = u''
            for o in suborders:
                if o.payment == 0:
                    pay += o.currentprice-o.pay_balance
                msg = msg + u' ' + o.message
                weight += sum([n.product_standard.weight*n.quantity for n in o.items])/1000.0

            line = (mainorder.deliverynum if mainorder.deliverynum else u'') + u','+ mainorder.ordernum + u',食品,纸箱,纸箱,1,'+str(weight)+\
                       u',月结,1*1*1*1,无,陕西,否,,,客户编号,车装甲,车装甲,,立丰国际407,,'+tel+u',,,' + \
                       mainorder.take_name + u',,'+ mainorder.take_address + u',' + mainorder.take_tel + u',,' + \
                       mainorder.take_tel + u',是,是,,不保险,0,0,,,,'+str(pay)+u',0,' + msg + u' '+tel+u',,1,\n'
            f.write(line.encode('gb18030'))
    except:
        pass
    finally:
        f.close()


#导出Order数据
def exportorders(orders, fname):
    f = open('upload/' + fname, 'w')
    try:
        f.write(u'订单号,用户账户,下单时间,订单详情,订单金额,运费,支付方式,收货方信息,订单状态,配送时间,备注,收件人,有效单数,物流运单号\n'.encode('gb18030') )

        for o in orders:
            items = u''
            for item in o.items:
                items = items + item.product.name + u' X ' + str(item.quantity) + u' '
            pay = u''
            if o.payment == 0:
                pay = u'货到付款'
            elif o.payment == 1:
                pay = u'支付宝'
            elif o.payment == 2:
                pay = u'账户余额'
            elif o.payment == 3:
                pay = u'网银支付'
            elif o.payment == 9:
                pay = u'补单'
            s = u''
            if o.status==0 and o.payment==1:
                s = u'待付款'
            elif o.status==1 or (o.status==0 and o.payment==0):
                s = u'待处理'
            elif o.status==2:
                s = u'正在处理'
            elif o.status==3:
                s = u'已发货'
            elif o.status==4:
                s = u'已完成'
            elif o.status==5:
                s = u'已取消'
            d_num = u''
            if o.deliverynum:
                d_num = str(o.deliverynum)
            else:
                d_num = u'无运单号'

            line = o.ordernum + u','+str(o.user.username)+u',' + \
                   time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(o.ordered)) + u',' + \
                   items + u',' + str(o.currentprice) + u',' + str(o.shippingprice) + u',' + pay + \
                   u',' + o.take_address + u' ' + o.take_name + u' ' + o.take_tel + u',' + s + \
                    u',' + o.distributiontime + u',' + o.message + u',' + o.take_name + u',' + str(o.trade_no) + u',' + d_num + u'\n'
            f.write(line.encode('gb18030'))

    except Exception, e:
        print e
    finally:
        f.close()


#导出SKU数据
def exportsku(skus, fname,title):
    f = open('upload/' + fname, 'w')
    try:
        f.write((title + u'SKU导出数据['+time.strftime("%Y-%m-%d",time.localtime(int(time.time())))+u']\n').encode('gb18030') )
        f.write(u'产品,规格,提取规格,库存量（斤）,份数,需采购量（斤）\n'.encode('gb18030') )

        for s in skus:

            line = s.name + u'(SKU:'+s.sku+u'),'+s.standards[0].name+u',' + \
                   str(s.standards[0].weight) + u',' + str(s.quantity1) + u',' + \
                   str(s.quantity) + u',' + str(((s.quantity * s.standards[0].weight) / 500) - s.quantity1) + u'斤\n'
            f.write(line.encode('gb18030'))

    except Exception, e:
        print e
        pass
    finally:
        f.close()

#按列表导出SKU数据
def exportskulist(skus, fname,title):
    f = open('upload/' + fname, 'w')
    try:
        f.write((title + u'SKU导出数据['+time.strftime("%Y-%m-%d",time.localtime(int(time.time())))+u']\n').encode('gb18030') )
        f.write(u'产品,规格,提取规格,库存量（斤）,份数,需采购量（斤）\n'.encode('gb18030') )

        for s in skus:

            line = s["name"] + u'(SKU:'+s["sku"]+u'),'+s["standard_name"]+u',' + \
                   str(s["standard_weight"]) + u',' + str(s["quantity1"]) + u',' + \
                   str(s["quantity"]) + u',' + str(((s["quantity"] * s["standard_weight"]) / 500) - s["quantity1"]) + u'斤\n'
            f.write(line.encode('gb18030'))

    except Exception, e:
        print e
        pass
    finally:
        f.close()

#按列表导出SKU数据
def exportinventoryorders(skus, fname,title,message):
    # import codecs
    # f = open('upload/' + fname, 'w','utf-8')
    f = open('upload/' + fname, 'w')
    try:
        # title=u"品相不好，6.5¥特价处理"
        # f.write((title + u'\n').encode('utf-8') )# 枫林绿洲产品清单【2015-7-5】
        f.write((title + u'\n' ).encode("gb18030"))# 枫林绿洲产品清单【2015-7-5】
        f.write((u'留言:'+message + u'\n').encode('gb18030') )# 留言:
        f.write(u'产品,规格,提取规格,数量,单位\n'.encode('gb18030') )

        for s in skus:

            line = s["name"] + u'(SKU:'+s["sku"]+u'),'+s["standard_name"]+u',' + \
                   str(s["standard_weight"]) + u',' + \
                   str(s["quantity"]) +u','+s['unitname']+ u'\n'
            f.write(line.encode('gb18030'))

    except Exception, e:
        print e
        pass
    finally:
        f.close()
if __name__ == '__main__':
    try:
        # client = Client('http://115.29.206.137:8081/MyService.svc?wsdl')
        #result = client.service.SendSMSYZM('18189279827',u'测试内容123321','0','1')
        # sendmsg( '15339212227,18189279827', '测试车装甲短信1', 1)
        # sendmsg( '15339212227,13468708870', '测试车装甲短信0', 0)
        print 'ok'
    except Exception, e:
        print e



#导出用户评论信息
def exportcomment(comment, fname):
    f = open('upload/' + fname, 'w')
    try:
        f.write(u'用户账户,评论商品,质量得分,发货速度,价格得分,服务得分,评价内容,提交时间,审核状态,回复内容,回复时间\n'.encode('gb18030') )

        for o in comment:
            status = u''
            if o.status == 0:
                status = u'已删除'
            elif o.status == 1:
                status = u'未审核'
            elif o.status == 2:
                status = u'审核通过'
            elif o.status == 3:
                status = u'拒绝通过'
            reply_date = u''
            if o.reply_time > 0:
                reply_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(o.reply_time))
            reply_content = u''
            if o.reply_content:
                reply_content = o.reply_content.replace('\n','')
                reply_content = reply_content.replace('\r','')
            comment = u''
            if o.comment:
                comment = o.comment.replace('\n','')
                comment = comment.replace('\r','')
            line = o.user.username + u','+ o.product.name+u',' + \
                   str(o.qualityscore) + u',' + str(o.speedscore) + u',' + str(o.pricescore) + u',' + \
                   str(o.servicescore) + u',' + comment + u',' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(o.created)) + \
                   u',' + status + u',' + reply_content + u',' + reply_date + u'\n'
            f.write(line.encode('gb18030'))

    except Exception, e:
        print e
    finally:
        f.close()

def export_user_csv(users, fname):
    f = open('upload/' + fname, 'w')
    try:
        f.write(u'登录名,注册时间,最后登陆时间,注册来源,有效单数,用户积分,账户余额,生日,昵称\n'.encode('gb18030'))
        for o in users:
            phoneactived = u''
            if o.phoneactived == 0:
                phoneactived = u'网站注册'
            elif o.phoneactived == 1:
                phoneactived = u'手机端注册'

            signuped = u''
            if o.signuped > 0:
                signuped = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(o.signuped))
            lsignined = u''
            if o.lsignined > 0:
                lsignined = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(o.lsignined))
            line = o.username + u','+ signuped + u',' + \
                   lsignined + u',' + phoneactived + u',' + str(o.order_count) + u',' + \
                   str(o.score) + u',' + str(o.balance) + u',' + str(o.birthday or '') + \
                   u',' + o.nickname  + u'\n'
            f.write(line.encode('gb18030'))

    except Exception, e:
        print e
    finally:
        f.close()
def export_user_csv(users, fname):
    f = open('upload/' + fname, 'w')
    try:
        f.write(u'登录名,注册时间,最后登陆时间,注册来源,有效单数,用户积分,账户余额,生日,昵称\n'.encode('gb18030'))
        for o in users:
            phoneactived = u''
            if o.phoneactived == 0:
                phoneactived = u'网站注册'
            elif o.phoneactived == 1:
                phoneactived = u'手机端注册'

            signuped = u''
            if o.signuped > 0:
                signuped = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(o.signuped))
            lsignined = u''
            if o.lsignined > 0:
                lsignined = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(o.lsignined))
            line = o.username + u','+ signuped + u',' + \
                   lsignined + u',' + phoneactived + u',' + str(o.order_count) + u',' + \
                   str(o.score) + u',' + str(o.balance) + u',' + str(o.birthday or '') + \
                   u',' + o.nickname  + u'\n'
            f.write(line.encode('gb18030'))

    except Exception, e:
        print e
    finally:
        f.close()


def export_product_csv(products, fname):
    f = open('upload/' + fname, 'w')
    try:
        f.write(u'商品ID,商品名称,SKU,规格（克）,当前库存（斤）,是否上架\n'.encode('gb18030'))
        for o in products:
            status = u''
            if o.status == 1:
                status = u'上架'
            elif o.status == 2:
                status = u'下架'
            elif o.status == 0:
                status = u'删除'
            line = str(o.id) + u','+ o.name + u'(sku:'+ str(o.sku) + u'),' + \
                   str(o.sku) + u',' + str(o.total_loss) + u',' + str(o.quantity) + u',' + status + u'\n'
            f.write(line.encode('gb18030'))

    except Exception, e:
        print e
    finally:
        f.close()

def export_price_csv(products, fname):
    f = open('upload/' + fname, 'w')
    try:
        f.write(u'商品ID,商品名称,SKU,规格,提取规格（克）,当前价格（斤）,当前价格（份）,本次采购价（斤）,毛利率\n'.encode('gb18030'))
        for p in products:
            if p['current_unitprice']:
                m = round(((p['currentprice'] - p['current_unitprice']) /p['currentprice'] * 100),2)
                line = str(p['id']) + u','+ p['name'] + u',' + \
                       u'sku:'+ str(p['sku']) + u',' + p['standard'] + u',' + str(p['weight']) + u',' + str(p['currentprice']) + u',' +\
                       str(p['currentpreprice']) + u',' + str(p['current_unitprice']) + u',' + str(m) + u'\n'
            else:
                line = str(p['id']) + u','+ p['name'] + u',' + \
                       u'sku:'+ str(p['sku']) + u',' + p['standard'] + u',' + str(p['weight']) + u',' + str(p['currentprice']) + u',' +\
                       str(p['currentpreprice']) + u',' + str('') + u',' + str('0') + u'\n'
            f.write(line.encode('gb18030'))

    except Exception, e:
        print e
    finally:
        f.close()