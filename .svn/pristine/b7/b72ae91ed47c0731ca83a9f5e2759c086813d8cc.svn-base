#!/usr/bin/env python
#coding=utf8

import logging
from handler import BaseHandler
from lib.route import route
from lib.alipay import Alipay
import simplejson
from lib.mqhelper import create_msg
from model import User, Order, Score,Balance,OrderItem,AdminUser,PayBack,Product_Reserve, OrderItemService
from activity import user_top_up_balance,return_reserve_balance
import time
import random

@route('/alipay/topay', name='pay_topay')  # 去支付宝支付
class PayHandler(BaseHandler):
    
    def get(self):
        tn = self.get_argument("tn", None)
        subject = self.get_argument("subject", "商品购买")
        body = self.get_argument("body", "购买商品")
        price = self.get_argument("price", None)
        is_bank = self.get_argument("is_bank", '')
        if tn and price:
            price = float(price)
            alipay = Alipay(**self.settings)
            self.redirect(alipay.create_payurl(tn, subject, body, price, is_bank))
    def post(self):
        tn = self.get_argument("tn", None)
        subject = self.get_argument("subject", "商品购买")
        body = self.get_argument("body", "购买商品")
        price = self.get_argument("price", None)
        is_bank = self.get_argument("is_bank", '')
        if tn and price:
            price = float(price)
            alipay = Alipay(**self.settings)
            self.redirect(alipay.create_payurl(tn, subject, body, price, is_bank))


@route('/alipay/return', name='pay_return')  # 支付宝支付完成后跳转
class success(BaseHandler):
    def get(self):
        alipay = Alipay(**self.settings)
        
        params = {}
        ks = self.request.arguments.keys()
        
        for k in ks:
            params[k] = self.get_argument(k)
        msg = ""
        if alipay.notify_verify(params):
            tn = self.get_argument("out_trade_no", None)
            trade_no = self.get_argument("trade_no", None)
            trade_status = self.get_argument("trade_status", None)
            logging.info("return:%s - %s - %s" % (tn, trade_no, trade_status))
            
            try:
                order = None
                tn1 = tn.split(',')
                for n in tn1:
                    orders = Order.select().where(Order.ordernum == n)
                    if orders.count() > 0:
                        order = orders[0]
                    if order and order.status == 0:
                        order.status = 1
                        order.save()

                        order_Item = ''
                        cartProducts = OrderItem.select().where(OrderItem.order == order)
                        for cartproduct in cartProducts:
                            order_Item += u'名称：'+ cartproduct.product.name + u' X '+ str(cartproduct.quantity) + u'份；'
                            if cartproduct.item_type == 5:
                                pr = Product_Reserve.get(Product_Reserve.product == cartproduct.product)
                                old_quantity = pr.quantity
                                pr.quantity += cartproduct.quantity
                                pr.save()
                                if (old_quantity < pr.quantity_stage1) & (pr.quantity >= pr.quantity_stage1):
                                    return_reserve_balance(cartproduct.product.id)
                                elif (old_quantity < pr.quantity_stage2) & (pr.quantity >= pr.quantity_stage2):
                                    return_reserve_balance(cartproduct.product.id)
                        for n in cartProducts:
                            if n.product.categoryfront.type == '2':
                                sn = 1
                                for s in range(n.quantity):
                                    sn = sn + s
                                    seed = "1234567890"
                                    sa = []
                                    for i in range(12):
                                        sa.append(random.choice(seed))
                                        salt = ''.join(sa)
                                    OrderItemService.create(order_item=n.id, sn=sn, service_code=salt, service_used=0, store=order.store, user=order.user)
                        try:
                            admins = AdminUser.select().where(AdminUser.roles % '%Y%')
                            receivers = [n.email for n in admins if len(n.email)>0]
                            email = {u'receiver': receivers, u'subject':u'用户下单成功',u'body': u"支付方式：在线支付；<br/>订单编号为：" + n + u"；<br>订单金额："+ str(order.currentprice) + u"；<br>订单详情："+order_Item}
                            create_msg(simplejson.dumps(email), 'email')
                        except Exception, e:
                            print e

                alipay.send_goods_confirm_by_platform(trade_no)
                msg = "success"
                self.redirect("/cart/pay?result="+msg+"&tn=" +tn+"&price="+str(order.currentprice)+"&ptype=1")
            except Exception, ex:
                logging.error(ex)
        else:
             msg = "fail"


@route(r'/alipay/notify', name='pay_notify')  # 支付宝异步通知
class NotfiyHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass
    def post(self):
        alipay = Alipay(**self.settings)
        
        params = {}
        ks = self.request.arguments.keys()
        
        for k in ks:
            params[k] = self.get_argument(k)
            
        if alipay.notify_verify(params):
            tn = self.get_argument("out_trade_no", None)    #订单编号
            trade_no = self.get_argument("trade_no", None)  #支付宝交易号
            trade_status = self.get_argument("trade_status", None)  #交易状态
            logging.info("notify:%s - %s - %s" % (tn, trade_no, trade_status))


            buyer_email = self.get_argument("buyer_email", None) #买家支付宝帐号
            notify_time = self.get_argument("notify_time", None) #通知时间
            subject = self.get_argument("subject", None) #商品名称
            payment_type = self.get_argument("payment_type", None) #支付类型
            gmt_create = self.get_argument("gmt_create", None) #交易创建时间
            gmt_payment = self.get_argument("gmt_payment", None) #交易付款时间
            gmt_close = self.get_argument("gmt_close", None) #交易关闭时间
            refund_status = self.get_argument("refund_status", None) #退款状态
            gmt_refund = self.get_argument("gmt_refund", None) #退款时间
            seller_email = self.get_argument("seller_email", None) #卖家支付宝账号
            seller_id = self.get_argument("seller_id", None) #卖家支付宝账户号
            buyer_id = self.get_argument("buyer_id", None) #买家支付宝账户号
            price = self.get_argument("price", None) #商品单价
            total_fee = self.get_argument("total_fee", None) #Number
            quantity = self.get_argument("quantity", None) #购买数量
            body = self.get_argument("body", None) #商品描述
            is_total_fee_adjust = self.get_argument("is_total_fee_adjust", None) #是否调整总价
            use_coupon = self.get_argument("use_coupon", None) #是否使用红包买家
            error_code = self.get_argument("error_code", None) #错误代码
            bank_seq_no = self.get_argument("bank_seq_no", None) #网银流水
            out_channel_inst = self.get_argument("out_channel_inst", None) #实际支付渠道

            pay_response = {'out_trade_no': tn, 'trade_no': trade_no, 'trade_status': trade_status,
                            'buyer_email': buyer_email, 'notify_time': notify_time, 'subject': subject, 'payment_type': payment_type,
                            'gmt_create': gmt_create, 'gmt_payment': gmt_payment, 'gmt_close': gmt_close, 'refund_status': refund_status,
                            'gmt_refund': gmt_refund, 'seller_email': seller_email,'seller_id': seller_id, 'buyer_id': buyer_id,
                            'price': price, 'total_fee': total_fee, 'quantity': quantity, 'body': body, 'is_total_fee_adjust': is_total_fee_adjust,
                            'use_coupon': use_coupon, 'error_code': error_code, 'bank_seq_no': bank_seq_no, 'out_channel_inst': out_channel_inst}

            try:
                order = None
                tn = tn.split(',')
                for n in tn:
                    orders = Order.select().where(Order.ordernum == n)
                    if orders.count() > 0:
                        order = orders[0]
                    if order and order.status == 0:
                        order.status = 1
                        order.pay_account = buyer_email
                        order.trade_no = trade_no
                        order.pay_response = simplejson.dumps(pay_response)
                        order.save()

                        order_Item = ''
                        cartProducts = OrderItem.select().where(OrderItem.order == order)
                        for cartproduct in cartProducts:
                            order_Item += u'名称：'+ cartproduct.product.name + u' X '+ str(cartproduct.quantity) + u'份；'
                            if cartproduct.item_type == 5:
                                pr = Product_Reserve.get(Product_Reserve.product == cartproduct.product)
                                old_quantity = pr.quantity
                                pr.quantity += cartproduct.quantity
                                pr.save()
                                if (old_quantity < pr.quantity_stage1) & (pr.quantity >= pr.quantity_stage1):
                                    return_reserve_balance(cartproduct.product.id)
                                elif (old_quantity < pr.quantity_stage2) & (pr.quantity >= pr.quantity_stage2):
                                    return_reserve_balance(cartproduct.product.id)
                        for n in cartProducts:
                            if n.product.categoryfront.type == '2':
                                sn = 1
                                for s in range(n.quantity):
                                    sn = sn + s
                                    seed = "1234567890"
                                    sa = []
                                    for i in range(12):
                                        sa.append(random.choice(seed))
                                        salt = ''.join(sa)
                                    OrderItemService.create(order_item=n.id, sn=sn, service_code=salt, service_used=0, store=order.store, user=order.user)
                        try:
                            admins = AdminUser.select().where(AdminUser.roles % '%Y%')
                            receivers = [n.email for n in admins if len(n.email)>0]
                            email = {u'receiver': receivers, u'subject':u'用户下单成功',u'body': u"支付方式：在线支付；<br/>订单编号为：" + n + u"；<br>订单金额："+ str(order.currentprice) + u"；<br>订单详情："+order_Item}
                            create_msg(simplejson.dumps(email), 'email')
                        except Exception, e:
                            print e

            except Exception, ex:
                logging.error(ex)
            
            if trade_status == 'WAIT_SELLER_SEND_GOODS':
                alipay.send_goods_confirm_by_platform(trade_no)
            
            self.write("success")

        else:
            self.write("fail")


@route('/alipay/topay_cz', name='pay_topay_cz')  # 去支付宝充值
class PayCZHandler(BaseHandler):

    def get(self):
        tn = self.get_argument("tn", None)
        subject = self.get_argument("subject", "账户充值")
        body = self.get_argument("body", "充值")
        price = self.get_argument("price", None)

        if tn and price:
            price = float(price)
            alipay = Alipay(**self.settings)
            self.redirect(alipay.create_payurl_cz(tn, subject, body, price))


@route('/alipay/return_cz', name='pay_return_cz')  # 支付宝支付完成后跳转
class CZSuccess(BaseHandler):

    def get(self):
        alipay = Alipay(**self.settings)

        params = {}
        ks = self.request.arguments.keys()

        for k in ks:
            params[k] = self.get_argument(k)
        msg = ""
        tn = ''
        strPrice = ''
        if alipay.notify_verify(params):
            tn = self.get_argument("out_trade_no", None)
            trade_no = self.get_argument("trade_no", None)
            trade_status = self.get_argument("trade_status", None)
            strPrice = self.get_argument("total_fee", None)
            #buyer_email = self.get_argument("buyer_email", None) #买家支付宝帐号
            logging.info("return:%s - %s - %s" % (tn, trade_no, trade_status))
            uid = int(tn.split('_')[0].replace('U', ''))

            try:
                alipay.send_goods_confirm_by_platform(trade_no)
                msg = "success"
            except Exception, ex:
                logging.error(ex)
        else:
             msg = "fail"
        self.redirect("/user/success?result="+msg+"&tn=" +tn+"&price="+str(strPrice))


@route(r'/alipay/notify_cz', name='pay_notify_cz')  # 支付宝异步通知
class NotfiyCZHandler(BaseHandler):

    def check_xsrf_cookie(self):
        pass

    def post(self):
        alipay = Alipay(**self.settings)

        params = {}
        ks = self.request.arguments.keys()

        for k in ks:
            params[k] = self.get_argument(k)

        if alipay.notify_verify(params):
            tn = self.get_argument("out_trade_no", None)
            trade_no = self.get_argument("trade_no", None)
            trade_status = self.get_argument("trade_status", None)
            strPrice = self.get_argument("total_fee", None)
            #buyer_email = self.get_argument("buyer_email", None) #买家支付宝帐号
            logging.info("return:%s - %s - %s" % (tn, trade_no, trade_status))
            uid = int(tn.split('_')[0].replace('U', ''))

            try:

                log = u'充值成功 - %s' %  tn
                b = Balance.select().where(Balance.log == log)
                if b.count() == 0:
                    balance = Balance()
                    balance.user = uid
                    balance.balance = float(strPrice)
                    balance.stype = 0
                    balance.log = log
                    balance.created = int(time.time())
                    balance.save()
                    user_top_up_balance(balance)

                user = User.get(id = uid)
                self.session['user'] = user
                self.session.save()
            except Exception, ex:
                logging.error(ex)
                self.write("fail")

            if trade_status == 'WAIT_SELLER_SEND_GOODS':
                alipay.send_goods_confirm_by_platform(trade_no)

            self.write("success")
        else:
            self.write("fail")


@route(r'/alipay/pay_back/notify', name='pay_back_notify')  # 支付宝退款异步通知
class PayBackNotifyHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def post(self):
        alipay = Alipay(**self.settings)

        params = {}
        ks = self.request.arguments.keys()

        for k in ks:
            params[k] = self.get_argument(k)

        if alipay.notify_verify(params):
            batch_no = self.get_argument("batch_no", None)    # 退款批次号
            try:
                pay_backs = PayBack.select().where(PayBack.batch_no == batch_no)
                if pay_backs.count() > 0:
                    pay_back = pay_backs[0]
                    if pay_back.status == 0:  # 等待退款
                        pay_back.status = 1
                        pay_back.pay_response = simplejson.dumps(params)
                        pay_back.save()
                        try:
                            admins = AdminUser.select().where(AdminUser.roles % '%Y%')
                            receivers = [n.email for n in admins if len(n.email)>0]
                            email = {u'receiver': receivers, u'subject':u'用户退款成功',
                                     u'body': u"退款订单编号为：" + pay_back.order.ordernum +
                                              u"；<br>退款金额："+ str(pay_back.price) + u"；"}
                            create_msg(simplejson.dumps(email), 'email')
                        except Exception, e:
                            print e

            except Exception, ex:
                logging.error(ex)
            self.write("success")
        else:
            self.write("fail")
