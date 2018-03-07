#!/usr/bin/env python
#coding=utf8

import logging
from tornado.web import HTTPError
from handler import BaseHandler,UserBaseHandler
from lib.route import route
from model import Oauth, User, UserVcode, Page,  Ad,Product, Order,Fav,Coupon,UserAddr,Consult,Balance,CouponTotal,\
    Score,Comment,OrderItem,User_Promote,UserCheckIn,UserLevel,ProductStandard,Product_Activity, Gift, UserAuto, Brand, \
    CategoryFront, Attribute,Store,StorePrice, UserMessage,ProductPic, Area, StoreNewsCategory, StoreNews, StorePic, \
    Delivery, FavStore, Feedback, Question, Answer, CircleTopic, CircleTopicPic, CircleTopicReply, CircleTopicPraise, Settlement, \
    Withdraw, OrderItemService, StoreAuto
import simplejson
from bootloader import db
import time
import base64
import os
import qrcode
import random

@route(r'/user/order', name='user_order') #我的订单
class UserOrderHandler(UserBaseHandler):
    def get(self):
        status = int(self.get_argument("status", -1))
        page = int(self.get_argument("page", 1))
        pagesize = self.settings['user_pagesize']
        ft = (Order.user == self.current_user.id) & (Order.status > -1)
        if status == -1:
            pass
        elif status == 0:#待付款
            ft = ft & ((Order.status == 0) & (Order.payment>=1))
        elif status == 1:#已付款；待处理,含货到付款的，含已付款的，含正在处理的，已发货的
            ft = ft & ((Order.status == 3) | (Order.status == 2) | ((Order.payment==0) & (Order.status==0)) | (Order.status == 1) & (Order.payment>=1))
        else: #完成或已取消的
            ft = ft & (Order.status == status)

        q = Order.select().where(ft)
        total = q.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        list = q.order_by(Order.ordered.desc()).paginate(page, pagesize)
        orders = map(self.bind_status_text, list)
        self.render('/user/order.html',c='order', orders=orders, s=status, total=total, page=page,
                    pagesize=pagesize, totalpage=totalpage,)

    def bind_status_text(self, order):
        if order.status < 0:
            order.ip = u'已删除'
        elif (order.status == 0 or order.status == 1 or order.status == 2 or order.status == 3) and order.payment == 0:
            order.ip = u'正在处理'
        elif (order.payment == 3 or order.payment == 2 or order.payment == 1) and order.status == 0:
            order.ip = u'等待付款'
        elif (order.payment == 3 or order.payment == 2 or order.payment == 1) and order.status == 1:
            order.ip = u'已付款'
        elif order.status == 2 or order.status == 3: #order.payment == 1 and (order.status == 1 or order.status == 2 or order.status == 3):
            order.ip = u'正在处理'
        elif order.status == 4:
            order.ip = u'已完成'
        elif order.status == 5:
            order.ip = u'已取消'
        else:
            order.ip = u'正在处理'
        return order

@route(r'/user/order/(\d+)', name='user_order_detail') #我的订单详情
class UserOrderDetailHandler(UserBaseHandler):
    def get(self, oid):
        try:
            o = Order.get((Order.id == oid) & (Order.user == self.current_user.id))
        except:
            o = None
        self.render('/user/order_detail.html',c='order',o=o)

@route(r'/user/order_store/(\d+)', name='user_order_store_detail') #店铺订单详情
class UserOrderStoreDetailHandler(UserBaseHandler):
    def get(self, oid):
        try:
            o = Order.get((Order.id == oid) & (Order.store == self.current_user.store))
        except:
            o = None
        self.render('/user/order_detail.html',c='order',o=o)

@route(r'/user/order/reserve/(\d+)', name='user_order_reserve') #服务预约
class UserOrderDetailHandler(UserBaseHandler):
    def get(self, id):
        try:
            order = OrderItemService.select().where((OrderItemService.order_item == id) & (OrderItemService.user == self.current_user.id))
            if order.count() > 0:
                o = order
            else:
                o = None
        except:
            o = None
        self.render('/user/order/order_reserve.html',c='order',o=o)
    def post(self, id):
        code = self.get_argument('code','')
        reserve_time = self.get_argument('reserve_time','')
        oi = OrderItemService.select().where((OrderItemService.order_item == id) & (OrderItemService.service_code == code))
        if oi.count() > 0:
            if oi[0].reserve_time:
                self.flash("<script>alert('已经预约，不能重复预约！');</script>")
                pass
            else:
                oi[0].reserve_time = time.mktime(time.strptime(reserve_time, "%Y-%m-%d"))
                oi[0].save()
                self.flash("<script>alert('提交成功！');</script>")
        self.redirect('/user/order/reserve/' + str(id))

@route(r'/user/order_midify/(\d+)', name='user_order_midify') #店铺订单修改
class UserOrderStoreDetailHandler(UserBaseHandler):
    def get(self, oid):
        try:
            o = Order.get((Order.id == oid) & (Order.store == self.current_user.store))
        except:
            o = None
        self.render('/user/order/order_modify.html',c='order',o=o)
    def post(self, oid):
        currentprice = self.get_argument('currentprice','0')
        message = self.get_argument('message','')
        o = Order.get(Order.id == oid)
        o.currentprice = currentprice
        o.message = message
        o.save()
        self.redirect('/user/order_store/' + str(oid))

@route(r'/user/fav', name='user_fav')  # 我收藏的产品
class UserFavHandler(UserBaseHandler):
    def get(self):
        products = Product.select().join(Fav).where(Fav.user==self.current_user.id)
        self.render('/user/account/fav.html', c='fav', products=products)

@route(r'/user/fav_store', name='user_fav_store')  # 我收藏的产品
class UserFavStoreHandler(UserBaseHandler):
    def get(self):
        items = Store.select().join(FavStore).where(FavStore.user==self.current_user.id)
        self.render('/user/account/fav_store.html', c='fav_store', items=items)

@route(r'/user/removefav/(\d+)', name='user_removefav') # 删除收藏
class RemoveFavHandler(UserBaseHandler):
    def get(self,pid):
        q = Fav.delete().where((Fav.product==pid) & (Fav.user == self.current_user.id))
        q.execute()
        self.redirect('/user/fav')

@route(r'/user/removefav_store/(\d+)', name='user_removefav_store') # 删除收藏的门店
class RemoveFavStoreHandler(UserBaseHandler):
    def get(self,  sid):
        q = FavStore.delete().where((FavStore.store == sid) & (Fav.user == self.current_user.id))
        q.execute()
        self.redirect('/user/fav_store')

@route(r'/user/coupon', name='user_coupon') #我的优惠劵
class UserCouponHandler(UserBaseHandler):
    def get(self):
        status = int(self.get_argument("status", 1))
        current_time =time.strptime(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),'%Y-%m-%d %H:%M:%S')
        ft = (Coupon.user ==self.current_user.id)
        if status == 3:
            ft = ft & (CouponTotal.status == 0) & (Coupon.status == 1)
            coupons = Coupon.select(Coupon,CouponTotal).join(CouponTotal,on=((Coupon.coupontotal==CouponTotal.id) & (time.mktime(current_time) > Coupon.endtime))).where(ft)
        elif status == 2:
            ft = ft & (CouponTotal.status == 0) & (Coupon.status == status)
            coupons = Coupon.select(Coupon,CouponTotal).join(CouponTotal,on=(Coupon.coupontotal==CouponTotal.id)).where(ft)
        else:
            ft = ft & (CouponTotal.status == 0) & (Coupon.status == status)
            coupons = Coupon.select(Coupon,CouponTotal).join(CouponTotal,on=((Coupon.coupontotal==CouponTotal.id) & (Coupon.endtime > time.mktime(current_time)))).where(ft)
        self.render('/user/coupon.html', c='coupon',coupons=coupons,s=status)



@route(r'/user/home', name='user_home') #会员首页
class UserHomeHandler(UserBaseHandler):
    def get(self):
        # result = self.get_argument('result','')
        user = User.get(id = self.current_user.id)
        #更新用户Session
        self.session['user'] = user
        self.session.save()

        seriesnum = user.hascheckedin()
        q = UserLevel.select().order_by(UserLevel.levelid)
        if(q.count()>0):
            for i in range(q.count()):
                if(q[i].levelid== user.userlevel.levelid):
                    userlevel=q[i]
                    if(i<q.count()-1):
                        userlevelnext=q[i+1]
                    else:
                        userlevelnext=None
        self.render('/user/home.html', seriesnum=seriesnum,userlevel=userlevel,userlevelnext=userlevelnext, c='home')


@route(r'/user/profile', name='user_profile')  # 我的账户信息
class UserProfileHandler(UserBaseHandler):
    def get(self):
        result = self.get_argument('result','')
        user = User.get(id = self.current_user.id)
        q=UserLevel.select().order_by(UserLevel.levelid)
        if(q.count()>0):
            for i in range(q.count()):
                if(q[i].levelid== user.userlevel.levelid):
                    userlevel=q[i]
                    if(i<q.count()-1):
                        userlevelnext=q[i+1]
                    else:
                        userlevelnext=None

        self.render('/user/account/profile.html', result=result,userlevel=userlevel,userlevelnext=userlevelnext, u=user, c='profile')

    def post(self):
        result = 0
        username = self.get_argument('username','')
        nickname = self.get_argument('nickname','')
        qq = self.get_argument('qq','')
        email = self.get_argument('email','')
        gender = int(self.get_argument('gender','2'))
        birthday = self.get_argument('birthday','')
        tel = self.get_argument('tel','')

        try:
            userinfo = User.get(id = self.current_user.id)
            userinfo.username = username
            userinfo.nickname = nickname
            userinfo.qq = qq
            userinfo.email = email
            userinfo.gender = gender
            userinfo.birthday = birthday
            userinfo.tel = tel
            userinfo.save()
            self.session['user'] = userinfo
            self.session.save()
            result = 1
        except Exception, ex:
            logging.error(ex)
            result = 0
        self.redirect('/user/profile')
        # self.render('/user/profile.html', result=result, c='profile')

@route(r'/user/feedback', name='user_feedback')  # 意见反馈
class UserFeedbackHandler(UserBaseHandler):
    def get(self):
        result = int(self.get_argument('result', 0))
        self.render('/user/account/feedback.html', result=result, c='feedback')

    def post(self):
        result = 0
        u = self.current_user
        content = self.get_argument('content','')
        type = ''
        contact = ''
        mobile = u.mobile
        created = int(time.time())
        reply_content = ''
        reply_time = 0
        try:
            fb = Feedback()
            fb.user = u.id
            fb.type = type
            fb.content = content
            fb.contact = contact
            fb.mobile = mobile
            fb.created = created
            fb.reply_content = reply_content
            fb.reply_time = reply_time
            fb.save()
            result = 1
        except Exception, ex:
            logging.error(ex)
            result = 0
        self.redirect('/user/feedback?result='+str(result))
        # self.render('/user/profile.html', result=result, c='profile')

@route(r'/user/apply_store', name='user_apply_store') # 申请成为服务门店
class UserApplyStoreHandler(UserBaseHandler):
    def get(self):
        result =int( self.get_argument('result',0))
        user = User.get(id = self.current_user.id)
        store = user.store
        areas = Area.select().where((Area.is_delete == 0) & (Area.pid == 0)).order_by(Area.spell_abb, Area.sort)
        default_province=''
        default_city=''
        default_district=''
        if store:
            default_province = store.area_code[0:4]
            default_city = store.area_code[0:8]
            default_district = store.area_code

        self.render('/user/apply_store.html', result=result, user=user, s=store, areas=areas,default_province=default_province,default_city=default_city,default_district=default_district)

    def post(self):
        result = 0
        name = self.get_argument('name','')
        area_code = self.get_argument('district_code','')
        address = self.get_argument('address','')
        link_man = self.get_argument('link_man','')
        tel = self.get_argument('tel','')
        image = self.get_argument('image','')
        image_legal = self.get_argument('legal','')
        image_license = self.get_argument('license','')

        try:
            user = User.get(id = self.current_user.id)
            store = user.store
            if not store:
                store = Store()
            store.name = name
            store.area_code = area_code
            store.address = address
            store.link_man = link_man
            store.tel = tel
            store.image = image
            store.image_legal = image_legal
            store.image_license = image_license
            store.mobile = user.mobile
            store.check_state = 0
            store.save()
            user.store = store
            user.save()
            pics = StorePic.select().where((StorePic.store == store)&(StorePic.is_cover == 1)&(StorePic.is_active == 1))
            if image :
                if pics.count()>0:
                    pics[0].path = image
                    pics[0].save()
                else:
                    pic = StorePic.create(store=store, path=image, check_state=0, is_cover=1, is_active=1)
            result = 1
        except Exception, ex:
            logging.error(ex)
            result = 0
        self.redirect('/user/apply_store?result=' + str(result))

@route(r'/user/profile_store', name='user_profile_store') # 门店资料修改
class UserProfileStoreHandler(UserBaseHandler):
    def get(self):
        result =int( self.get_argument('result',0))
        user = User.get(id = self.current_user.id)
        store = user.store
        areas = Area.select().where((Area.is_delete == 0) & (Area.pid == 0)).order_by(Area.code)
        default_province=''
        default_city=''
        default_district=''
        if not result and store.check_state == 0:
            result = 2
        if store:
            default_province = store.area_code[0:4]
            default_city = store.area_code[0:8]
            default_district = store.area_code

        self.render('/user/account/profile_store.html', result=result, user=user, s=store, areas=areas,default_province=default_province,default_city=default_city,default_district=default_district)

    def post(self):
        result = 0
        name = self.get_argument('name','')
        area_code = self.get_argument('district_code','')
        address = self.get_argument('address','')
        # link_man = self.get_argument('link_man','')
        tel = self.get_argument('tel','')
        image = self.get_argument('image','')
        # image_legal = self.get_argument('legal','')
        # image_license = self.get_argument('license','')
        intro = self.get_argument('intro','')
        x = self.get_argument('x','')
        y = self.get_argument('y','')

        try:
            user = User.get(id = self.current_user.id)
            store = user.store
            result = 1
            if store.name != name:
                store.check_state = 0
                result = 2
            store.name = name
            store.area_code = area_code
            store.address = address
            store.intro = intro
            store.tel = tel
            store.image = image
            # store.image_legal = image_legal
            # store.image_license = image_license
            store.mobile = user.mobile
            store.x = x
            store.y = y
            store.save()
            # user.store = store
            # user.save()
        except Exception, ex:
            logging.error(ex)
            result = 0
        self.redirect('/user/profile_store?result=' + str(result))

@route(r'/user/address', name='user_address') # 我的地址
class UserAddressHandler(UserBaseHandler):
    def get(self):
        user = self.current_user
        ft = (UserAddr.user == user.id) & (UserAddr.isactive == 1)
        addritems = UserAddr.select().where(ft).order_by(UserAddr.id.desc())    #UserAddr.isdefault.desc(),
        self.render('/user/address.html', addritems=addritems, c='address')
    def post(self):
        user = self.current_user
        recipient_name = self.get_argument('recipient_name','')
        region = self.get_argument('ddlCounty','')
        street = self.get_argument('ddlStreet','')
        address = self.get_argument('recipient_street','')
        recipient_hp = self.get_argument('recipient_hp','')
        tel_area = self.get_argument('recipient_tel_area','')
        tel_number = self.get_argument('recipient_tel_number','')
        tel_ext = self.get_argument('recipient_tel_ext','')
        address_id = self.get_argument('hidAddressID','')
        userAddr = UserAddr()
        user = self.current_user
        userAddr.user = user.id
        userAddr.address = address
        userAddr.mobile = recipient_hp
        userAddr.province = '陕西'
        userAddr.city = '西安'
        userAddr.region = region
        userAddr.name = recipient_name
        userAddr.street = street

        if(tel_area != '' and tel_number != ''):
            if( tel_ext != ''):
                userAddr.tel = tel_area + '-' + tel_number + '-' + tel_ext
            else:
                userAddr.tel = tel_area + '-' + tel_number
        userAddr.isdefault = 1
        if(address_id != ''):
            userAddr.id = address_id

        listUserAddrs = UserAddr.select().where((UserAddr.user == user.id) & (UserAddr.isdefault == 1))
        for listUserAddr in listUserAddrs:
            listUserAddr.isdefault = 0
            listUserAddr.save()

        userAddr.save()

        ft = (UserAddr.user == user.id) & (UserAddr.isactive == 1)
        addritems = UserAddr.select().where(ft).order_by(UserAddr.isdefault.desc(),UserAddr.id.desc())
        self.render('/user/address.html', addritems=addritems)

@route(r'/user/autos', name='user_autos') # 我的汽车
class UserAutosHandler(UserBaseHandler):
    def get(self):
        id= int(self.get_argument("id", 0))
        user = self.current_user
        ft = (UserAuto.user == user.id)
        # items = UserAuto.select(UserAuto, 't2.name as brand_name').join(Brand,on=(UserAuto.brand_id == Brand.id)).\
        #     join(Brand,on=(UserAuto.xing_id == Brand.id)).join(Brand,on=(UserAuto.year_id == Brand.id)).where(ft).order_by(UserAuto.id.desc())
        sql = '''
       select a.*,b.name as brand_name,c.name as xing_name,d.name as year_name from tb_user_auto a
inner JOIN tb_brand b on left(a.brand_code,4)=b.code
inner JOIN tb_brand c on left(a.brand_code,8)=c.code
inner JOIN tb_brand d on a.brand_code=d.code where a.user_id=%s
        '''
        q = db.handle.execute_sql(sql % ( user.id))
        items = q.fetchall()
        brands = Brand.select().where((Brand.is_delete == 0) & (Brand.pid == 0)).order_by(Brand.spell_abb, Brand.sort)
        userAuto = None
        default_brand=''
        default_xing=''
        default_year=''
        if id>0:
            userAuto=UserAuto.get(UserAuto.id == id)
            default_brand=userAuto.brand_code[0:4]
            default_xing=userAuto.brand_code[0:8]
            default_year=userAuto.brand_code
        self.render('/user/account/autos.html', items=items, c='autos', brands=brands, userAuto=userAuto,default_brand=default_brand,default_xing=default_xing,default_year=default_year)
    def post(self):
        id= int(self.get_argument("id", 0))
        user = self.current_user
        brand_id = self.get_argument('brand_id','0')
        xing_id = self.get_argument('xing_id','0')
        year_id = self.get_argument('year_id','0')
        mileage = self.get_argument('mileage','0')
        buy_time = self.get_argument('buy_time','')
        userAuto = UserAuto()
        user = self.current_user
        userAuto.user = user.id
        # userAuto.brand_id = brand_id
        # userAuto.xing_id = xing_id
        userAuto.brand_code = year_id
        userAuto.mileage = mileage
        if not buy_time:
            userAuto.buy_time = 0
        else:
            userAuto.buy_time =  time.mktime(time.strptime(buy_time, "%Y-%m-%d"))
        if(id > 0):
            userAuto.id = id
        userAuto.save()
        self.redirect('/user/autos')
        # ft = (UserAuto.user == user.id)
        # items = UserAuto.select().where(ft).order_by(UserAuto.id.desc())
        # brands = Brand.select().where((Brand.is_delete == 0) & (Brand.pid == 0)).order_by(Brand.spell_abb, Brand.sort)
        # self.render('/user/autos.html', items=items, c='autos', brands=brands)

@route(r'/user/auto_del/(\d+)', name='user_auto_del')  # 删除我的汽车
class UserAutoDeleteHandler(UserBaseHandler):
    def get(self,id):
        UserAuto.delete().where(UserAuto.id == id).execute()
        self.flash(u"删除成功！")
        self.redirect('/user/autos')

@route(r'/user/balance', name='user_balance') # 我的余额
class UserBalanceHandler(UserBaseHandler):
    def get(self):
        page = int(self.get_argument("page", 1))
        pagesize = self.settings['user_pagesize']
        user = self.current_user
        #刷新用户信息
        userNew = User.get(User.id == user.id)
        balance = round(userNew.balance,2)
        q = Balance.select().where(Balance.user == user.id)
        total = q.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        list = q.order_by(Balance.id.desc()).paginate(page, pagesize)
        balances = map(self.bind_status_text, list)
        self.render('/user/balance.html', p=balance,items = balances, c='balance', total=total, page=page,
                    pagesize=pagesize, totalpage=totalpage)

    def bind_status_text(self, balance):
        if len(balance.log.split(' - {"sec_id"'))>1:
            balance.log = balance.log[0:4]
        return balance

@route(r'/user/top_up', name='user_topup') #账户充值
class TopUpHandler(UserBaseHandler):
    def get(self):
        price = self.get_argument('price', '0')
        self.render('/user/top_up.html', c='balance', price=price)
    def post(self):
        # self.render('/user/top_up.html', c='balance', price=u'由于车装甲仓库搬迁，自今日起暂停服务一个月。')
        user = self.current_user
        price = self.get_argument('price','0')
        ordernum = 'U' + str(user.id) + '_T' + str(time.time())
        gateway = self.get_argument("gateway")

        if gateway == 'Alipay':
            self.redirect("/alipay/topay_cz?tn=%s&price=%f" % (ordernum, float(price)))


@route(r'/user/success', name='success') #充值结果
class SuccessHandler(UserBaseHandler):
    def get(self):
        result = self.get_argument('result','')
        price = self.get_argument('price','')
        self.render('/user/success.html',result = result,price=price, c='balance')


@route(r'/user/password', name='user_password') #修改密码
class UserPasswordHandler(UserBaseHandler):
    def get(self):
       self.render('/user/password.html', c='password')
    def post(self):
        result = 0
        user = self.get_current_user()
        opwd = self.get_argument('old_password','')
        pwd = self.get_argument('password','')
        if user.check_password(opwd):
            user.password = User.create_password(pwd)
            user.save()
            self.session['user'] = user
            self.session.save()
            result = 1
            self.flash("修改成功")
        else:
            result = 0
            self.flash("原始密码不对")
        self.render('/user/password.html', result=result)


@route(r'/user/service', name='user_service') #我的售后咨询
class UserServiceHandler(UserBaseHandler):
    def get(self):
        user = self.current_user
        ft = (Consult.user == user.id)
        consults = Consult.select().where(ft).order_by(Consult.created.desc(),Consult.reply_time.desc())
        self.render('/user/service.html', consults=consults, c='service')


@route(r'/user/service-add', name='user_service_add') #我的售后咨询添加
class UserServiceAddHandler(UserBaseHandler):
    def get(self):
        self.render('/user/service_add.html', c='service')
    def post(self):
        result = 0
        user = self.get_current_user()
        isreceived = self.get_argument('isreceived',0)
        ordernum = self.get_argument('ordernum','')
        q_type = self.get_argument('q_type','')
        content = self.get_argument('comment','')
        contact = self.get_argument('username','')
        mobile = self.get_argument('mobile','')
        try:
            c = Consult()
            c.user = user.id
            c.type = q_type
            c.content = content
            c.contact = contact
            c.mobile = mobile
            c.order = ordernum
            c.isreceived = int(isreceived)
            c.created = time.time()
            c.save()
            result = 1
        except Exception, ex:
            logging.error(ex)
            result = 0

        user = self.current_user
        ft = (Consult.user == user.id)
        consults = Consult.select().where(ft).order_by(Consult.created.desc(),Consult.reply_time.desc())
        self.render('/user/service.html', consults=consults)


@route(r'/user/service_show/(\d+)', name='user_service_show') #我的售后咨询添加
class UserServiceShowHandler(UserBaseHandler):
    def get(self,cid):
        consult = Consult.get(id=cid)
        self.render('/user/service_show.html', consult=consult, c='service')


@route(r'/user/message', name='user_message') # 我的消息
class UserMessageHandler(UserBaseHandler):
    def get(self):
        user = self.current_user
        ft = (UserMessage.user == user.id)
        items = UserMessage.select().where(ft).order_by(UserMessage.send_time.desc())
        self.render('/user/message.html', items=items, c='message')

@route(r'/user/message_show/(\d+)', name='user_message_show') # 我的消息显示
class UserMessageShowHandler(UserBaseHandler):
    def get(self,cid):
        message = UserMessage.get(id=cid)
        message.has_read=1
        message.save()
        self.render('/user/message_show.html', message=message, c='message')
@route(r'/user/message_del/(\d+)', name='user_message_del') # 我的消息显示
class UserMessageShowHandler(UserBaseHandler):
    def get(self,cid):
        UserMessage.delete().where(UserMessage.id == cid).execute()
        self.redirect('/user/message')

@route(r'/user/score', name='user_score') #我的余额
class UserScoreHandler(UserBaseHandler):
    def get(self):
        page = int(self.get_argument("page", 1))
        pagesize = self.settings['user_pagesize']
        user = self.current_user
        userNew = User.get(User.id == user.id)
        #更新用户Session
        self.session['user'] = userNew
        self.session.save()
        score = userNew.score
        q = Score.select().where(Score.user == userNew.id)
        total = q.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        scores = q.order_by(Score.id.desc()).paginate(page, pagesize)
        self.render('/user/score.html', p=score,items = scores, c='score', total=total, page=page,
                    pagesize=pagesize, totalpage=totalpage)


@route(r'/user/comment/(\d+)', name='user_comment')  # 评价
class UserCommentHandler(BaseHandler):
    def get(self, pid):
        iid = self.get_argument('iid','')
        oid = self.get_argument('oid', '')
        p = Product.get(id = pid)
        self.render('/user/comment_add.html',p=p,iid=iid, oid=oid)
    def post(self, pid):
        oid = int(self.get_argument('oid',0))
        try:
            user = User.get(User.id == self.current_user.id)
            iid = int(self.get_argument('iid',0))
            qualityscore = int(self.get_argument('qualityscore',5))
            speedscore = int(self.get_argument('speedscore',5))
            pricescore = int(self.get_argument('pricescore',5))
            servicescore = int(self.get_argument('servicescore',5))
            comment = self.get_argument('comment','好评')

            order_item = OrderItem.select().where((OrderItem.order == oid) & (OrderItem.product == pid) & (OrderItem.hascomment == 0))
            if order_item.count() > 0:
                c = Comment()
                c.product = pid
                c.user = user.id
                c.qualityscore = qualityscore
                c.speedscore = speedscore
                c.pricescore = pricescore
                c.servicescore = servicescore
                c.comment = comment
                c.created = int(time.time())
                c.approvedby = 2
                c.status = 1
                c.save()
                # 如果评价超过30字，并且全五星好评，赠送抽奖机会一次
                if len(comment) > 30: # and qualityscore == 5 and speedscore == 5 and pricescore == 5 and servicescore == 5
                    user.raffle_count += 1
                    user.save()
                item = OrderItem.get(id = iid)
                item.hascomment = 1
                item.save()
                try:
                    ul=UserLevel.get(levelid=user.userlevel.levelid)
                    if ul:
                        stype=0
                        jftype=1
                        scorenum=ul.commentscore
                        log=u'会员评价商品获得%s奖励积分'
                        log=log%(scorenum)
                        user.updatescore(stype,jftype,scorenum,log)
                except Exception, ex:
                    logging.error(ex)
        except Exception, e:
            logging.error(e)

        self.redirect('/user/order/'+str(oid))


@route(r'/user/promote', name='user_promote')  # 我的好友推广
class UserScoreHandler(UserBaseHandler):
    def get(self):
        user = self.current_user
        promotes = User_Promote.select().where(User_Promote.old_user == user.id)
        u = User.get(id = user.id)
        s1 = base64.encodestring(u.username)
        #s2 = base64.decodestring(s1)
        self.render('/user/promote.html', promotes=promotes, u=u, d=s1, c='promote')


@route(r'/user/score/product/(\d+)', name='user_score_product')  # 提交积分换购
class UserScoreToProductHandler(UserBaseHandler):
    def get(self, jfid):
        user = self.current_user
        ft = (UserAddr.user == user.id) & (UserAddr.isactive == 1)
        addritems = UserAddr.select().where(ft).order_by(UserAddr.isdefault.desc(), UserAddr.id.desc())
        pa = Product_Activity.get(id=jfid)
        self.render("site/cart/jfconfirm.html", addritems=addritems, pa=pa, err='')

    def post(self, jfid):
        address_id = self.get_argument("address_id")    # 选中的送货地址ID
        prefer_delivery_day = self.get_argument("prefer_delivery_day")    # 选中送货时间

        user = self.current_user
        jfItem = Product_Activity.get(id=jfid)
        if user.score < jfItem.price:
            ft = (UserAddr.user == user.id) & (UserAddr.isactive == 1)
            addritems = UserAddr.select().where(ft).order_by(UserAddr.isdefault.desc(), UserAddr.id.desc())
            self.render("site/cart/jfconfirm.html", addritems=addritems, pa=jfItem, err='您的积分不足')
        else:
            ps = jfItem.product_standard
            order = Order()
            order.user = user.id
            order.address = address_id
            address = UserAddr.get(id=int(address_id))
            order.take_name = address.name
            order.take_tel = address.mobile +' '+address.tel
            order.take_address = address.city+' '+address.region+' '+address.street+' '+address.address
            if prefer_delivery_day == '':
                order.distributiontime = '工作日/周末/假日均可'
            elif prefer_delivery_day == 'weekend':
                order.distributiontime = '仅周末送货'
            elif prefer_delivery_day == 'weekday':
                order.distributiontime = '仅工作日送货'

            order.payment = 5  # 积分换购
            order.message = ''

            order.shippingprice = 0
            order.price = 0
            order.ordered = int(time.time())
            order.currentprice = 0
            order.status = 1    #订单状态 0等待付款 1付款成功 2已送货 3交易完成 4已取消,-1已删除
            order.ip = self.request.remote_ip
            order.order_from = 1 #网站下单
            order.ordereddate = time.strftime('%Y-%m-%d', time.localtime(order.ordered))    #下单日期，文本格式
            order.orderedtime = time.strftime('%H:%M:%S', time.localtime(order.ordered))    #下单时间，文本格式
            order.weight = round((ps.weight/500 * 1), 2)
            order.save()
            order.ordernum = 'U' + str(order.user.id) + '-S' + str(order.id)
            order.save()

            orderItem = OrderItem()
            orderItem.product = ps.product.id
            orderItem.order = order.id
            orderItem.product_standard = ps
            orderItem.price = 0
            orderItem.quantity = 1
            orderItem.weight = ps.weight
            orderItem.product_standard_name = ps.name
            orderItem.item_type = 2
            orderItem.save()
            product = Product.get(id=ps.product.id)
            product.orders += 1
            product.save()

            self.redirect("/cart/pay?result=success&tn=" +order.ordernum+"&price="+str(order.currentprice)+"&ptype=3")

@route(r'/user/gift', name='user_gift')     # 用户中心 我的礼品管理
class UserGiftHandler(UserBaseHandler):
    def get(self):
        status = int(self.get_argument("status", 1))
        current_time = time.strptime(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),'%Y-%m-%d %H:%M:%S')
        ft = (Gift.user ==self.current_user.id)
        if status == 3:
            ft = ft & (Gift.status < 1)
            gifts = Gift.select().where((time.mktime(current_time) > Gift.end_time) & ft)
        elif status == 2:
            ft = ft & (Gift.status == 1)
            gifts = Gift.select().where(ft)
        else:
            ft = ft & (Gift.status < 1)
            gifts = Gift.select().where((Gift.end_time > time.mktime(current_time)) & ft)
        self.render('/user/gift.html', c='gift', gifts=gifts, s=status)

@route(r'/user/products', name='user_products')  # 商品管理
class UserProductHandler(UserBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        cid = int(self.get_argument("pcategory", 0))
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", None)
        defaultstandard = self.get_argument("defaultstandard", None)
        status = int(self.get_argument("status", 1))
        ft = (Product.status > 0)

        if cid > 0:
            ft = ft & (Product.categoryfront == cid)
        if keyword:
            keyw = '%' + keyword + '%'
            ft = ft & (Product.name % keyw)
        if defaultstandard:
            ft = ft & (Product.defaultstandard % defaultstandard)
        ft = ft & (Product.status == status)

        if self.current_user.store:
            ft = ft  & (Product.store == self.current_user.store)
            q = Product.select(Product, CategoryFront).join(CategoryFront).where(ft)
            total = q.count()
            if total % pagesize > 0:
                totalpage = total / pagesize + 1
            else:
                totalpage = total / pagesize
            products = q.order_by(Product.created.desc()).paginate(page, pagesize).aggregate_rows()
        else:
            self.flash("<script>alert('您不是商家，无权使用。');</script>")
            total = 0
            totalpage = 0
            products = None
        categorys = CategoryFront.select(CategoryFront, db.fn.Left(CategoryFront.code, 2).alias('left2')). \
            where(db.fn.LENGTH(CategoryFront.code) == 6).order_by(CategoryFront.code, CategoryFront.slug)

        self.render('user/product/products.html', products=products, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, categorys=categorys, cid=cid, c='products', status=status, keyword=keyword,
                    dp=defaultstandard)

@route(r'/user/product/(\d+)', name='user_editproduct')  # 修改产品页
class UserEditProductHandler(UserBaseHandler):
    def get(self, pid):
        default_brand=''
        default_xing=''
        default_year=''
        default_category = ''
        default_category2 = ''
        default_category3 = ''
        if pid == '0':
            p = None
        else:
            p = Product.get(Product.id == pid)
            # p.prompt = p.prompt.replace("</br>", "\r\n")
            default_brand=p.brand_code[0:4]
            default_xing=p.brand_code[0:8]
            default_year=p.brand_code
            if len(p.categoryfront.code) == 12:
                default_category3 = p.categoryfront.id
                default_category2 = p.categoryfront.pid
                default_category = CategoryFront.get(id = p.categoryfront.pid)
            elif  len(p.categoryfront.code) == 8:
                default_category2 = p.categoryfront.id
                default_category = p.categoryfront.pid
            else:
                default_category = p.categoryfront.id
        categorys = CategoryFront.select(CategoryFront). \
            where(CategoryFront.pid == 0).order_by(CategoryFront.code)
        attributes = Attribute.select().where((Attribute.type == 1) & (Attribute.isactive == 1))
        brands = Brand.select().where((Brand.is_delete == 0) & (Brand.pid == 0)).order_by(Brand.spell_abb, Brand.sort)

        self.render('user/product/edit_product.html', p=p, categorys=categorys, attributes=attributes, c='add_product',
                    brands=brands,default_brand=default_brand,default_xing=default_xing,default_year=default_year,
                    default_category=default_category,default_category2=default_category2,default_category3=default_category3)

    def post(self, pid):
        resume = self.get_argument("presume", '')
        name = self.get_argument("pname", '')
        tags = self.get_argument("tags", '')
        sku = self.get_argument("psku", '')
        intro = self.get_argument("pintro", '')
        producer = self.get_argument("pproducer", '')
        metakeywords = self.get_argument("pmetakeywords", '')
        metadescription = self.get_argument("pmetadescription", '')
        metatitle = self.get_argument("pmetatitle", '')
        category = self.get_argument("category", '1')
        category3 = int(self.get_argument("category3", 1))
        p_from = self.get_argument("product_from", 'A')
        quality = self.get_argument("quality", '')
        standard = self.get_argument("standard", '')
        is_reserve = self.get_argument("is_reserve", '0')
        reserve_time = self.get_argument("reserve_time", '')
        is_score = int(self.get_argument("is_score", '0'))
        score_num = int(self.get_argument("score_num", 0))
        xgperusernum = int(self.get_argument("xgperusernum", '0'))
        xgtotalnum = int(self.get_argument("xgtotalnum", '0'))
        avg_quantity = int(self.get_argument("avg_quantity", '0'))
        bz_days = int(self.get_argument("bz_days", '0'))
        weights = int(self.get_argument("weights", '0'))
        brand_code = self.get_argument("year_id", '')
        is_bargain = int(self.get_argument("is_bargain", '0'))
        prompt = self.get_argument("prompt", '')
        service_time = int(self.get_argument("service_time", '0'))
        # prompt = prompt.replace("\r\n", "</br>")
        try:
            if pid == '0':
                p = Product()
                p.sku = sku.strip()
            else:
                p = Product.get(Product.id == pid)
            p.args = p_from
            if is_reserve == '1':
                p.is_reserve = is_reserve
                if reserve_time:
                    dg_time = time.strptime(reserve_time, "%Y-%m-%d")
                    p.reserve_time = time.mktime(dg_time)
            else:
                p.is_reserve = 0
                p.reserve_time = 0
            p.is_score = is_score
            if score_num:
                p.score_num = score_num
            if category3:
                p.categoryfront = category3
            else:
                p.categoryfront = category
            p.updatedtime = int(time.time())
            p.updatedby = self.get_admin_user()
            p.resume = resume
            p.name = name
            p.tags = tags
            p.intro = intro
            p.producer = producer
            p.metakeywords = metakeywords
            p.metadescription = metadescription
            p.metatitle = metatitle
            p.marketprice = 0
            p.quality = quality
            p.standard = standard
            p.xgperusernum = xgperusernum
            p.xgtotalnum = xgtotalnum
            p.avg_quantity = avg_quantity
            p.bz_days = bz_days
            p.weights = weights
            p.status = 2  # 默认下架
            p.brand_code = brand_code
            p.is_store = 1
            p.store = self.current_user.store
            p.is_bargain = is_bargain
            p.prompt = prompt
            p.service_time = service_time
            if self.current_user.store.area_code:
                p.area_code = self.current_user.store.area_code
                area = Area.select().where(Area.code == p.area_code)
                p.city_id = area[0].id
            p.save()
            if pid == '0':
                s = ProductStandard()
                s.name = ''
                s.tags = ''
                s.price = 0
                s.orginalprice = 0
                s.weight = 0
                s.ourprice = 0
                s.relations = []
                s.product = p
                s.save()
                s.relations = '[' + str(s.id) + ']'
                s.save()
                p.defaultstandard = s.id
                if p.sku == '':
                    p.sku = p.id
                p.created = int(time.time())
                p.categoryback = 1
                p.save()
                if not os.path.exists('upload/' + str(p.sku)):
                    os.mkdir('upload/' + str(p.sku))
            self.flash("保存成功")

            self.redirect('/user/product/' + str(p.id))
        except Exception, e:
            self.flash("保存失败，请联系管理员" + e.message)
            self.redirect('/user/product/0')

@route(r'/user/editprice/(\d+)/(\d+)', name='user_editprice')  # 修改产品价格
class UserEditPriceHandler(UserBaseHandler):
    def get(self, pid, sid):
        p = Product.get(Product.id == pid)
        if sid == '0':
            s = None
        else:
            s = ProductStandard.get(ProductStandard.id == sid)

        self.render('user/product/standard.html', p=p, s=s, active='products')

    def post(self, pid, sid):
        content = {}
        name = self.get_argument("sname", '')
        weight = float(self.get_argument("sweight", '0'))
        relations = self.get_argument("srelations", '[]')
        ourprice = float(self.get_argument("ourprice", '0'))
        price = float(self.get_argument("price", '0'))
        pf_price = float(self.get_argument("pf_price", '0'))
        p = Product.get(Product.id == pid)
        is_show = int(self.get_argument("is_show", '1'))
        orginalprice = float(self.get_argument("orginalprice", '0'))

        f = self.get_argument("f", '')

        if sid == '0':
            s = ProductStandard()
            content['operatetype'] = u'新建产品规格-' + p.name
            msg = u'范围：' + name + u'; 提取重量：' + str(weight) + u'; 关联产品编号：' +relations
        else:
            s = ProductStandard.get(ProductStandard.id == sid)
            content['operatetype'] = u'修改产品规格-' + p.name
            # content['standard'] = simplejson.dumps(str(s))
            msg = u'范围：由 [' + s.name + u'] 改为 ' + u'[' + name + u']; <br>提取重量：由 [' + \
                  str(s.weight) + u'] 改为 [' + str(weight) + u']; <br> 关联产品编号：由 [' + \
                  s.relations + u'] 改为 [' + relations + u']'
        s.name = name
        s.weight = weight
        s.relations = relations
        s.product = p
        s.price = price
        s.ourprice = ourprice
        s.pf_price = pf_price
        s.is_show = is_show
        s.orginalprice = orginalprice
        s.save()
        list = simplejson.loads(relations)
        pslist = ProductStandard.select().where(ProductStandard.id << list)
        for ps in pslist:
            ps.relations = relations
            ps.save()
        # 添加产品到StorePrice
        # qstore=Store.select().where(Store.store_type==0)
        # for store in qstore:
        #     qi=StorePrice.select().where((StorePrice.store==store.id)&(StorePrice.product==p.id))
        #     if qi.count()>0 and  qi[0].price<=0:#修改价格
        #         qi[0].price=s.ourprice * 2;
        #         qi[0].last_update_time=int(time.time())
        #         qi[0].save()

        self.redirect('/user/product/' + str(pid))

@route(r'/user/delpic/(\d+)', name='user_delpic')  # 删除产品图片
class DelPicHandler(UserBaseHandler):
    def get(self, pcid):
        p = ProductPic.get(ProductPic.id == pcid)
        content = {}
        content['operatetype'] = '删除产品图片'
        content['pcid'] = pcid
        content['path'] = p.path
        pid = p.product.id
        p.delete_instance()
        self.redirect('/user/product/' + str(pid))


@route(r'/user/delpic_topic/(\d+)', name='user_delpic_topic')  # 删除圈子主题图片
class DelPicHandler(UserBaseHandler):
    def get(self, pcid):
        p = CircleTopicPic.get(CircleTopicPic.id == pcid)
        content = {}
        content['operatetype'] = '删除圈子主题图片'
        content['pcid'] = pcid
        content['path'] = p.path
        pid = p.topic.id
        p.delete_instance()

        homedir = os.getcwd()

        oldImgPath = os.path.join(homedir +p.path)
        if os.path.exists(oldImgPath):
            os.remove(oldImgPath)
        ext = p.path.rsplit('.')[-1].lower()
        oldImgPath = oldImgPath.replace(ext,'mobile.'+ext)
        if os.path.exists(oldImgPath):
            os.remove(oldImgPath)
        self.redirect('/user/circle/' + str(pid))

@route(r'/user/store/delpic/(\d+)', name='user_del_pic')  # 删除门店图片
class DelStorePicHandler(UserBaseHandler):
    def get(self, pcid):
        p = StorePic.get(StorePic.id == pcid)
        if p.path != p.store.image:
            content = {}
            content['operatetype'] = '删除门店图片'
            content['pcid'] = pcid
            content['path'] = p.path
            p.delete_instance()
            homedir = os.getcwd()

            oldImgPath = os.path.join(homedir +p.path)
            if os.path.exists(oldImgPath):
                os.remove(oldImgPath)
            ext = p.path.rsplit('.')[-1].lower()
            oldImgPath = oldImgPath.replace(ext,'mobile.'+ext)
            if os.path.exists(oldImgPath):
                os.remove(oldImgPath)
        else:
            self.flash("<script>alert('封面图片不能删除！');</script>")
        self.redirect('/user/profile_store')

@route(r'/user/primarypic/(\d+)', name='user_primarypic')  # 设置产品图片
class UserDelPicHandler(UserBaseHandler):
    def get(self, pcid):
        p = ProductPic.get(ProductPic.id == pcid)
        content = {}
        content['operatetype'] = '设置主图'
        content['pcid'] = pcid
        content['old_path'] = p.product.cover
        content['current_path'] = p.path
        p.product.cover = p.path
        p.product.updatedtime = int(time.time())
        p.product.updatedby = self.get_admin_user()
        p.product.save()
        self.redirect('/user/product/' + str(p.product.id))

@route(r'/user/store/primarypic/(\d+)', name='user_store_primarypic')  # 设置门店封面图片
class UserStorePrimaryPicHandler(UserBaseHandler):
    def get(self, pcid):
        p = StorePic.get(StorePic.id == pcid)
        content = {}
        content['operatetype'] = '设置门店封面图片'
        content['pcid'] = pcid
        content['old_path'] = p.store.image
        content['current_path'] = p.path
        p.store.image = p.path
        p.store.last_update = int(time.time())
        p.store.save()
        # p.is_cover = 1
        # p.save()
        self.redirect('/user/profile_store')

@route(r'/user/changeproduct/(\d+)/(\d+)', name='user_changeproduct')  # 修改产品状态
class UserStatusProductHandler(UserBaseHandler):
    def get(self, pid, status):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        cid = int(self.get_argument("cid", 0))
        keyword = self.get_argument("keyword", None)
        ds = self.get_argument("ds", None)
        s = int(self.get_argument("status", 1))

        p = Product.get(Product.id == pid)
        content = {}
        content['operatetype'] = '修改产品状态'
        content['pid'] = pid
        content['old_status'] = p.status
        content['current_status'] = status
        p.status = status
        if int(status)==2:
            p.xgtotalnum=0
        p.updatedtime = int(time.time())
        p.updatedby = self.get_admin_user()
        p.save()
        self.redirect('/user/products?page=' + str(page) + '&pcategory=' + str(cid) + '&keyword='+ keyword +
                      '&defaultstandard=' + str(ds) + '&status=' + str(s))

@route(r'/user/news', name='user_news')  # 信息管理
class UserNewsHandler(UserBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        cid = int(self.get_argument("pcategory", 0))
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", None)
        ft = (StoreNews.status == 1)

        if cid > 0:
            ft = ft & (StoreNews.category == cid)
        if keyword:
            keyw = '%' + keyword + '%'
            ft = ft & (StoreNews.title % keyw)

        if self.current_user.store:
            ft = ft  & (StoreNews.store == self.current_user.store)
            q = StoreNews.select().where(ft)
            total = q.count()
            if total % pagesize > 0:
                totalpage = total / pagesize + 1
            else:
                totalpage = total / pagesize
            items = q.order_by(StoreNews.created.desc()).paginate(page, pagesize).aggregate_rows()
        else:
            self.flash("<script>alert('您不是商家，无权使用。');</script>")
            total = 0
            totalpage = 0
            items = None
        categorys = StoreNewsCategory.select().where(StoreNewsCategory.status == 1).order_by(StoreNewsCategory.id)

        self.render('user/news/news.html', items=items, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, categorys=categorys, cid=cid, c='news', keyword=keyword)
@route(r'/user/news/(\d+)', name='user_editnews')  # 修改信息页
class UserEditNewsHandler(UserBaseHandler):
    def get(self, pid):
        if pid == '0':
            p = None
        else:
            p = StoreNews.get(StoreNews.id == pid)
        categorys = StoreNewsCategory.select().where(StoreNewsCategory.status == 1).order_by(StoreNewsCategory.id)
        self.render('user/news/edit_news.html', p=p, categorys=categorys, active='news')

    def post(self, pid):
        title = self.get_argument("title", '')
        content = self.get_argument("content", '')
        category = int(self.get_argument("category", '1'))
        image = self.get_argument("image", '')
        try:
            if pid == '0':
                p = StoreNews()
                p.created = int(time.time())
            else:
                p = StoreNews.get(StoreNews.id == pid)
            p.store = self.current_user.store
            p.category = category
            p.title = title
            p.image = image
            p.content = content
            p.check_state = 1
            p.last_update = int(time.time())
            p.save()
            self.flash("保存成功")

            self.redirect('/user/news')
        except Exception, e:
            self.flash("保存失败，请联系管理员" + e.message)
            self.redirect('/user/news/0')

@route(r'/user/order/orders', name='user_orders')  # 订单管理
class UserOrderHandler(UserBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        status = int(self.get_argument("status", -1))
        pagesize = self.settings['admin_pagesize']
        ft = (Order.status > -1)
        keyword = self.get_argument("keyword", '')
        begindate = self.get_argument("begindate", '')
        enddate = self.get_argument("enddate", '')
        statuscheck = int(self.get_argument("statuscheck", '-1') if len(self.get_argument("statuscheck", '1')) > 0 else '-1')
        delivery = self.get_argument('delivery','')
        phone = self.get_argument("phone", '')
        order_type = int(self.get_argument("order_type", 0))

        ft = ft & (Order.order_type == order_type) & ((Order.store == self.current_user.store) | (Order.agent == self.current_user.store))
        if delivery:
            ft = ft & (Order.delivery == delivery)
        if keyword:
            keyw = '%' + keyword + '%'
            ft = ft & (Order.ordernum % keyw)
            status = -1
        if phone:
            ph = '%' + phone + '%'
            ft = ft & ((Order.take_tel % ph) | (Order.take_name % ph))
            status = -1
        if (phone == '') & (keyword == ''):
            if status != -1:
                if status == 0:  # 待付款
                    ft = ft & ((Order.status == 0) & ((Order.payment == 1) | (Order.payment == 3)))
                elif status == 1:  # 待处理
                    ft = ft & ((Order.status == 1) | ((Order.payment == 0) & (Order.status == 0)))
                    pagesize = 99999
                else:
                    ft = ft & (Order.status == status)
            else:
                if statuscheck != -1 and statuscheck != '':
                    if statuscheck == 0:  # 待付款
                        ft = ft & ((Order.status == 0) & ((Order.payment == 1 | (Order.payment == 3))))
                    elif statuscheck == 1:  # 待处理
                        ft = ft & ((Order.status == 1) | ((Order.payment == 0) & (Order.status == 0)))
                        pagesize = 99999
                    else:
                        ft = ft & (Order.status == statuscheck)
        if begindate and enddate:
            begin = time.strptime(begindate, "%Y-%m-%d")
            end = time.strptime((enddate + " 23:59:59"), "%Y-%m-%d %H:%M:%S")
            ft = ft & (Order.ordered > time.mktime(begin)) & (Order.ordered < time.mktime(end))

        q = Order.select().where(ft).order_by(Order.ordered.desc())
        total = q.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        orders = q.paginate(page, pagesize)
        for o in orders:
            oCount = Order.select().where((Order.id<o.id) & (Order.status>0) & (Order.status<5) & (Order.user==o.user)).count()
            o.pay_response = u'首单' if oCount==0 else u''
            o.trade_no = str(oCount + 1)
        deliverys = Delivery.select()
        agents = User.select().where(User.grade == 3)
        self.render('user/order/orders.html', orders=orders, total=total, page=page, pagesize=pagesize,
        totalpage=totalpage, status=status, c='orders', begindate=begindate, enddate=enddate, keyword=keyword,
        delivery=delivery, phone=phone, order_type=order_type, deliverys=deliverys, agents=agents)

@route(r'/user/product_from', name='user_product_from')  # 从厂家发布产品之选择厂家
class UserProductFromHandler(UserBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        ft = (User.isactive == 1) & (User.grade == 2) & (User.store is not None)
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", '')
        if keyword:
            keyw = '%' + keyword + '%'
            ft = ft & (Store.name % keyw)
        q = User.select().join(Store).where(ft).order_by(User.lsignined.desc())
        total = q.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        lists = q.paginate(page, pagesize)

        self.render('user/product/product_from1.html', lists=lists, total=total, page=page, pagesize=pagesize,
        totalpage=totalpage, c='product_from', keyword=keyword)

@route(r'/user/product_from/(\d+)', name='user_product_from2')  # 从厂家发布产品之选择产品
class UserProductFromHandler(UserBaseHandler):
    def get(self, sid):
        u = self.current_user
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        ft = (Product.is_pass == 1) & (Product.store == sid)
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", '')
        if keyword:
            keyw = '%' + keyword + '%'
            ft = ft & (Product.name % keyw)
        qs = Product.select().where(Product.store == u.store)
        ids_has = [n.source_id for n in qs if n.source_id>0]
        ft = ft & ~(Product.id << ids_has)
        if len(ids_has)==0:
            ids_has.append(0)

        q = Product.select().where(ft).order_by(Product.orders.desc())
        total = q.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        lists = q.paginate(page, pagesize)

        self.render('user/product/product_from2.html', lists=lists, total=total, page=page, pagesize=pagesize,
        totalpage=totalpage, c='product_from', keyword=keyword, sid=sid)

@route(r'/user/product_end/(\d+)', name='user_product_end')  # 从厂家发布产品之发布产品
class UserProductEndHandler(UserBaseHandler):
    def get(self, pid):
        u = self.current_user
        p = Product.get(Product.id == pid)
        pNew = Product()
        pNew.sku = random.randint(-10000, -1)
        pNew.name = p.name
        pNew.city_id = p.city_id  # todo: city_id error
        pNew.area_code = p.area_code  # todo: area_code error
        pNew.brand_code = p.brand_code
        pNew.cagegoryfront = p.categoryfront
        pNew.resume = p.resume
        pNew.intro = p.intro
        pNew.prompt = p.prompt
        pNew.args = p.args
        pNew.marketprice = p.marketprice
        pNew.cover = p.cover
        pNew.quantity = 0
        pNew.views = 0
        pNew.orders = 0
        pNew.status = p.status
        pNew.defaultstandard = p.defaultstandard
        pNew.created = int(time.time())
        pNew.metakeywords = p.metakeywords
        pNew.categoryfront = p.categoryfront
        pNew.metadescription = p.metadescription
        pNew.metatitle = p.metatitle
        pNew.updatedtime = int(time.time())
        # pNew.updatedby = p.categoryfront
        pNew.attribute = p.attribute
        pNew.tags = p.tags
        pNew.xgtotalnum = p.xgtotalnum
        pNew.xgperusernum = p.xgperusernum
        pNew.is_reserve = p.is_reserve
        pNew.reserve_time = p.reserve_time
        pNew.is_score = p.is_score
        pNew.score_num = p.score_num
        pNew.is_store = p.is_store
        pNew.store = u.store.id
        pNew.category_store = p.category_store
        pNew.avg_quantity = p.avg_quantity
        pNew.weights = p.weights
        pNew.is_pass = p.is_pass
        pNew.user = u.id
        pNew.comment_count = 0
        pNew.source_id = p.id
        pNew.is_recommend = 0
        pNew.is_bargain = 0
        pNew.save()
        pNew.sku = pNew.id
        pNew.save()
        pics = ProductPic.select().where((ProductPic.product == p.id) & (ProductPic.isactive == 1))
        for pic in pics:
            picNew = ProductPic()
            picNew.product = pNew.id
            picNew.path = pic.path
            picNew.isactive = 1
            picNew.user = u.id
            picNew.save()
        pss = ProductStandard.select().where((ProductStandard.product == p.id))
        for ps in pss:
            psNew = ProductStandard()
            psNew.product = pNew.id
            psNew.name = ps.name
            psNew.weight = ps.weight
            psNew.price = ps.price
            psNew.orginalprice = ps.orginalprice
            psNew.ourprice = ps.ourprice
            psNew.relations = ps.relations
            psNew.isactive = ps.isactive
            psNew.pf_price = ps.pf_price
            psNew.is_show = ps.is_show
            psNew.save()
            if ps.id == p.defaultstandard:
                pNew.defaultstandard = psNew.id
                pNew.save()
        self.flash(u"产品发布成功！")
        self.redirect('/user/product/' + str(pid))

@route(r'/qrcode', name='test_qrcode')  # 测试生成二维码
class UserQrcodeHandler(UserBaseHandler):
    def get(self):
        user = self.current_user
        path_dir = 'upload/' + str(user.id/10000) + '/' + str(user.id) + '/qrcode'
        if not os.path.exists('upload/' + str(user.id/10000)):
            os.mkdir('upload/' + str(user.id/10000))
        if not os.path.exists('upload/' + str(user.id/10000) + '/' + str(user.id)):
            os.mkdir('upload/' + str(user.id/10000) + '/' + str(user.id))
        if not os.path.exists(path_dir):
            os.mkdir(path_dir)

        seed = "1234567890"
        sa = []
        for i in range(12):
            sa.append(random.choice(seed))
            salt = ''.join(sa)

        filename = '%d%d.%s' % (int(time.time()), random.randint(1000, 9999), 'png')
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(salt)
        qr.make(fit=True)
        img = qr.make_image()
        img.save(path_dir + '/' + filename)
        self.render('user/order/order_qrcode.html',code=salt, path_dir=path_dir + '/' + filename)

@route(r'/user/question', name='user_question')  # 用户中心-我提出的问题
class UserQuestionHandler(UserBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        ft = (Question.is_delete == 0) & (Question.user == self.current_user)
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", '')
        if keyword:
            keyw = '%' + keyword + '%'
            ft = ft & (Question.name % keyw)
        q = Question.select().where(ft).order_by(Question.created.desc())
        total = q.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        lists = q.paginate(page, pagesize)

        self.render('user/ask/question.html', lists=lists, total=total, page=page, pagesize=pagesize,
        totalpage=totalpage, c='question', keyword=keyword)

@route(r'/user/a_question', name='user_a_question')  # 用户中心-我回答的问题
class UserAQuestionHandler(UserBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        ft = (Question.is_delete == 0) & (Answer.user == self.current_user)
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", '')
        if keyword:
            keyw = '%' + keyword + '%'
            ft = ft & (Question.name % keyw)
        q = Question.select().join(Answer, on=(Question.id == Answer.question)).where(ft).order_by(Question.created.desc()).distinct()
        total = q.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        lists = q.paginate(page, pagesize)

        self.render('user/ask/a_question.html', lists=lists, total=total, page=page, pagesize=pagesize,
        totalpage=totalpage, c='a_question', keyword=keyword)

@route(r'/user/question/(\d+)', name='user_question_edit')  # 修改信息页
class UserEditQuestionHandler(UserBaseHandler):
    def get(self, pid):
        result = int(self.get_argument('result', 0))
        if pid == '0':
            p = None
        else:
            p = Question.get(Question.id == pid)
        self.render('user/ask/question_edit.html', p=p, result=result, active='question')

    def post(self, pid):
        title = self.get_argument("title", '')
        content = self.get_argument("content", '')
        scores = 0
        clicks = 0
        answers = 0
        publish_from = ""
        check_status = 0
        is_recommend = 0
        is_anonymous = 0
        is_finish = 0
        is_delete = 0
        created = int(time.time())
        try:
            if pid == '0':
                p = Question()
                p.clicks = clicks
                p.answers = answers
                p.publish_from = publish_from
                p.check_status = check_status
                p.is_recommend = is_recommend
                p.is_anonymous = is_anonymous
                p.is_finish = is_finish
                p.is_delete = is_delete
                p.created = created
            else:
                p = Question.get(Question.id == pid)
            p.user = self.current_user
            p.title = title
            p.content = content
            p.scores = scores
            p.save()
            self.flash("保存成功")

            self.redirect('/user/question')
        except Exception, e:
            self.flash("保存失败，请联系管理员" + e.message)
            self.redirect('/user/question')

@route(r'/user/a_question/(\d+)', name='user_a_question_edit')  # 修改信息页
class UserEditAQuestionHandler(UserBaseHandler):
    def get(self, pid):
        result = int(self.get_argument('result', 0))
        p = Question.get(Question.id == pid)
        qa = Answer.select().where((Answer.question == pid)&(Answer.is_delete == 0)&(Answer.user == self.current_user))
        if qa.count()>0:
            answer = qa[0]
        else:
            answer = None
        self.render('user/ask/a_question_edit.html', p=p, result=result, answer=answer, active='a_question')

    def post(self, pid):
        content = self.get_argument("content", '')
        opposes = 0
        supports = 0
        need_money = float(self.get_argument("need_money", 0))
        publish_from = ""
        is_best = 0
        is_anonymous = 0
        is_delete = 0
        created = int(time.time())
        try:
            question = Question.get(Question.id == pid)
            qa = Answer.select().where((Answer.question == pid)&(Answer.is_delete == 0)&(Answer.user == self.current_user))
            if qa.count()>0:
                p = qa[0]
            else:
                p = Answer()
                p.opposes = opposes
                p.supports = supports
                p.publish_from = publish_from
                p.is_best = is_best
                p.is_anonymous = is_anonymous
                p.is_delete = is_delete
                p.created = created
                p.question = pid
                p.user = self.current_user
                question.answers = question.answers + 1
                question.save()
            p.need_money = need_money
            p.content = content
            p.save()
            self.flash("保存成功")

            self.redirect('/user/a_question')
        except Exception, e:
            self.flash("保存失败，请联系管理员" + e.message)
            self.redirect('/user/a_question')

@route(r'/user/circle', name='user_circle')  # 用户中心-我的圈子
class UserCircleHandler(UserBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        ft = (CircleTopic.is_delete == 0) & (CircleTopic.user == self.current_user)
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", '')
        if keyword:
            keyw = '%' + keyword + '%'
            ft = ft & (CircleTopic.content % keyw)
        q = CircleTopic.select().where(ft).order_by(CircleTopic.created.desc())
        total = q.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        lists = q.paginate(page, pagesize)

        self.render('user/circle/topic.html', lists=lists, total=total, page=page, pagesize=pagesize,
        totalpage=totalpage, c='circle', keyword=keyword)

@route(r'/user/circle/(\d+)', name='user_circle_edit')  # 修改信息页
class UserEditCircleHandler(UserBaseHandler):
    def get(self, pid):
        result = int(self.get_argument('result', 0))
        if pid == '0':
            p = None
        else:
            p = CircleTopic.get(CircleTopic.id == pid)
        self.render('user/circle/topic_edit.html', p=p, u=self.current_user, result=result, active='circle')

    def post(self, pid):
        is_finish = self.get_argument("is_finish", '0')
        title = self.get_argument("title", '')
        content = self.get_argument("content", '')
        clicks = 0
        publish_from = ""
        check_status = 0
        is_show_address = self.get_argument("is_show_address", 0)
        is_show_contact = self.get_argument("is_show_contact", 0)
        is_delete = 0
        created = int(time.time())
        try:
            if pid == '0':
                p = CircleTopic()
                p.clicks = clicks
                p.publish_from = publish_from
                p.check_status = check_status
                p.is_delete = is_delete
                p.created = created
                p.user = self.current_user
            else:
                p = CircleTopic.get(CircleTopic.id == pid)
            p.is_show_address = is_show_address
            p.is_show_contact = is_show_contact
            p.title = title
            p.content = content
            p.save()
            self.flash("保存成功")
            if is_finish == '1':
                self.redirect('/user/circle')
            else:
                self.redirect('/user/circle/'+str(p.id))
        except Exception, e:
            self.flash("保存失败，请联系管理员" + e.message)
            self.redirect('/user/circle')

@route(r'/user/settlement', name='user_settlement')  # 结算管理
class UserSettlementHandler(UserBaseHandler):
    def get(self):
        page = int(self.get_argument("page", 1))
        pagesize = self.settings['user_pagesize']
        ft = (Settlement.user == self.current_user)
        q = Settlement.select().where(ft)
        total = q.count()

        ftO = (Order.store == self.current_user.store) & (Order.status == 4) & (Order.settlement >> None)
        qO = Order.select().where(ftO)
        settle_money = 0
        for aa in qO:
            settle_money = settle_money + aa.price
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        lists = q.order_by(Settlement.created.desc()).paginate(page, pagesize)
        self.render('/user/order/settlement.html',c='settlement', lists=lists,  total=total, page=page,
                    pagesize=pagesize, totalpage=totalpage, u=self.current_user, settle_money=settle_money)

@route(r'/user/settlement_orders/(\d+)', name='user_settlement_orders')  # 结算页面
class UserSettlementOrdersHandler(UserBaseHandler):
    def get(self, sid):
        page = int(self.get_argument("page", 1))
        pagesize = self.settings['user_pagesize']
        ft = (Order.store == self.current_user.store) & (Order.status == 4) & (Order.settlement >> None)
        if int(sid)==0:
            s = None
            q = Order.select().where(ft)
            total = q.count()
            if total % pagesize > 0:
                totalpage = total / pagesize + 1
            else:
                totalpage = total / pagesize
            list = q.order_by(Order.ordered.desc()).paginate(page, pagesize)
            orders = map(self.bind_status_text, list)
        else:
            s = Settlement.get(Settlement.id == sid)
            orders = s.settlement_orders
            total = orders.count()
            page = 1
            pagesize = total
            totalpage = 1
        self.render('/user/order/settlement_orders.html',c='settlement', orders=orders,  total=total, page=page,
                    pagesize=pagesize, totalpage=totalpage, s = s)

    def bind_status_text(self, order):
        if order.status < 0:
            order.ip = u'已删除'
        elif (order.status == 0 or order.status == 1 or order.status == 2 or order.status == 3) and order.payment == 0:
            order.ip = u'正在处理'
        elif (order.payment == 3 or order.payment == 2 or order.payment == 1) and order.status == 0:
            order.ip = u'等待付款'
        elif (order.payment == 3 or order.payment == 2 or order.payment == 1) and order.status == 1:
            order.ip = u'已付款'
        elif order.status == 2 or order.status == 3: #order.payment == 1 and (order.status == 1 or order.status == 2 or order.status == 3):
            order.ip = u'正在处理'
        elif order.status == 4:
            order.ip = u'已完成'
        elif order.status == 5:
            order.ip = u'已取消'
        else:
            order.ip = u'正在处理'
        return order

@route(r'/user/withdrawals', name='user_withdrawals')  # 我的提现
class UserWithdrawalsHandler(UserBaseHandler):
    def get(self):
        u = self.current_user
        ft = (Withdraw.user == u.id)
        items = Withdraw.select().where(ft).order_by(Withdraw.id.desc())
        ytx_money = Withdraw.select( db.fn.SUM(Withdraw.sum_money).alias('sum_money')).where(ft&(Withdraw.status==2))[0].sum_money
        if not ytx_money:
            ytx_money = 0
        alipay_account_unall = u.alipay_account[:2]+"****"+u.alipay_account[u.alipay_account.find("@"):]
        bank_account_unall = u.bank_account[:4]+"**** ****"+u.bank_account[len(u.bank_account)-4:]
        self.render('/user/order/withdrawals.html', items=items, c='settlement', u=u, alipay_account_unall=alipay_account_unall, bank_account_unall=bank_account_unall,ytx_money=ytx_money)

    def post(self):
        # id= int(self.get_argument("id", 0))
        # user = self.current_user
        # brand_id = self.get_argument('brand_id','0')
        # xing_id = self.get_argument('xing_id','0')
        # year_id = self.get_argument('year_id','0')
        # mileage = self.get_argument('mileage','0')
        # buy_time = self.get_argument('buy_time','')
        # userAuto = UserAuto()
        # user = self.current_user
        # userAuto.user = user.id
        # # userAuto.brand_id = brand_id
        # # userAuto.xing_id = xing_id
        # userAuto.brand_code = year_id
        # userAuto.mileage = mileage
        # if not buy_time:
        #     userAuto.buy_time = 0
        # else:
        #     userAuto.buy_time =  time.mktime(time.strptime(buy_time, "%Y-%m-%d"))
        # if(id > 0):
        #     userAuto.id = id
        # userAuto.save()
        self.redirect('/user/withdrawals')

@route(r'/user/store_autos', name='user_store_autos') # 店铺可维修品牌管理
class UserStoreAutosHandler(UserBaseHandler):
    def get(self):
        id= int(self.get_argument("id", 0))
        user = self.current_user
        ft = (UserAuto.user == user.id)
        # items = UserAuto.select(UserAuto, 't2.name as brand_name').join(Brand,on=(UserAuto.brand_id == Brand.id)).\
        #     join(Brand,on=(UserAuto.xing_id == Brand.id)).join(Brand,on=(UserAuto.year_id == Brand.id)).where(ft).order_by(UserAuto.id.desc())
        sql = '''
       select a.*,b.name as brand_name,c.name as xing_name,d.name as year_name from tb_store_auto a
inner JOIN tb_brand b on left(a.brand_code,4)=b.code
inner JOIN tb_brand c on left(a.brand_code,8)=c.code
inner JOIN tb_brand d on a.brand_code=d.code where a.user_id=%s
        '''
        q = db.handle.execute_sql(sql % ( user.id))
        items = q.fetchall()
        brands = Brand.select().where((Brand.is_delete == 0) & (Brand.pid == 0)).order_by(Brand.spell_abb, Brand.sort)
        userAuto = None
        default_brand=''
        default_xing=''
        default_year=''
        if id>0:
            userAuto=StoreAuto.get(StoreAuto.id == id)
            default_brand=userAuto.brand_code[0:4]
            default_xing=userAuto.brand_code[0:8]
            default_year=userAuto.brand_code
        self.render('/user/account/store_autos.html', items=items, c='autos', brands=brands, userAuto=userAuto,default_brand=default_brand,default_xing=default_xing,default_year=default_year)
    def post(self):
        id= int(self.get_argument("id", 0))
        user = self.current_user
        brand_id = self.get_argument('brand_id','0')
        xing_id = self.get_argument('xing_id','0')
        year_id = self.get_argument('year_id','0')
        storeAuto = StoreAuto()
        user = self.current_user
        storeAuto.user = user.id
        storeAuto.store = user.store.id
        storeAuto.brand_code = year_id
        # storeAuto.brand_full_name = ''

        if(id > 0):
            storeAuto.id = id
        storeAuto.save()
        self.redirect('/user/store_autos')


@route(r'/user/store_auto_del/(\d+)', name='user_store_auto_del')  # 删除店铺可维修品牌
class UserStoreAutoDeleteHandler(UserBaseHandler):
    def get(self,id):
        StoreAuto.delete().where(StoreAuto.id == id).execute()
        self.flash(u"删除成功！")
        self.redirect('/user/store_autos')
