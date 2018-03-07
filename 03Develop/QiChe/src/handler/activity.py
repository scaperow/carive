#!/usr/bin/env python
# coding=utf8

import os
import time
import simplejson
from handler import BaseHandler
from lib.route import route
from model import User, UserActivity, Coupon, CouponTotal, Order, AdminUser, ProductStandard, Product,User_Promote,\
    Balance,Product_Activity,CouponReal,Gift,Product_Reserve,OrderItem,Cart, Inventory_Store,UserAddr, Store
from lib.mqhelper import create_msg
from bootloader import db
import logging
import setting
import random
import uuid
import urllib2
from map import getDistanceAS

logger = logging.getLogger('activity')
logger.addHandler(logging.StreamHandler())

@route(r'/activity/new_year', name='activity_new_year')  # 新年活动
class ActivityNewYearHandler(BaseHandler):
    def get(self):
        iscatched = False
        if self.current_user:
            beginvalue = time.mktime(time.strptime('2015-01-12', "%Y-%m-%d"))
            endvalue = time.mktime(time.strptime('2015-01-31', "%Y-%m-%d"))

            q = Order.select(Order.currentprice).where((Order.user == self.current_user) &
                                  (Order.ordered >= beginvalue) & (Order.status < 5) &
                                 (Order.ordered < endvalue) & (Order.payment < 9) &
                                 (((Order.status > -1) & (Order.payment == 0)) |
                                  ((Order.status > 0) & (Order.payment > 0)))).dicts()

            price = sum([n['currentprice'] for n in q])
            cpcount = int(price/50.0)
            activities = UserActivity.select().where(UserActivity.user == self.current_user.id)
            if activities.count() > 0:
                iscatched = True
        else:
            price = 0.0
            cpcount = 0
        list = ProductStandard.select(ProductStandard).join(Product). \
            where((ProductStandard.id << [268,215,128,279,38,37,84,86]) & (Product.status == 1))
        self.render('activity/new_year.html', user=self.current_user, price=price,
                    cpcount=cpcount, iscatched=iscatched, list=list)

@route(r'/activity/new_year/catch', name='activity_new_year_catch')  # 老用户领取优惠券
class ActivityNewYearCatchHandler(BaseHandler):
    def get(self):
        userid = self.get_argument('userid', None)

        if userid:
            user = User.get(id=userid)
            if user:
                activities = UserActivity.select().where(UserActivity.user == user)
                if activities.count() == 0:
                    beginvalue = time.mktime(time.strptime('2015-01-12', "%Y-%m-%d"))
                    endvalue = time.mktime(time.strptime('2015-01-31', "%Y-%m-%d"))
                    q = Order.select(Order.currentprice).where((Order.user == self.current_user) &
                                  (Order.ordered >= beginvalue) & (Order.status < 5) &
                                 (Order.ordered < endvalue) & (Order.payment < 9) &
                                 (((Order.status > -1) & (Order.payment == 0)) |
                                  ((Order.status > 0) & (Order.payment > 0)))).dicts()

                    price = sum([n['currentprice'] for n in q])
                    cpcount = int(price/50.0)
                    if cpcount > 0:
                        cps = Coupon.select(Coupon).join(CouponTotal).where((CouponTotal.name == '满50减5元') & (Coupon.status == 0)).limit(cpcount)
                        if cps.count() < cpcount:
                            msg = '领取优惠券失败，管理员会立即处理，请谅解，给您带来的不便'
                            admins = AdminUser.select()
                            receivers = [n.email for n in admins if len(n.email) > 0]
                            email = {u'receiver': receivers, u'subject': u'5元优惠券库存不够了', u'body': u'用户:'+str(userid)+u'领取优惠券失败，库存不足。'}
                            try:
                                create_msg(simplejson.dumps(email), 'email')
                            except:
                                pass
                        else:
                            for cp in cps:
                                cp.user = user
                                cp.status = 1
                                cp.save()

                                cp.coupontotal.quantity += 1
                                cp.coupontotal.save()
                            UserActivity.create(user=user, catchtime=int(time.time()), status=1)
                            msg = '成功领取'+str(cpcount)+'张优惠券。您可以在 [个人中心]-[我的优惠券] 中查看详情，感谢您的关注'
                            try:

                                content = '作为车装甲最最重视的用户，非常感谢您对车装甲的支持。送您'+str(cpcount*5)+'元优惠券，请笑纳。'
                                sms = {'mobile': user.mobile, 'body': content, 'signtype': '1', 'isyzm': '1'}
                                create_msg(simplejson.dumps(sms), 'sms')
                            except:
                                pass
                    else:
                        msg = '您累计消费不足50元，无法领取优惠券，感谢您的关注'
                else:
                    msg = '您已经领取过优惠券，感谢您的关注'
            else:
                msg = '请先登录车装甲，之后才能领取，感谢您的关注'
        else:
            msg = '请先登录车装甲，之后才能领取，感谢您的关注'
        self.write(msg)

@route(r'/activity/first_order', name='activity_first_order')  # 新用户首单满20以上返50%优惠券
class ActivityNewYearHandler(BaseHandler):
    def get(self):
        self.render('activity/first_order/fl.html')

def new_year_send_logic(order):
    user = order.user
    beginvalue = time.mktime(time.strptime('2015-01-31', "%Y-%m-%d"))
    endvalue = time.mktime(time.strptime('2015-02-15', "%Y-%m-%d"))
    now = int(time.time())
    # logger.error(str(now))
    needsend = True
    if now < endvalue and order.status < 5 and order.payment < 9 and \
            ((order.status > -1 and order.payment == 0) or (order.status > 0 and order.payment > 0)):
             #当前为2月15日之前,并且订单状态有效
        if user.signuped > beginvalue: #新注册用户,1月31日当天或以后注册的
            q = Order.select().where((Order.user == user) & (Order.id != order.id) &
                                     (Order.status < 5) & (Order.payment < 9) &
                                     (((Order.status > -1) & (Order.payment == 0)) |
                                      ((Order.status > 0) & (Order.payment > 0))))
            ct = q.count()
            if ct == 0: #新用户第一次购买
                needsend = False
                tencount = int(order.currentprice/40.0)
                fivecount = tencount * 2
                if fivecount > 0:
                    cps = Coupon.select(Coupon).join(CouponTotal).where((CouponTotal.name == '满50减5元') & (Coupon.status == 0) & (Coupon.user >> None)).limit(fivecount)
                    if cps.count() < fivecount:
                        admins = AdminUser.select()
                        receivers = [n.email for n in admins if len(n.email) > 0]
                        email = {u'receiver': receivers, u'subject': u'5元优惠劵库存不够了', u'body': u'用户:'+str(user.id)+u'领取优惠劵失败，库存不足。'}
                        try:
                            create_msg(simplejson.dumps(email), 'email')
                        except:
                            pass
                    else:
                        for cp in cps:
                            cp.user = user
                            cp.status = 1
                            cp.save()

                            cp.coupontotal.quantity += 1
                            cp.coupontotal.save()

                if tencount > 0:
                    cps = Coupon.select(Coupon).join(CouponTotal).where((CouponTotal.name == '满100减10元') & (Coupon.status == 0) & (Coupon.user >> None)).limit(tencount)
                    if cps.count() < tencount:
                        admins = AdminUser.select()
                        receivers = [n.email for n in admins if len(n.email) > 0]
                        email = {u'receiver': receivers, u'subject': u'10元优惠劵库存不够了', u'body': u'用户:'+str(user.id)+u'领取优惠劵失败，库存不足。'}
                        try:
                            create_msg(simplejson.dumps(email), 'email')
                        except:
                            pass
                    else:
                        for cp in cps:
                            cp.user = user
                            cp.status = 1
                            cp.save()

                            cp.coupontotal.quantity += 1
                            cp.coupontotal.save()
                if fivecount > 0:
                    try:
                        content = '小易终于等到您啦~请收下见面礼吧！'+str(tencount*10+fivecount*5)+'元代金券已经放入账户，下单时即可使用。更多优惠请到车装甲'
                        sms = {'mobile': user.mobile, 'body': content, 'signtype': '1', 'isyzm': '1'}
                        create_msg(simplejson.dumps(sms), 'sms')
                    except:
                        pass

        if needsend: #老用户下单(含新用户第二次下单)，满50送5，满80送5X2；1月31日以前注册的用户
            cpcount = 0
            if order.currentprice >= 80:
                cpcount = 2
            elif order.currentprice >= 50:
                cpcount = 1

            if cpcount > 0:
                cps = Coupon.select(Coupon).join(CouponTotal).where((CouponTotal.name == '满50减5元') & (Coupon.status == 0) & (Coupon.user >> None)).limit(cpcount)
                if cps.count() < cpcount:
                    admins = AdminUser.select()
                    receivers = [n.email for n in admins if len(n.email) > 0]
                    email = {u'receiver': receivers, u'subject': u'5元优惠劵赠送异常', u'body': u'用户:'+str(user.id)+u'领取优惠劵失败，库存不足。'}
                    try:
                        create_msg(simplejson.dumps(email), 'email')
                    except:
                        pass
                else:
                    for cp in cps:
                        cp.user = user
                        cp.status = 1
                        cp.save()

                        cp.coupontotal.quantity += 1
                        cp.coupontotal.save()
                    try:
                        content = '作为车装甲最最重视的用户，非常感谢您对车装甲的支持。送您'+str(cpcount*5)+'元优惠券，请笑纳。'
                        sms = {'mobile': user.mobile, 'body': content, 'signtype': '1', 'isyzm': '1'}
                        create_msg(simplejson.dumps(sms), 'sms')
                    except:
                        pass

#新用户注册首单返50%优惠券
def new_user_order_coupon(order):
    msg = ''
    oc = Order.select().where((Order.user == order.user) & (Order.status > 1) & (Order.status < 5) & (Order.ordered <= order.ordered))
    if oc.count() == 1:
        log = u'首单返50%优惠券活动，系统自动赠送'
        if (oc[0].currentprice >= 20) & (oc[0].currentprice < 80):
            cpcount = int(oc[0].currentprice/10.0)
            cps = CouponTotal.select().where((CouponTotal.name == '满50减5元') & (CouponTotal.status == 0)).limit(1)
            if cps.count() < 1:
                msg = u'用户'+ order.user.username + u'首单返券失败，请检查“满50减5元”优惠券是否存在或已被禁用'
            else:
                count = 0
                while count < cpcount:
                    create_coupon(order.user, cps[0].id, log)
                    count += 1
                msg += u'首单返卷成功，用户获得'+ str(cpcount) + u'张5元优惠券'
        if(oc[0].currentprice >= 80):
            cpcount5 = int(oc[0].currentprice / 10.0 / 2)
            cpcount10 = int(oc[0].currentprice / 10.0 / 4)
            cps5 = CouponTotal.select().where((CouponTotal.name == '满50减5元') & (CouponTotal.status == 0)).limit(1)
            cps10 = CouponTotal.select().where((CouponTotal.name == '满100减10元') & (CouponTotal.status == 0)).limit(1)
            if cps5.count() < 1:
                msg = u'用户'+ order.user.username + u'首单返卷失败，请检查“满50减5元”优惠券是否存在或已被禁用'
            else:
                count = 0
                while count < cpcount5:
                    create_coupon(order.user, cps5[0].id, log)
                    count += 1
                msg += u'首单返卷成功，用户获得 '+ str(cpcount5) + u' 张5元优惠券'
            if cps10.count() < 1:
                msg = u'用户'+ order.user.username + u'首单返卷失败，请检查“满100减10元”优惠券是否存在或已被禁用'
            else:
                count = 0
                while count < cpcount10:
                    create_coupon(order.user, cps10[0].id, log)
                    count += 1
                msg += u'和 '+ str(cpcount10) + u' 张10元优惠券'
    return msg

#老推新用户首单返余额
def old_new_user_balance(order):
    try:
        rate = float(setting.Old_New_User_Rate)         #首单返利利率
        max_price = float(setting.Old_New_Max_Price)    #首单返利最大金额
        oc = Order.select().where((Order.user == order.user) & (Order.status == 4) & (Order.ordered <= order.ordered))
        if oc.count() == 1:
            fl_price = oc[0].currentprice - oc[0].shippingprice   #商品金额 = 订单实际支付金额 - 订单运费
            if (fl_price >= 0):
                return_balance = round((fl_price * rate), 2)
                if return_balance > max_price:
                    return_balance = max_price
                up = User_Promote.get(User_Promote.new_user == order.user)
                if up:
                    balance = Balance()
                    balance.user = up.old_user
                    balance.balance = return_balance
                    balance.created = int(time.time())
                    balance.stype = 0
                    balance.log = u'老推新首单返利。'
                    balance.save()
                    msg = u'恭喜您，您推荐的好友'+order.user.username+u'首次订单已经完成，您获得'+str(return_balance)+\
                          u'元余额返利，请登录车装甲查收。'
                    sms = {'mobile': up.old_user.username, 'body': msg, 'signtype': '1', 'isyzm': '1'}
                    create_msg(simplejson.dumps(sms), 'sms')

                    up.first_order_gift = 1
                    up.first_order_time = int(time.time())
                    up.first_order_content =  msg
                    up.save()
    except:
        pass

#用户充值返余额
def user_top_up_balance(balance):
    max_price = int(setting.Balance_Max_Price)  #最大返利金额
    end_date = time.mktime(time.strptime(setting.Balance_End_Date, "%Y-%m-%d")) #活动结束时间
    date = int(time.time())
    if date < end_date:
        try:
            b = Balance.select(db.fn.SUM(Balance.balance).alias('total_price')).where((Balance.user == balance.user) &
                                (Balance.stype == 0) & (Balance.log == '充值返现活动赠送')).dicts()
            need_price = 0
            if b[0]["total_price"]:
                if b[0]["total_price"] < max_price:
                    need_price = max_price - b[0]["total_price"]
                    if (balance.balance / 2 < need_price):
                        need_price = balance.balance / 2
                else:
                    return
            else:
                need_price = balance.balance / 2
                if need_price > max_price:
                    need_price = max_price
            b_new = Balance()
            b_new.user = balance.user
            b_new.balance = need_price
            b_new.created = int(time.time())
            b_new.stype = 0
            b_new.log = u'充值返现活动赠送'
            b_new.save()
            msg = u'恭喜您，充值成功！并获得充值返现金额 '+str(need_price)+u' 元，请登录车装甲查收。'
            sms = {'mobile': balance.user.username, 'body': msg, 'signtype': '1', 'isyzm': '1'}
            create_msg(simplejson.dumps(sms), 'sms')
        except Exception, ex:
            logging.error(ex)
            pass

#老推新注册送优惠券
def old_new_user_coupon(promote,user):
    if promote:
        result = 0
        msg = ''
        try:
            oldUser = User.get(User.username == promote)
            cps = CouponTotal.select().where((CouponTotal.name == '满30减3元') & (CouponTotal.status == 0)).limit(1)
            if cps.count() < 1:
                msg = u'请检查“满30减3元优惠券”是否被禁用或者不存在，老用户'+oldUser.username +u"未获得返卷，请手动补充优惠券后手动补发。"
                admins = AdminUser.select()
                receivers = [n.email for n in admins if len(n.email)>0]
                email = {u'receiver': receivers, u'subject':u'老推新用户注册返卷失败',u'body': msg}
                create_msg(simplejson.dumps(email), 'email')
            else:
                log = u'系统自动赠送'
                create_coupon(oldUser, cps[0].id, log)
                msg = u'恭喜您，您推荐的好友'+ user.mobile+u'已经注册成功，您获得3元优惠券一张，请在有效期内使用。'
                sms = {'mobile': oldUser.username, 'body': msg, 'signtype': '1', 'isyzm': '1'}
                create_msg(simplejson.dumps(sms), 'sms')
                result = 1
            up = User_Promote()
            up.old_user = oldUser.id
            up.new_user = user.id
            up.signuped = int(time.time())
            if result == 1:
                up.signup_gift = 1
                up.signup_gift_content = msg
            up.save()
        except Exception, e:
            logging.error("推荐人不存在" + e)

#老推新注册送抽奖机会
def old_new_user_raffle(promote,user):
    if promote:
        result = 0
        msg = ''
        try:
            oldUser = User.get(User.username == promote)
            oldUser.raffle_count += 1
            oldUser.save()
            up = User_Promote()
            up.old_user = oldUser.id
            up.new_user = user.id
            up.signuped = int(time.time())
            up.signup_gift = 1
            up.signup_gift_content = msg
            up.save()
        except Exception, e:
            logging.error("老推新注册送抽奖机会,推荐人不存在" + e)

# 检查商品是否为活动商品
def check_activity(pid):
    datetime = int(time.time())
    pa = Product_Activity.select().where((Product_Activity.status == 1) & (Product_Activity.quantity > 0) & (Product_Activity.type == 1) &
                (Product_Activity.begin_time < datetime) & (Product_Activity.end_time > datetime) & (Product_Activity.product == pid)).\
                order_by(Product_Activity.end_time.desc())
    p = {'flag': 0, 'price': 0, 'begin_time': 0, 'end_time': 0, 'quantity': 0, 'pid': 0, 'status': 1, 'psid': '', 'id': ''}
    if pa.count() > 0:
        if (datetime >= pa[0].begin_time) and (pa[0].quantity > 0) and (datetime < pa[0].end_time):
            p["flag"] = 1
        elif datetime > pa[0].begin_time or pa[0].quantity <= 0:
            p["flag"] = 2
        elif datetime < pa[0].begin_time:
            p["flag"] = 0
        p["price"] = pa[0].price
        p["begin_time"] = pa[0].begin_time
        p["end_time"] = pa[0].end_time
        p["quantity"] = pa[0].quantity
        p["status"] = pa[0].status
        p["pid"] = pa[0].product.id
        p["psid"] = pa[0].product_standard.id
        p["id"] = pa[0].id
    if p["flag"] == 1:
        return p
    else:
        return None

# 新用户注册即送10元账户余额    5月5日修改为送5元
def new_user_balance(user):
    pass
    try:
        b_new = Balance()
        b_new.user = user.id
        b_new.balance = 5
        b_new.created = int(time.time())
        b_new.stype = 0
        b_new.log = u'新用户注册即送5元账户余额'
        b_new.save()
        msg = u'恭喜您，注册成功！并获得系统赠送5元现金余额，请登录车装甲个人中心查收。'
        sms = {'mobile': user.username, 'body': msg, 'signtype': '1', 'isyzm': '1'}
        create_msg(simplejson.dumps(sms), 'sms')
    except Exception, ex:
        msg = u'新用户注册送5元账户余额失败，用户名' + user.username + u' 错误信息：' + ex.message
        email = {u'receiver': ['kouzhikai@kingrocket.com','liuxiaoming@kingrocket.com'], u'subject':u'新用户注册即送5元账户余额失败',u'body': msg}
        create_msg(simplejson.dumps(email), 'email')

# 创建优惠券 1 参数 user对象， 2 coupontotal.id， 3 获取方式及其他信息
def create_coupon(user, total_id, log):
    try:
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
        sa = []
        for i in range(16):
            sa.append(random.choice(seed))
            salt = ''.join(sa)
        code = uuid.uuid3(uuid.NAMESPACE_DNS, salt + str(int(time.time())))
        cp = Coupon()
        cp.user = user.id
        cp.code = code
        cp.coupontotal = total_id
        cp.status = 1
        cp.starttime = int(time.time())
        cp.endtime = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 0:0:0", time.localtime(time.time()+ 86400 * 30)), "%Y-%m-%d 0:0:0")))
        cp.log = log
        cp.save()
        cp.coupontotal.quantity += 1
        cp.coupontotal.save()
        msg = u'为用户'+ user.username + u'增加优惠券成功！'
        return msg
    except Exception, ex:
        msg = u'创建优惠券失败，错误信息：' + ex.message
        email = {u'receiver': ['kouzhikai@kingrocket.com','liuxiaoming@kingrocket.com'], u'subject':u'创建优惠券失败',u'body': msg}
        create_msg(simplejson.dumps(email), 'email')
        return msg

# 创建实物优惠券 1 参数 user对象， 2 couponrealtotal.id， 3 操作人
def create_coupon_real(user, total_id, createby, type):
    try:
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
        sa = []
        for i in range(16):
            sa.append(random.choice(seed))
            salt = ''.join(sa)
        code = uuid.uuid3(uuid.NAMESPACE_DNS, salt + str(int(time.time())))
        cp = CouponReal()
        cp.user = user.id
        cp.code = code
        cp.coupon_real_total = total_id
        cp.status = 1
        cp.starttime = int(time.time())
        cp.endtime = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 0:0:0", time.localtime(time.time()+ 86400 * 30)), "%Y-%m-%d 0:0:0")))
        cp.createby = createby
        cp.createtime = int(time.time())
        cp.save()
        cp.coupon_real_total.quantity += 1
        cp.coupon_real_total.save()

        gift = Gift()
        gift.user = user.id
        gift.product = cp.coupon_real_total.product
        gift.product_standard = cp.coupon_real_total.product_standard
        gift.quantity = 1
        gift.created = int(time.time())
        gift.created_by = AdminUser.get(AdminUser.username == createby).id
        gift.status = 0
        gift.type = type   # 对应orderItem表中的item_type
        gift.end_time = cp.endtime
        gift.save()
        cp.status = 1
        cp.save()
        cp.coupon_real_total.used += 1
        cp.coupon_real_total.save()

        msg = u'为用户'+ user.username + u'增加实物优惠券成功！'
        return msg
    except Exception, ex:
        msg = u'创建实物优惠券失败，错误信息：' + ex.message
        email = {u'receiver': ['kouzhikai@kingrocket.com','liuxiaoming@kingrocket.com'], u'subject':u'创建实物优惠券失败',u'body': msg}
        create_msg(simplejson.dumps(email), 'email')
        return msg

# 到达阶梯后返还预订商品差额
def return_reserve_balance(pid):
    try:
        pass
        # item = OrderItem.select().where((OrderItem.product == pid) & (OrderItem.item_type == 5))
        # pr = Product_Reserve.select().where(Product_Reserve.product == pid)
        # for i in item:
        #     if (i.order.payment >= 1) & (i.order.payment <= 3) & (i.order.status >= 1) & (i.order.status <= 2):     #支付方式不是货到付款，并且状态为待处理,和正在处理
        #         b = Balance()
        #         b.user = i.order.user.id
        #         b.created = int(time.time())
        #         b.stype = 0
        #         balance = 0
        #         quantity = 0
        #         if (pr[0].quantity >= pr[0].quantity_stage1) & (pr[0].quantity < pr[0].quantity_stage2):
        #             balance = i.price - pr[0].price_stage1
        #             quantity = pr[0].quantity_stage1
        #         elif pr[0].quantity >= pr[0].quantity_stage2:
        #             balance = i.price - pr[0].price_stage2
        #             quantity = pr[0].quantity_stage2
        #         if balance > 0:
        #             b.balance = balance * i.quantity
        #             b.log = u'预售商品'+pr[0].product.name+u'总数到达' + str(quantity) + u'份系统返还差额'
        #             b.save()
        #             i.price -= balance
        #             i.save()
        #         balance = balance * i.quantity
        #         i.order.price -= balance
        #         i.order.currentprice -= balance
        #         i.order.status = 2      # 返还差额后将订单状态改为正在处理，不允许用户自行取消
        #         i.order.save()
    except:
        pass

# 检查用户当天可购买数量是否超出
def check_buy_quantity(pid, uid, c, is_cart):
    result = {'flag': 0, 'quantity': 0}
    try:
        begin = time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime(time.time())), "%Y-%m-%d"))
        end = time.mktime(time.strptime(time.strftime("%Y-%m-%d 23:59:59", time.localtime(time.time())), "%Y-%m-%d %H:%M:%S"))
        item = OrderItem.select(OrderItem, Order).join(Order).where((Order.ordered > begin) & (Order.ordered < end) &
                                     (Order.status > 0) & (Order.status < 5) &
                                     (Order.user == uid) & (OrderItem.product == pid) & (OrderItem.item_type == 0))
        cart = Cart.select().where((Cart.product == pid) & (Cart.user == uid) & (Cart.type == 0))
        cart_c = 0
        for n in cart:
            cart_c += n.quantity
        p = Product.get(id = pid)
        quantity = 0
        for n in item:
            quantity += n.quantity
        if is_cart == 1:    # 如果等于1 表示是购物车中操作
            count = quantity + c
        else:
            count = quantity + c + cart_c
        if count > p.xgperusernum:
            result['flag'] = 1
            result['quantity'] = p.xgperusernum - quantity
        if p.xgperusernum == 0:
            result['flag'] = 0
        return result
    except Exception, ex:
        return result

# 检查店铺中此商品是否有库存
def check_store_product_quantity(store_id, psid):
    result = 0
    if store_id:
        ins = Inventory_Store.select().where((Inventory_Store.store == store_id) & (Inventory_Store.product_standard == psid))
        if ins.count() > 0:
            if ins[0].quantity > 0:
                result = 1
    return result

# 检查用户默认地址和所选店铺之间的距离
def check_user_store_distance(_self):
    result = 0
    user = _self.get_current_user()
    client_store = _self.get_secure_cookie('store', None)
    if client_store and user:
        ua = UserAddr.select().where((UserAddr.user == user.id) & (UserAddr.isdefault == 1))
        if ua.count() > 0:
            address = ua[0].province + ua[0].city + ua[0].address
            s = getDistanceAS(address.replace(' ', ''), client_store)
            if s['flag'] == 1:
                if float(s['data']) < setting.PeiSongDistance:
                    result = 1
    return result

# 检查订单中的所有商品离最近可配送店铺是否有货
def check_order_store_quantity(store_id, oid):
    result = 0
    items = OrderItem.select().where(OrderItem.order == oid)
    r = 0
    if store_id:
        for i in items:
            if i.product.is_store == 1:     # and i.product.store.id == int(store_id)
                r += 1
            else:
                r += check_store_product_quantity(store_id, i.product_standard.id)
        if r == items.count():
            result = 1
    else:
        list = []
        order = Order.get(Order.id == oid)
        store = Store.select().where(Store.status == 1)
        sid = 0
        for s in store:
            ss = getDistanceAS(order.take_address.replace(' ', ''), s.id)
            if ss['flag'] == 1:
                list.append(float(ss['data']))
                if float(ss['data']) < setting.PeiSongDistance:
                    sid = s.id
        for i in items:
            if i.product.is_store == 1 and i.product.store.id == sid:
                r += 1
            else:
                r += check_store_product_quantity(sid, i.product_standard.id)
        if r == items.count():
            result = 1
    return result