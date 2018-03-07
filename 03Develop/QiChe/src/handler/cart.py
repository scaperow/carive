#!/usr/bin/env python
#coding=utf8

import logging
from handler import BaseHandler, UserBaseHandler
from lib.route import route
import simplejson
from lib.mqhelper import create_msg
from model import Cart,Product,ProductStandard,ProductPic,UserAddr,Order,OrderItem,Coupon,CouponTotal,Balance,User,\
    UserVcode,Invoicing,AdminUser,Gift,Product_Activity,Product_Reserve, OrderItemService
import time
import copy
from bootloader import db
from activity import check_activity,return_reserve_balance
import tornado.gen
from tornado.concurrent import run_on_executor
# 这个并发库在python3自带在python2需要安装sudo pip install futures
from concurrent.futures import ThreadPoolExecutor
import tornado.web
import setting
import random

@route(r'/cart/show', name='show') #我的购物车详情页
class ShowHandler(BaseHandler):
    def get(self):
        user = self.current_user
        client_car = self.get_secure_cookie('car',None)
        list = []
        carproduct = {'name':'','price':0,'oprice':0,'quantity':0,'imgurl':'','pid':0,'standardname':'','sku':'',
                      'status':1,'psid':'','is_activity':0, 'gid': 0, 'store_name': '', 'poid': '', 'standard': ''}
        carItems = []
        giftItems = []
        itemCount = 0
        is_activity = 0
        is_start = setting.Is_Start
        full_price = setting.Full_Price
        reduce_price = setting.Reduce_Price
        free_shipping = setting.FreeshippingFee
        is_reserve = 0

        if client_car:
            carItems= simplejson.loads(client_car)
        if user:
            for pro in carItems:
                cart = Cart.select().where((Cart.user == user.id) & (Cart.product == pro['pid']))  # & (Cart.type != 2)
                if cart.count() > 0:
                    cart[0].quantity += int(pro['quantity'])
                    cart[0].save()
                else:
                    c1 = Cart()
                    c1.user = user.id
                    c1.product = pro['pid']
                    c1.product_standard = pro['psid']
                    c1.quantity = pro['quantity']
                    c1.type = pro['type']
                    c1.save()
            cartitems = Cart.select().where(Cart.user == self.current_user.id)  # & (Cart.type != 2)
            self.clear_cookie('car')
            for i in cartitems:
                if i.type == 2:
                    is_reserve = 1
                c = copy.deepcopy(carproduct)
                c['name'] = i.product.name
                quantity = self.application.session_store.get_session('psid_'+ str(i.product_standard.id),'')
                if quantity > 0:
                    pa = check_activity(i.product.id)
                else:
                    pa = None
                if pa:
                    c['price'] = pa["price"]
                    c['quantity'] = 1
                    c['is_activity'] = 1
                    is_activity = 1
                else:
                    if i.type == 3 and i.product_offline:
                        c['price'] = i.product_offline.price
                        c['store_name'] = i.product_offline.store.name
                        c['poid'] = i.product_offline.id
                        c['weight'] = str(int(i.product_offline.weight * 1000)) + '克'
                    elif i.type == 2:
                        pr = Product_Reserve.select().where(Product_Reserve.product_standard == i.product_standard)
                        if pr.count() > 0:
                            c['price'] = pr[0].price
                    else:
                        if user.grade == 0:
                            c['price'] = i.product_standard.price
                        elif user.grade == 1:
                            c['price'] = i.product_standard.ourprice
                        elif user.grade == 1:
                            c['price'] = i.product_standard.pf_price
                    c['quantity'] = i.quantity
                c['oprice'] = i.product_standard.orginalprice * i.product_standard.weight / 500
                c['standardname'] = i.product_standard.name
                c['psid'] = i.product_standard.id
                c['imgurl'] = i.product.cover
                c['pid'] = i.product.id
                c['sku'] = i.product.sku
                if i.product.status == 1 and i.product.xgtotalnum > 0 and i.product.xgperusernum > 0:
                    c['status'] = 1
                elif i.product.status == 1 and i.product.xgtotalnum == 0 and i.product.xgperusernum == 0:
                    c['status'] = 1
                else:
                    c['status'] = 2
                if i.product.store:
                    c['store_name'] = i.product.store.name
                list.append(c)
                itemCount += 1
            current_time = time.strptime(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),'%Y-%m-%d %H:%M:%S')
            giftitem =  Gift.select().where((Gift.user == self.current_user.id) & (Gift.status == 0) & (Gift.end_time > time.mktime(current_time)))
            for i in giftitem:
                c = copy.deepcopy(carproduct)
                c['name'] = i.product.name
                c['price'] = 0.0
                c['quantity'] = i.quantity
                c['oprice'] = i.product_standard.orginalprice * i.product_standard.weight / 500
                c['standardname'] = i.product_standard.name
                c['psid'] = i.product_standard.id
                c['imgurl'] = i.product.cover
                c['pid'] = i.product.id
                c['sku'] = i.product.sku
                c['is_activity'] = 1
                c['gid'] = i.id
                if i.product.status==1:
                    c['status'] = 1
                else:
                    c['status'] = 2
                if i.product.store:
                    c['store_name'] = i.product.store.name
                giftItems.append(c)
                itemCount += i.quantity
        else:
            for i in carItems:
                c = copy.deepcopy(carproduct)
                p = Product.get(id=i['pid'])
                ps = ProductStandard.get(id=i['psid'])

                quantity = self.application.session_store.get_session('psid_'+ str(ps.id),'')
                if quantity > 0:
                    pa = check_activity(p.id)
                else:
                    pa = None

                if pa:
                    c['price'] = pa["price"]
                    c['quantity'] = 1
                    c['is_activity'] = 1
                else:
                    c['price'] = ps.price
                    c['quantity'] = i['quantity']
                c['name'] = p.name
                c['oprice'] = ps.orginalprice * ps.weight / 500
                c['standardname'] = ps.name
                c['psid'] = ps.id
                c['imgurl'] = p.cover
                c['pid'] = i['pid']
                c['sku'] = p.sku
                # c['status'] = p.status
                if p.status==1 and p.xgtotalnum>0 and p.xgperusernum>0:
                    c['status'] = 1
                elif p.status==1 and p.xgtotalnum==0:
                    c['status'] = 1
                else:
                    c['status'] = 2
                if p.store:
                    c['store_name'] = p.store.name
                list.append(c)
                itemCount += 1
            #to do:get cookies to show
        self.render("site/cart/show.html", cartitems=list,itemCount=itemCount,gifts=giftItems, is_activity=is_activity,
                    is_start=is_start, full_price=full_price, reduce_price=reduce_price, is_reserve=is_reserve, free_shipping=free_shipping)


@route(r'/cart/confirmation', name='confirmation') #订单确认页
class ConfirmationHandler(UserBaseHandler):
    def get(self):
        self.render("site/cart/show.html")

    def post(self):
        # self.render("site/gg.html")
        # pass
        user = self.current_user
        user_balance = User.get(id = user.id)
        gids = self.get_argument('gids', '')
        pid = self.get_arguments('items', [0])
        order_type = 0
        is_start = setting.Is_Start
        full_price = setting.Full_Price
        reduce_price = setting.Reduce_Price
        distribution = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 0:0:0", time.localtime(time.time()+ 86400 * 3)), "%Y-%m-%d 0:0:0")))

        if pid or gids:
            try:
                fn = ((Cart.user == user.id) & (Cart.product << pid))
            except Exception, ex:
                self.flash(str(ex))
            cartitems = Cart.select(Cart, ProductStandard).join(ProductStandard).where(fn)

            totalPrice = 0
            list = []
            gift_list = []
            car_product = {'name':'','flag':-1,'price':0,'uid':user.id,'cover':'', 'oprice':0, 'store_name': '',
                           'quantity':0,'imgurl':'','pid':0,'standardname':'','sku':'','status':1,'psid':'',
                           'type':0, 'opid': 0, 'weight': 0}
            if pid:
                for i in cartitems:
                    c = copy.deepcopy(car_product)
                    p = Product.get(id = i.product.id)
                    ps = ProductStandard.get(id=i.product_standard.id)

                    quantity = self.application.session_store.get_session('psid_'+ str(ps.id),'')
                    if quantity > 0:
                        pa = check_activity(i.product.id)
                    else:
                        pa = None

                    if pa:
                        totalPrice += pa["price"]
                        c['price'] = pa["price"]
                        c['quantity'] = 1
                        c['flag'] = pa['flag']
                    else:
                        if i.type == 2:
                            pr = Product_Reserve.select().where(Product_Reserve.product == i.product)
                            if (pr[0].quantity >= pr[0].quantity_stage1) & (pr[0].quantity < pr[0].quantity_stage2):
                                totalPrice += pr[0].price_stage1 * i.quantity
                                c['price'] = pr[0].price_stage1
                            elif pr[0].quantity >= pr[0].quantity_stage2:
                                totalPrice += pr[0].price_stage2 * i.quantity
                                c['price'] = pr[0].price_stage2
                            else:
                                totalPrice += pr[0].price * i.quantity
                                c['price'] = pr[0].price
                            c['type'] = 5  # 对应 order_item 表中的item_type字段  5表示预售商品
                            order_type = 2
                            distribution = pr[0].delivery_time

                            c['standardname'] = ps.name
                        elif i.type == 3 and i.product_offline:
                            c['price'] = i.product_offline.price
                            c['opid'] = i.product_offline.id
                            c['store_name'] = i.product_offline.store.name
                            c['standardname'] = str(int(i.product_offline.weight*1000)) + '克'
                            totalPrice += i.product_offline.price * i.quantity
                            c['weight'] = i.product_offline.weight*1000
                        else:
                            if user.grade == 0:
                                totalPrice += float(ps.price) * float(i.quantity)
                                c['price'] = ps.price
                            elif user.grade == 1:
                                totalPrice += float(ps.ourprice) * float(i.quantity)
                                c['price'] = ps.ourprice
                            elif user.grade == 1:
                                totalPrice += float(ps.pf_price) * float(i.quantity)
                                c['price'] = ps.pf_price
                            # totalPrice += ps.price * i.quantity
                            # c['price'] = ps.price
                            c['standardname'] = ps.name
                        c['quantity'] = i.quantity
                    c['name'] = p.name
                    c['oprice'] = ps.orginalprice * ps.weight / 500
                    c['psid'] = ps.id
                    c['imgurl'] = p.cover
                    c['pid'] = i.product.id
                    c['sku'] = p.sku
                    c['status'] = p.status
                    c['cover'] = p.cover
                    c['weight'] = ps.weight
                    if p.store:
                        c['store_name'] = p.store.name
                        c['store'] = p.store.id
                    list.append(c)
            if gids:
                glist = [int(n) for n in gids.split(',')]
                fng = ((Gift.user == user.id) & (Gift.id << glist) & (Gift.status == 0))
                gift_items = Gift.select().where(fng)
                for i in gift_items:
                    c = copy.deepcopy(car_product)
                    c['price'] = 0.0
                    c['quantity'] = i.quantity
                    c['name'] = i.product.name
                    c['oprice'] = i.product_standard.orginalprice * i.product_standard.weight / 500
                    c['standardname'] = i.product_standard.name
                    c['psid'] = i.product_standard.id
                    c['imgurl'] = i.product.cover
                    c['pid'] = i.product.id
                    c['sku'] = i.product.sku
                    c['status'] = i.product.status
                    c['cover'] = i.product.cover
                    if i.product.store:
                        c['store_name'] = i.product.store.name
                        c['store'] = p.store.id
                    gift_list.append(c)

            current_time =time.strptime(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),'%Y-%m-%d %H:%M:%S')

            if list or gift_list:
                ft = (UserAddr.user == user.id) & (UserAddr.isactive == 1)
                addritems = UserAddr.select().where(ft).order_by(UserAddr.isdefault.desc(), UserAddr.id.desc())
                shopping_price = 0
                free_shipping = int(setting.FreeshippingFee)
                if totalPrice < free_shipping:
                    shopping_price = 5
                date_time = int(time.time())
                hour = time.strftime('%H', time.localtime(date_time))
                coupon = Coupon.select(Coupon, CouponTotal).join(CouponTotal).where((Coupon.user == user.id) & (Coupon.status == 1) & (CouponTotal.minprice <= totalPrice) & (Coupon.endtime > time.mktime(current_time))).order_by(CouponTotal.price.desc(),Coupon.endtime)
                self.render("site/cart/confirmation.html", addritems=addritems, cartitems=list, giftitems=gift_list,gids=gids,
                            totalPrice=totalPrice, coupon=coupon, balance=float(user_balance.balance),
                            shopping_price=shopping_price, order_type=order_type, pids=pid, hour=hour, distribution=distribution,
                            is_start=int(is_start), full_price=float(full_price), reduce_price=float(reduce_price))
            else:
                self.redirect('/cart/show')
        else:
            self.redirect('/cart/show')


@route(r'/cart/pay', name='pay')  # 订单提交
class PayHandler(BaseHandler):
    def get(self):
        result = self.get_argument("result", 'success')
        tn = self.get_argument("tn", '')
        price = float(self.get_argument("price", '0'))
        ptype = self.get_argument("ptype", '')
        orderid = self.get_argument('orderid', '0')
        oids = [int(n) for n in  orderid.split(',')]
        orders = Order.select().where(Order.id << oids)
        if orders.count() > 0:
            oNum = ''
            currentprice = 0
            payment = ''
            for n in orders:
                oNum += n.ordernum + ','
                currentprice += n.currentprice
                payment = n.payment
            tn = oNum[:-1]
            price = currentprice
            ptype = payment
        score = int(price)
        self.render("site/cart/pay.html", result=result, tn=tn, price=price, ptype=ptype, score=score)

    def post(self):
        result = {'status': 0, 'msg': ''}
        user = self.current_user
        url = self.get_argument("from", None)
        address_id = self.get_argument("address_id")    #选中的送货地址ID
        prefer_delivery_day = self.get_argument("prefer_delivery_day")    #选中送货时间
        gateway = self.get_argument("gateway")  #选中的支付方式
        message = self.get_argument("txtmessage") #订单留言
        code = self.get_argument("coupon_code") #优惠卷编码
        pid = self.get_arguments('pid',[0])
        try:
            isinvoice = self.get_argument("is_need_invoice")  #是否开发票
            invoice_type = self.get_argument("invoice_type")  #发票类型 1个人/2公司
            invoicename = self.get_argument("invoice_companyname") #发票抬头 如果是个人就默认收件人，如果是公司则获取输入内容
        except :
            pass
        shippingprice = float(self.get_argument("logistic_preference",0)) #运费价格
        totalPrice = float(self.get_argument("sub_totalPrice",0))  #订单金额
        isBalancePay = self.get_argument("balance",'') #是否使用余额支付
        hidPay = float(self.get_argument("hidPay",0)) #使用余额之后的部分
        #vcode = self.get_argument("vcode", None) #余额支付验证码
        try:
            if code:
                coupon = Coupon.get(Coupon.code == code)
                hidPay = (hidPay - coupon.coupontotal.price)
        except:
            pass
        itemCount = Cart.select().where((Cart.user == user.id) & (Cart.product << pid)).count()
        if itemCount > 0:
            userinfo = User.get(id = user.id)
            op = (totalPrice - hidPay)
            if (userinfo.balance+0.01 >= op):
                try:
                    with db.handle.transaction():
                        order = Order()
                        order.user = user.id
                        order.address = address_id
                        address = UserAddr.get(id = int(address_id))
                        order.take_name = address.name
                        order.take_tel = address.mobile +' '+address.tel
                        order.take_address = address.city+' '+address.region+' '+address.street+' '+address.address
                        if prefer_delivery_day == '':
                            order.distributiontime = '工作日/周末/假日均可'
                        elif prefer_delivery_day == 'weekend':
                            order.distributiontime = '仅周末送货'
                        elif prefer_delivery_day == 'weekday':
                            order.distributiontime = '仅工作日送货'
                        if gateway == 'COD':
                            order.payment = "0"
                        elif gateway == 'Alipay':
                            order.payment ='1'
                        elif gateway == 'Balance':
                            order.payment ='2'
                        else:
                            order.payment = '3'
                        order.message = message
                        try:
                            order.isinvoice = isinvoice
                            order.invoicesub = invoice_type
                            order.invoicename = invoicename
                            order.invoicecontent = '' #发票类型 0蔬菜 1食水果   暂时没用
                        except :
                            pass
                        order.shippingprice = shippingprice
                        order.price = totalPrice - shippingprice
                        order.ordered = int(time.time())
                        order.currentprice = totalPrice
                        order.status = 0    #订单状态 0等待付款 1付款成功 2已送货 3交易完成 4已取消,-1已删除
                        order.ip = self.request.remote_ip
                        order.order_from = 1 #网站下单
                        order.ordereddate = time.strftime('%Y-%m-%d', time.localtime(order.ordered))    #下单日期，文本格式
                        order.orderedtime = time.strftime('%H:%M:%S', time.localtime(order.ordered))    #下单时间，文本格式
                        if isBalancePay != '':
                            order.pay_balance = float(order.currentprice) - float(hidPay)
                        if order.payment == '2':
                            order.pay_balance = float(order.currentprice)
                        #order.ordered = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                        try:
                            order.save()
                            order.ordernum = 'U' + str(order.user.id) + '-S' + str(order.id)
                            order.save()
                            result['status'] = 1
                        except:
                            result['status'] = 10
                            result['msg'] = '订单保存失败'
                        cartProducts = Cart.select().where((Cart.user == user.id) & (Cart.product << pid))
                        #将订单中的产品信息存入OrderItem表中
                        body = ''
                        order_weight = 0.0
                        order_Item = ''
                        for cartproduct in cartProducts:
                            try:
                                orderItem = OrderItem()
                                orderItem.product = cartproduct.product.id
                                orderItem.order = order.id
                                orderItem.product_standard = cartproduct.product_standard.id

                                # 判断商品是否为活动商品
                                quantity = self.application.session_store.get_session('psid_'+ str(cartproduct.product_standard.id),'')
                                if quantity > 0:
                                    pa = check_activity(cartproduct.product.id)
                                else:
                                    pa = None

                                if pa:
                                    orderItem.quantity = 1
                                    orderItem.price = pa["price"]
                                    orderItem.item_type = 1     # 1表示秒杀商品
                                    try:
                                        product_active = Product_Activity.get(id = pa["id"])
                                        product_active.quantity -= 1
                                        product_active.save()
                                    except:
                                        pass

                                else:
                                    orderItem.quantity = cartproduct.quantity
                                    orderItem.price = cartproduct.product_standard.price


                                orderItem.weight = cartproduct.product_standard.weight
                                orderItem.product_standard_name = cartproduct.product_standard.name
                                orderItem.save()
                                order_weight += round((cartproduct.product_standard.weight/500 * cartproduct.quantity), 2)
                                result['status'] = 2
                                result['msg'] = 'OrderItem保存成功,产品ID：'+ str(cartproduct.product.id)
                                order_Item += u'名称：'+ cartproduct.product.name + u' X '+ str(cartproduct.quantity) + u'份；'
                                body += cartproduct.product.name + " " + cartproduct.product_standard.name + " " + str(cartproduct.quantity) + " "

                                product = Product.get(id = cartproduct.product.id)
                                product.orders = product.orders + 1
                                product.save()

                                #根据仓库 张宏伟要求，取消下单时扣除库存和用户取消订单返回库存功能 2015-03-24修改
                                '''i = Invoicing()
                                i.type = 1 #0入库，1出库
                                i.product = cartproduct.product.id
                                i.quantity = (cartproduct.product_standard.weight * cartproduct.quantity) / 500
                                i.price = cartproduct.product_standard.price * cartproduct.quantity
                                i.unitprice =cartproduct.product_standard.price
                                i.args = order.ordernum
                                i.addtime = int(time.mktime(time.strptime(time.strftime('%Y-%m-%d',time.localtime(time.time())),"%Y-%m-%d")))
                                i.save()

                                pro = Product.get(id = cartproduct.product.id)
                                ps = ProductStandard.get(id=pro.defaultstandard)
                                list = simplejson.loads(ps.relations)
                                pslist = ProductStandard.select().where(ProductStandard.id << list)
                                for n in pslist:
                                    p = Product.get(id=n.product.id)
                                    p.quantity -= (cartproduct.product_standard.weight * cartproduct.quantity) / 500
                                    p.save()
                                    #对于低于库存警戒线时报警
                                    if p.quantity < 5:
                                        body = p.name + u' 当前理论库存数量为' + str(p.quantity) + u'斤，请关注库存情况。'
                                        ausers = AdminUser.select().where((AdminUser.mobile != '') & (AdminUser.isactive == 1) & (AdminUser.roles % '%B%'))
                                        sms = {'apptype': 2, 'body': body, 'receiver': []}
                                        for au in ausers:
                                            sms['receiver'].append(au.mobile)'''

                            except Exception, e:
                                result['status'] = 20
                                result['msg'] = 'OrderItem保存失败,产品ID：'+str(cartproduct.product.id)

                        # 赠品信息 如果Gift中有该赠品信息则一并加入到该订单中
                        giftProducts = Gift.select().where((Gift.user == user.id) & (Gift.status == 0))
                        for cartproduct in giftProducts:
                            try:
                                orderItem = OrderItem()
                                orderItem.product = cartproduct.product.id
                                orderItem.order = order.id
                                orderItem.product_standard = cartproduct.product_standard.id
                                orderItem.price = 0  # 赠品价格为0
                                orderItem.item_type = 9
                                orderItem.quantity = cartproduct.quantity
                                orderItem.weight = cartproduct.product_standard.weight
                                orderItem.product_standard_name = cartproduct.product_standard.name
                                orderItem.save()
                                order_weight += round((cartproduct.product_standard.weight/500 * cartproduct.quantity), 2)

                                order_Item += u'名称：'+ cartproduct.product.name + u' X '+ str(cartproduct.quantity) + u'份；'
                                body += cartproduct.product.name + " " + cartproduct.product_standard.name + " " + str(cartproduct.quantity) + " "

                                product = Product.get(id = cartproduct.product.id)
                                product.orders = product.orders + 1
                                product.save()

                                #根据仓库 张宏伟要求，取消下单时扣除库存和用户取消订单返回库存功能 2015-03-24修改
                                '''i = Invoicing()
                                i.type = 1 #0入库，1出库
                                i.product = cartproduct.product.id
                                i.quantity = (cartproduct.product_standard.weight * cartproduct.quantity) / 500
                                i.price = cartproduct.product_standard.price * cartproduct.quantity
                                i.unitprice =cartproduct.product_standard.price
                                i.args = order.ordernum
                                i.addtime = int(time.mktime(time.strptime(time.strftime('%Y-%m-%d',time.localtime(time.time())),"%Y-%m-%d")))
                                i.save()

                                pro = Product.get(id = cartproduct.product.id)
                                ps = ProductStandard.get(id=pro.defaultstandard)
                                list = simplejson.loads(ps.relations)
                                pslist = ProductStandard.select().where(ProductStandard.id << list)
                                for n in pslist:
                                    p = Product.get(id=n.product.id)
                                    p.quantity -= (cartproduct.product_standard.weight * cartproduct.quantity) / 500
                                    p.save()
                                    #对于低于库存警戒线时报警
                                    if p.quantity < 5:
                                        body = p.name + u' 当前理论库存数量为' + str(p.quantity) + u'斤，请关注库存情况。'
                                        ausers = AdminUser.select().where((AdminUser.mobile != '') & (AdminUser.isactive == 1) & (AdminUser.roles % '%B%'))
                                        sms = {'apptype': 2, 'body': body, 'receiver': []}
                                        for au in ausers:
                                            sms['receiver'].append(au.mobile)'''
                                cartproduct.status = 1
                                cartproduct.used_time = int(time.time())
                                cartproduct.save()
                            except Exception, e:
                                result['status'] = 20
                                result['msg'] = 'OrderItem保存失败,产品ID：'+str(cartproduct.product.id)



                        order.weight = order_weight
                        if(order_weight > int(order_weight)):
                            order.freight = 5 + int(order_weight - 1.0) * 0.5 #5是首重运费，order_weight单位是斤，超过一公斤每斤加五毛，不足一斤算一斤
                        else:
                            order.freight = 5 + (order_weight - 2) * 0.5
                        order.save()
                        #保存完订单之后需要删除购物车产品
                        try:
                            Cart.delete().where((Cart.user == order.user.id) & (Cart.product << pid)).execute()
                            result['status'] = 3
                        except:
                            result['status'] = 30
                            result['msg'] = '购物车清空失败'
                        #修改优惠卷状态
                        if code != '':
                            p = Coupon.get(Coupon.code == code)
                            p.status = 2
                            p.save()
                            #更新订单中的优惠卷信息
                            order.coupon = p.id
                            order.price = round(float(order.price) + float(p.coupontotal.price),2)
                            order.save()
                        #余额历史
                        balance = Balance()
                        if order.payment == '1':    # 支付宝支付
                            if isBalancePay != '':
                                balance.user = user.id
                                balance.balance = float(order.currentprice) - float(hidPay)
                                balance.stype = 1
                                balance.log = '合并支付，订单编号：'+ order.ordernum + ' 余额支付部分金额：' + str(balance.balance)
                                balance.created = int(time.time())
                                balance.save()

                                usernew = User.get(id=user.id)
                                self.session['user'] = usernew
                                self.session.save()
                                self.redirect("/alipay/topay?tn=%s&body=%s&price=%f" % (order.ordernum, body, float(hidPay)))
                            else:
                                self.redirect("/alipay/topay?tn=%s&body=%s&price=%f" % (order.ordernum, body, float(order.currentprice)))
                        elif order.payment == '0':  # 货到付款
                            if isBalancePay != '':
                                balance.user = user.id
                                balance.balance = float(order.currentprice) - float(hidPay)
                                balance.stype = 1
                                balance.log = '合并支付，订单编号：'+ order.ordernum + ' 余额支付部分金额：' + str(balance.balance)
                                balance.created = int(time.time())
                                balance.save()

                                usernew = User.get(id=user.id)
                                self.session['user'] = usernew
                                self.session.save()
                                # 货到付款订单状态保持不变
                                order.status = 1
                                order.save()
                                self.redirect("/cart/pay?result=success&tn=" +order.ordernum+"&price="+str(order.currentprice)+"&ptype=3")
                            else:
                                try:
                                    admins = AdminUser.select().where(AdminUser.roles % '%Y%')
                                    receivers = [n.email for n in admins if len(n.email)>0]
                                    email = {u'receiver': receivers, u'subject':u'用户下单成功',u'body': u"支付方式：货到付款；<br/>订单编号为：" + order.ordernum  + u"；<br>订单金额："+ str(order.currentprice) + u"；<br>订单详情："+order_Item}
                                    create_msg(simplejson.dumps(email), 'email')
                                except Exception, e:
                                    print e
                                order.status = 1
                                order.save()
                                self.redirect("/cart/pay?result=success&tn=" +order.ordernum+"&price="+str(order.currentprice)+"&ptype=0")
                        elif order.payment == '2':  # 余额支付
                            balance.user = user.id
                            balance.balance = float(order.currentprice)
                            balance.stype = 1
                            balance.log = u'使用余额支付-订单编号：'+ order.ordernum
                            balance.created = int(time.time())
                            balance.save()

                            order.status = 1
                            order.save()

                            usernew = User.get(id=user.id)
                            self.session['user'] = usernew
                            self.session.save()
                            try:
                                admins = AdminUser.select().where(AdminUser.roles % '%Y%')
                                receivers = [n.email for n in admins if len(n.email)>0]
                                email = {u'receiver': receivers, u'subject':u'用户下单成功',u'body': u"支付方式：余额支付；<br/>订单编号为：" + order.ordernum + u"；<br>订单金额："+ str(order.currentprice) + u"；<br>订单详情："+order_Item}
                                create_msg(simplejson.dumps(email), 'email')
                            except Exception, e:
                                print e
                            self.redirect("/cart/pay?result=success&tn=" +order.ordernum+"&price="+ str(order.currentprice) +"&ptype=2")
                        elif order.payment == '3':
                            try:
                                admins = AdminUser.select().where(AdminUser.roles % '%Y%')
                                receivers = [n.email for n in admins if len(n.email)>0]
                                email = {u'receiver': receivers, u'subject':u'用户下单成功',u'body': u"支付方式：网银支付；<br/>订单编号为：" + order.ordernum + u"；<br>订单金额："+ str(order.currentprice) + u"；<br>订单详情："+order_Item}
                                create_msg(simplejson.dumps(email), 'email')
                            except Exception, e:
                                print e

                            if isBalancePay != '':
                                balance.user = user.id
                                balance.balance = float(order.currentprice) - float(hidPay)
                                balance.stype = 1
                                balance.log = '合并支付-订单编号：'+ order.ordernum + ' 余额支付部分金额：' + str(balance.balance)
                                balance.created = int(time.time())
                                balance.save()
                                usernew = User.get(id=user.id)
                                self.session['user'] = usernew
                                self.session.save()
                                self.redirect("/alipay/topay?tn=%s&body=%s&price=%f&is_bank=%s" % (order.ordernum, body, float(hidPay),gateway))
                            else:
                                self.redirect("/alipay/topay?tn=%s&body=%s&price=%f&is_bank=%s" % (order.ordernum, body, float(order.currentprice),gateway))
                except Exception, ex:
                    logging.error(ex)
            else:
                self.write("账户余额不足！")
        else:
            self.write("请勿重复提交订单，查看<a href='/user/order'>我的订单</a>")
        #self.render('site/cart/pay.html')


@route(r'/cartcontrol', name='cartcontrol')  # 前台添加到购物车ajax调用
class CartControlHandler(BaseHandler):
    def get(self):
        user = self.current_user
        client_car = self.get_secure_cookie('car', None)
        list = []
        count = 0
        totalprice = 0
        carproduct = {'name': '', 'price': 0, 'oprice': 0, 'quantity': 0, 'imgurl': '', 'pid': 0, 'standardname': '',
                      'sku': '','psid':'','is_activity':0, 'psid': 0, 'gid': 0, 'store_name': '', 'ourprice': 0, 'pf_price': 0}
        carItems = []
        giftItems = []
        if client_car:
            carItems= simplejson.loads(client_car)
        if user:
            for pro in carItems:
                cart = Cart.select().where((Cart.user == user.id) & (Cart.product == pro['pid']))  #  & (Cart.type != 2)
                if cart.count() > 0:
                    cart[0].quantity += int(pro['quantity'])
                    cart[0].save()
                else:
                    c1 = Cart()
                    c1.user = user.id
                    c1.product = pro['pid']
                    c1.product_standard = pro['psid']
                    c1.quantity = pro['quantity']
                    c1.save()
            cartitems =  Cart.select().where((Cart.user == self.current_user.id)) # & (Cart.type != 2)
            self.clear_cookie('car')
            for i in cartitems:
                c = copy.deepcopy(carproduct)
                c['name'] = i.product.name

                quantity = self.application.session_store.get_session('psid_'+ str(i.product_standard.id),'')
                if quantity > 0:
                    pa = check_activity(i.product.id)
                else:
                    pa = None

                if pa:
                    c['price'] = pa["price"]
                    c['quantity'] = 1
                    c['is_activity'] = 1
                    totalprice += float(pa["price"]) * float(i.quantity)
                else:
                    if i.type == 3 and i.product_offline:
                        c['price'] = i.product_offline.price
                        c['store_name'] = i.product_offline.store.name
                        totalprice += float(i.product_offline.price) * float(i.quantity)
                    elif i.type == 2:
                        pr = Product_Reserve.select().where(Product_Reserve.product_standard == i.product_standard)
                        if pr.count() > 0:
                            c['price'] = pr[0].price
                            totalprice += float(pr[0].price) * float(i.quantity)
                    else:
                        if user.grade == 0:
                            c['price'] = i.product_standard.price
                            totalprice += float(i.product_standard.price) * float(i.quantity)
                        elif user.grade == 1:
                            c['price'] = i.product_standard.ourprice
                            totalprice += float(i.product_standard.ourprice) * float(i.quantity)
                        elif user.grade == 1:
                            c['price'] = i.product_standard.pf_price
                            totalprice += float(i.product_standard.pf_price) * float(i.quantity)
                    c['quantity'] = i.quantity
                c['oprice'] = i.product_standard.orginalprice
                c['ourprice'] = i.product_standard.ourprice
                c['pf_price'] = i.product_standard.pf_price
                c['standardname'] = i.product_standard.name
                c['imgurl'] = i.product.cover
                c['pid'] = i.product.id
                c['sku'] = i.product.sku
                c['psid'] = i.product_standard.id
                # totalprice += float(i.product_standard.price) * float(i.quantity)
                count += int(i.quantity)
                list.append(c)
            current_time = time.strptime(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),'%Y-%m-%d %H:%M:%S')
            giftitem =  Gift.select().where((Gift.user == self.current_user.id) & (Gift.status == 0) & (Gift.end_time > time.mktime(current_time)))
            for i in giftitem:
                c = copy.deepcopy(carproduct)
                c['name'] = i.product.name
                c['price'] = 0.0
                c['quantity'] = i.quantity
                c['oprice'] = i.product_standard.orginalprice * i.product_standard.weight / 500
                c['ourprice'] = i.product_standard.ourprice
                c['pf_price'] = i.product_standard.pf_price
                c['standardname'] = i.product_standard.name
                c['psid'] = i.product_standard.id
                c['imgurl'] = i.product.cover
                c['pid'] = i.product.id
                c['sku'] = i.product.sku
                c['is_activity'] = 1
                c['gid'] = i.id
                if i.product.status==1:
                    c['status'] = 1
                else:
                    c['status'] = 2
                giftItems.append(c)
                count += i.quantity
        else:
            for i in carItems:
                c = copy.deepcopy(carproduct)
                p = Product.get(id=i['pid'])
                ps = ProductStandard.get(id=i['psid'])
                c['name'] = p.name

                quantity = self.application.session_store.get_session('psid_'+ str(ps.id),'')
                if quantity > 0:
                    pa = check_activity(i['pid'])
                else:
                    pa = None

                if pa:
                    c['price'] = pa["price"]
                    c['quantity'] = 1
                    c['is_activity'] = 1
                    totalprice += float(pa["price"]) * 1
                else:
                    c['price'] = ps.price
                    c['quantity'] = i['quantity']
                    totalprice += float(ps.price) * float(i['quantity'])
                c['oprice'] = ps.orginalprice
                c['standardname'] = ps.name
                c['imgurl'] = p.cover
                c['pid'] = i['pid']
                c['sku'] = p.sku
                c['psid'] = i['psid']
                # totalprice += float(ps.price) * float(i['quantity'])
                count += int(i['quantity'])
                list.append(c)
        return self.render("layout/mycart.html", cartitems=list,count=count, gift_items=giftItems, totalprice=totalprice)


@route(r'/cart/check', name='cartcheck')  # 订单检查页
class CartCheckHandler(UserBaseHandler):
    def get(self):
        user = self.current_user
        user_balance = User.get(id = user.id)
        onum = self.get_arguments('onum', '')
        #plist = [int(n) for n in  pid.split(',')]
        try:
            fn = ((Order.ordernum == onum) & (Order.status == 0))
            order = Order.get(fn)
            address = UserAddr.get(id=order.address)
            if onum != '':
                date_time = int(time.time())
                hour = time.strftime('%H', time.localtime(date_time))
                self.render("site/cart/check.html", order=order,
                            balance=float(user_balance.balance), address=address, err='', hour=hour)
            else:
                self.render("site/cart/order.html")
        except Exception, ex:
            #self.flash(u'订单信息不存在，请重试')
            self.redirect("/user/order")


@route(r'/cart/pay_again', name='pay_again')  # 继续支付
class PayAgainHandler(BaseHandler):
    def post(self):
        result = {'status': 0, 'msg': ''}
        user = self.current_user
        order_num = self.get_argument("formorder",None)
        prefer_delivery_day = self.get_argument("prefer_delivery_day")    #选中送货时间
        gateway = self.get_argument("gateway")  #选中的支付方式

        with db.handle.transaction():
            order = Order.get((Order.ordernum == order_num) & (Order.user == user.id))

            mscheck = True  # 检查用户今天是否秒杀过
            today_start_time = time.mktime(time.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d"))
            msItems = OrderItem.select().where((OrderItem.order == order) & (OrderItem.item_type == 1))
            if msItems.count() > 0:
                today_ms = OrderItem.select().join(Order).where((Order.status < 5) & (Order.status > 0) &
                                     (Order.user == user) & (OrderItem.item_type == 1) & (Order.ordered >= today_start_time))
                if today_ms.count() > 0:
                    mscheck = False
                    result['msg'] = u'您今天已经秒杀过产品了，每位会员每天仅能秒杀一个商品'
            if mscheck:
                items = OrderItem.select().where(OrderItem.order == order)  # & (OrderItem.item_type == 0))
                if items.count() > 0:
                    # 检查商品是否限购商品
                    # 查出该商品今天该用户购买过几次
                    # 查出该商品库存多少
                    # 当次购买需《每日限购 《库存；否则：mscheck=False
                    jrmsg = u''
                    for n in items:
                        if n.product.xgperusernum>0:
                            today_ms = OrderItem.select().join(Order).\
                                where((Order.status < 5) & (Order.status > 0) &
                                (0 == OrderItem.item_type) & (Order.ordered >= today_start_time) & (Order.user == user)
                                & (OrderItem.product_standard == n.product_standard) )
                            jrgmcs=today_ms.count()
                            if jrgmcs+n.quantity>n.product.xgperusernum:
                                mscheck = False
                                jrmsg += n.product.name+u' 超出了今日限购次数;'

                    if not mscheck:
                        result['msg'] = u'您购买的商品'+jrmsg
            if mscheck:  # 检查是否存在秒杀活动结束的商品
                now = time.time()
                activityMsg = u''
                for item in order.items:
                    if item.item_type == 1:
                        activityProducts = Product_Activity.select().where((Product_Activity.product_standard == item.product_standard) &
                                        (Product_Activity.status == 1) &
                                        (now >= Product_Activity.begin_time) & (now <= Product_Activity.end_time))
                        if activityProducts.count() == 0:
                            mscheck = False
                            activityMsg += item.product.name + u'、'

                if not mscheck:
                    result['msg'] =activityMsg[0:-1] + u'秒杀活动已经结束，感谢您的关注'
                    address = UserAddr.get(id=order.address)
                    err = result['msg']
                    self.render("site/cart/check.html", order=order,
                            balance=float(user.balance), address=address, err=err)
                else:
                    if prefer_delivery_day == '':
                        order.distributiontime = '工作日/周末/假日均可'
                    elif prefer_delivery_day == 'weekend':
                        order.distributiontime = '仅周末送货'
                    elif prefer_delivery_day == 'weekday':
                        order.distributiontime = '仅工作日送货'
                    elif prefer_delivery_day == 'morning':
                        order.distributiontime = '早上8点到11点'
                    elif prefer_delivery_day == 'noon':
                        order.distributiontime = '早上11点到下午4点'
                    elif prefer_delivery_day == 'afternoon':
                        order.distributiontime = '下午4点到7点'
                    if gateway == 'COD':
                        order.payment = "0"
                    elif gateway == 'Alipay':
                        order.payment ='1'
                    elif gateway == 'Balance':
                        order.payment ='2'
                    else:
                        order.payment = '3'
                    order.ordered = int(time.time())
                    order.ip = self.request.remote_ip
                    try:
                        order.save()
                        result['status'] = 1
                    except:
                        result['status'] = 10
                        result['msg'] = '订单保存失败'
                    # orderItems = OrderItem.select().where(OrderItem.order == order.ordernum)
                    # 将订单中的产品信息存入OrderItem表中
                    body = ''
                    # 余额历史
                    balance = Balance()
                    if order.payment == '1':
                        self.redirect("/alipay/topay?tn=%s&body=%s&price=%f" % (order.ordernum, body, round(order.currentprice - order.pay_balance, 2)))
                    elif order.payment == '0':
                        order.status = 1
                        order.save()
                        self.redirect("/cart/pay?result=success&tn=" +order.ordernum+"&price="+str(order.currentprice)+"&ptype=0")
                    elif order.payment == '2':
                        balance.user = user.id
                        balance.balance = round(order.currentprice - order.pay_balance, 2)
                        balance.stype = 1
                        balance.log = u'余额支付-订单编号：'+ order.ordernum
                        balance.created = int(time.time())
                        balance.save()

                        order.pay_balance = order.currentprice
                        order.status = 1
                        order.save()

                        usernew = User.get(id=user.id)
                        self.session['user'] = usernew
                        self.session.save()

                        for n in items:
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

                        self.redirect("/cart/pay?result=success&tn=" +order.ordernum+"&price="+ str(order.currentprice) +"&ptype=2")
                    elif order.payment == '3':
                        self.redirect("/alipay/topay?tn=%s&body=%s&price=%f&is_bank=%s" % (order.ordernum, body, round(order.currentprice - order.pay_balance, 2), gateway))
            else:
                address = UserAddr.get(id=order.address)
                err = result['msg']
                self.render("site/cart/check.html", order=order,
                        balance=float(user.balance), address=address, err=err)


@route(r'/cart/pay2nd', name='pay2nd_handler')  # 订单提交
class Pay2ndHandler(BaseHandler):
    executor = ThreadPoolExecutor(200)
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        yield self.execPay(self)

    @run_on_executor
    def execPay(self, handler):

        user = User.get(id=handler.current_user.id)
        address_id = handler.get_argument("address_id")    # 选中的送货地址ID
        prefer_delivery_day = handler.get_argument("prefer_delivery_day")    # 选中送货时间
        gateway = handler.get_argument("gateway")  # 选中的支付方式
        message = handler.get_argument("message", '')  # 订单留言
        coupon_code = handler.get_argument("coupon_code")  # 优惠卷编码
        items = handler.get_arguments('items', [])  # 普通商品集合
        msitems = handler.get_arguments('msitems', [])  # 秒杀商品集合

        isinvoice = handler.get_argument("isinvoice", '0')  # 是否开发票
        invoice_type = handler.get_argument("invoice_type", '0')  # 发票类型 1个人/2公司
        invoicename = handler.get_argument("invoicename", '')  # 发票抬头 如果是个人就默认收件人，如果是公司则获取输入内容

        shippingprice = float(handler.get_argument("shippingprice", '0'))  # 运费价格
        price = float(handler.get_argument("price", '0'))  # 订单金额
        currentprice = float(handler.get_argument("currentprice", '0'))  # 订单金额
        balance = float(handler.get_argument("balance", '0'))  # 余额支付金额
        gids = handler.get_argument("gids", '')     # 赠品ID
        storeid = int(handler.get_argument("storeid", '0'))     # 店铺id
        order_type = 0
        result = {'flag': 0, 'msg': '', 'url': '', 'orderid': 0, 'price': 0, 'tn': '', 'is_bank': ''}
        mscheck = True  # 检查用户今天是否秒杀过

        if len(items) > 0:
            items = simplejson.loads((items[0]))

        today_start_time = time.mktime(time.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d"))

        if len(items) > 0:
            # 检查商品是否限购商品
            # 查出该商品今天该用户购买过几次
            # 查出该商品库存多少
            # 当次购买需《每日限购 《库存；否则：mscheck=False
            jrmsg = u''
            for n in items:
                ps = ProductStandard.get(id=n['psid'])
                if ps.product.xgperusernum>0:
                    today_ms = OrderItem.select().join(Order).\
                        where((Order.status < 5) & (Order.status > 0) &
                        (0 == OrderItem.item_type) & (Order.ordered >= today_start_time) & (Order.user == user)
                        & (OrderItem.product_standard == n['psid']) )
                    jrgmcs=today_ms.count()
                    if ps.product.is_reserve != 1 and n['poid'] == 0:
                        if jrgmcs+n['quantity']>ps.product.xgperusernum:
                            mscheck = False
                            jrmsg += ps.product.name+u' 超出了今日限购次数;'
                        elif n['quantity']>ps.product.xgtotalnum:
                            mscheck = False
                            jrmsg += ps.product.name+u' 已经售完;'

            if not mscheck:
                result['msg'] = u'您购买的商品'+jrmsg

        if mscheck:  # 检查是否存在秒杀活动结束的商品
            now = time.time()
            activityMsg = u''

            coupon = None  # 优惠券
            is_store = None
            if storeid:
                is_store = storeid
            if coupon_code:
                coupon = Coupon.get(Coupon.code == coupon_code)
            address = UserAddr.get(id=address_id)
            psids = [n['psid'] for n in items]
            sids = [n['store'] for n in items]
            has_xiajia = Product.select().join(ProductStandard, on=(Product.defaultstandard == ProductStandard.id)). \
                    where((ProductStandard.id << psids) & (Product.store << sids) & (Product.status == 1))
            if has_xiajia.count() != len(items):
                result['msg'] = u'您的订单中包含下架商品，请重新下单'
            else:
                order_weight = 0.0
                itemList = []
                storeList = []
                # storeItem = {'weight': 0, 'price': 0, 'store_id': 1}
                for n in items:
                    ps = ProductStandard.get(id=n['psid'])
                    orderItem = OrderItem()
                    orderItem.product = ps.product.id
                    orderItem.product_standard = ps
                    orderItem.price = n['price']  # ps.price
                    orderItem.quantity = n['quantity']
                    if n['poid'] > 0:
                        orderItem.weight = n['weight']
                        orderItem.product_offline = n['poid']
                    else:
                        orderItem.weight = ps.weight
                    orderItem.product_standard_name = ps.name
                    orderItem.item_type = n['type']
                    orderItem.hascomment = ps.product.weights #存储权重，用于排序
                    itemList.append(orderItem)
                    order_weight += round((ps.weight / 500 * n['quantity']), 2)
                    if n['type'] == 5:
                        order_type = 1
                    is_store = orderItem.product.store
                    if is_store in storeList:
                        pass
                    else:
                        storeList.append(is_store)

                if len(itemList) == 0:
                    result['msg'] = u'订单中至少需要选择一件商品'
                else:
                    if balance > 0 and user.balance < balance:
                        result['msg'] = u'账户余额不足'
                    else:
                        with db.handle.transaction():
                            orderList = []
                            payment = 0
                            for o in storeList:
                                order = Order()
                                if prefer_delivery_day == '':
                                    order.distributiontime = '工作日/周末/假日均可'
                                elif prefer_delivery_day == 'weekend':
                                    order.distributiontime = '仅周末送货'
                                elif prefer_delivery_day == 'weekday':
                                    order.distributiontime = '仅工作日送货'
                                elif prefer_delivery_day == 'morning':
                                    order.distributiontime = '早上8点到11点'
                                elif prefer_delivery_day == 'noon':
                                    order.distributiontime = '早上11点到下午4点'
                                elif prefer_delivery_day == 'afternoon':
                                    order.distributiontime = '下午4点到7点'
                                order.user = user
                                if gateway == 'COD':
                                    payment = 0
                                    order.payment = 0
                                elif gateway == 'Alipay':
                                    payment = 1
                                    order.payment =1
                                elif gateway == 'Balance':
                                    payment = 2
                                    order.payment =2
                                else:
                                    payment = 3
                                    order.payment = 3
                                order.message = message
                                order.address = address
                                order.take_name = address.name
                                order.take_tel = address.mobile + ' ' + address.tel
                                order.take_address = address.province + ' ' + address.city + ' ' + address.region + ' ' + address.address
                                order.ip = self.request.remote_ip
                                order.status = 0
                                order.order_from = 1  # 网站下单

                                order.ordered = int(time.time())
                                order.ordereddate = time.strftime('%Y-%m-%d', time.localtime(order.ordered))
                                order.orderedtime = time.strftime('%H:%M:%S', time.localtime(order.ordered))
                                try:
                                    order.isinvoice = isinvoice
                                    order.invoicesub = invoice_type
                                    order.invoicename = invoicename
                                    order.invoicecontent = '0' #发票类型 0蔬菜 1食水果   暂时没用
                                except :
                                    pass
                                store_price = 0
                                store_weight = 0
                                order_count = len(itemList)
                                for orderItem in itemList:
                                    if orderItem.product.store == o:
                                        store_price += orderItem.price * orderItem.quantity
                                        store_weight += orderItem.weight * orderItem.quantity
                                if order_count > 1:
                                    order.price = store_price
                                    order.currentprice = store_price
                                    order.weight = store_weight
                                    order.pay_balance = balance / order_count
                                else:
                                    order.price = price
                                    order.currentprice = currentprice
                                    order.weight = order_weight
                                    order.pay_balance = balance
                                order.shippingprice = shippingprice
                                order.order_type = order_type
                                order.store = o
                                order.save()

                                order.ordernum = 'U' + str(order.user.id) + '-S' + str(order.id)
                                itemList=sorted(itemList, key=lambda orderItem: orderItem.hascomment, reverse=True)
                                for orderItem in itemList:
                                    if orderItem.product.store == o:
                                        orderItem.hascomment = 0 #存储权重，完成，初始化回去
                                        orderItem.order = order.id
                                        orderItem.save()
                                        delCar = Cart.delete().where(
                                            (Cart.user == user) & (Cart.product_standard == orderItem.product_standard))
                                        delCar.execute()  # 清空该item的购物车

                                if (order_weight > int(order_weight)):
                                    order.freight = 5 + int(
                                        order_weight - 1.0) * 0.5  # 5是首重运费，order_weight单位是斤，超过一公斤每斤加五毛，不足一斤算一斤
                                else:
                                    order.freight = 5 + (order_weight - 2) * 0.5
                                # 修改优惠券状态
                                if coupon:
                                    coupon.status = 2
                                    coupon.save()
                                    # 更新订单中的优惠券信息
                                    order.coupon = coupon.id
                                order.save()
                                orderList.append(order)

                            if balance > 0:
                                b = Balance()
                                b.user = user
                                b.balance = balance
                                b.stype = 1
                                b.log = u'余额支付' # '，订单编号：' + order.ordernum
                                b.created = int(time.time())
                                b.save()
                                usernew = User.get(id=user.id)
                                self.session['user'] = usernew
                                self.session.save()

                            if str(payment) == '0':  # 货到付款
                                oIds = ''
                                for oItem in orderList:
                                    oItem.status = 1
                                    oItem.save()
                                    oIds += str(oItem.id) + ','
                                # order.status = 1
                                result['flag'] = 1
                                result['orderid'] = oIds[:-1]
                                # order.save()
                            elif str(payment) == '1':  # 支付宝
                                oNum = ''
                                for oItem in orderList:
                                    oNum += oItem.ordernum + ','
                                result['url'] = u"/alipay/topay?tn=%s&body=%s&price=%f" % (oNum[:-1], u'车装甲商品', round(currentprice - balance, 2))
                                result['flag'] = 2
                                result['tn'] = oNum[:-1]
                                result['price'] = round(currentprice - balance, 2)

                            elif str(payment) == '2':  # 账户余额
                                oIds = ''
                                for oItem in orderList:
                                    oItem.status = 1
                                    oItem.save()
                                    oIds += str(oItem.id) + ','

                                # todo 支付成功后生成服务码

                                for n in itemList:
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
                                result['orderid'] = oIds[:-1]
                                result['flag'] = 1
                            elif str(payment) == '3':  # 网银支付
                                oNum = ''
                                for oItem in orderList:
                                    oNum += oItem.ordernum + ','
                                result['url'] = u"/alipay/topay?tn=%s&body=%s&price=%f&is_bank=%s" % (oNum[:-1], u'车装甲商品', round(currentprice - balance, 2), gateway)
                                result['flag'] = 2
                                result['tn'] = oNum[:-1]
                                result['price'] = round(currentprice - balance, 2)
                                result['is_bank'] = gateway

                        for orderItem in itemList:
                            p = orderItem.product
                            p.orders += 1

                            if orderItem.item_type == 0 and p.xgperusernum>0:  # 普通限购商品，修改限购库存总数
                                p.xgtotalnum-=orderItem.quantity
                                if p.xgtotalnum<0:
                                    p.xgtotalnum=0

                                if p.xgtotalnum<=5:#限购库存不足5份，给仓库C，运营Y，采购B，采购G发邮件报警
                                    try:
                                        admins = AdminUser.select()
                                        receivers = [n.email for n in admins if (len(n.email) > 0 and (n.roles.count('C')>0 or n.roles.count('Y')>0 or n.roles.count('B')>0 or n.roles.count('G')>0))]
                                        email = {u'receiver': receivers, u'subject': p.name+'限购库存不足提醒', u'body': p.name+'['+p.sku+'] 限购库存不足,当前剩余：'+str(p.xgtotalnum)+'份'}
                                        create_msg(simplejson.dumps(email), 'email')
                                    except:
                                        pass

                            p.save()

                            if orderItem.item_type == 1:  # 秒杀商品，修改秒杀活动数量
                                flymscount = self.application.session_store.get_session('psid_'+str(orderItem.product_standard.id), '')
                                flymscount = flymscount if flymscount else 0
                                flymscount = int(flymscount) - orderItem.quantity
                                if flymscount < 0:
                                    flymscount = 0
                                self.application.session_store.set_session('psid_'+str(orderItem.product_standard.id), flymscount, None, expiry=5*24*60*60)

                            if (orderItem.item_type == 5) & ((str(order.payment) == '0') | (str(order.payment) == '2')):    # 预定商品，修改已预定份数
                                pr = Product_Reserve.get(Product_Reserve.product == orderItem.product)
                                old_quantity = pr.quantity
                                pr.quantity += orderItem.quantity
                                pr.save()
                                if (old_quantity < pr.quantity_stage1) & (pr.quantity >= pr.quantity_stage1):
                                    return_reserve_balance(orderItem.product.id)
                                elif (old_quantity < pr.quantity_stage2) & (pr.quantity >= pr.quantity_stage2):
                                    return_reserve_balance(orderItem.product.id)

        handler.write(simplejson.dumps(result))
        return result


@route(r'/waiting', name='waiting')  # 支付等待
class WaitingHandler(BaseHandler):
    def get(self):
        self.render("site/cart/waiting.html")
