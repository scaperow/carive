#!/usr/bin/env python
# coding=utf8

from handler import AdminBaseHandler, BaseHandler
from lib.route import route
from lib.util import calprice
from model import AdminUser, User, Product, CategoryFront, Order, Ad, Page, Delivery, ProductPic, ProductStandard, \
    Coupon, OrderItem, PageBlock, CouponTotal, AdminLog, Invoicing,  DeliveryNumbers, \
    GroupOrder, UserAddr, Score, Inventory, Comment,AdType, \
    Attribute, ProductAttribute, InvoicingChanged, PayBack, Balance,Gift,\
    Topic,Topic_Discuss,Hot_Search,MobileBlock,Consult,Product_Activity,User_Raffle_Log,CouponRealTotal,CouponReal,\
    DeliveryOrderStatus,UserVcode,MediaNews,Product_Reserve,Store,UserInterview,ProductOffline,StorePrice, Brand, Area,\
UserMessage, Feedback, Question, Answer, CircleTopic, CircleTopicPic, CircleTopicReply, CircleTopicPraise, Withdraw, MobileUpdate
from bootloader import db
from lib.mqhelper import create_msg
import time
import datetime
import simplejson
import logging
import random
import uuid
import os
import urllib2
import json
from activity import new_user_order_coupon, create_coupon, create_coupon_real
from ajax2 import OrderChangeStatus
import setting
import re
# from test.mongo_sys_document import sys_log_data, import_log_data

@route(r'/admin', name='admin_index')  # 首页
class IndexHandler(AdminBaseHandler):
    def get(self):
        report = {}
        minday = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 0:0:0", time.localtime()), "%Y-%m-%d 0:0:0")))
        report['day_new_users'] = User.select().where((User.isactive == 1) & (User.signuped >= minday)).count()
        self.render('admin/index.html', report=report)


@route(r'/admin/logout', name='admin_logout')  # 退出
class LogoutHandler(AdminBaseHandler):
    def get(self):
        if "admin" in self.session:
            del self.session["admin"]
            self.session.save()
        self.render('admin/login.html')

@route(r'/admin/login', name='admin_login')  # 登录
class LoginHandler(BaseHandler):
    def get(self):
        self.render('admin/login.html')
    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)

        if username and password:
            try:
                user = AdminUser.get(AdminUser.username == username)
                if user.check_password(password):
                    if user.isactive == 1:
                        user.updatesignin()
                        self.session['admin'] = user
                        self.session.save()
                        self.redirect("/admin")
                        return
                    else:
                        self.flash("此账户被禁止登录，请联系管理员。")
                else:
                    self.flash("密码错误")
            except Exception, e:
                print e
                self.flash("此用户不存在")
        else:
            self.flash("请输入用户名或者密码")

        self.render("/admin/login.html", next=self.next_url)


@route(r'/admin/users', name='admin_users')  # 会员列表
class UserHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        key = self.get_argument("keyword", None)
        group = int(self.get_argument("group", -1))
        ordernum = self.get_argument("ordernum", None)
        order_sign = self.get_argument("order_sign", "")
        # order_count = self.get_argument("order_count", "")
        begindate = self.get_argument("begindate", '')
        enddate = self.get_argument("enddate", '')
        grade = int(self.get_argument("grade", -1))

        order_str = User.signuped.desc()
        if order_sign == '0':
            order_str = User.signuped.desc()
        elif order_sign == '1':
            order_str = User.signuped.asc()
        elif order_sign == '2':
            order_str = db.fn.COUNT(Order.user).desc()
        elif order_sign == '3':
            order_str = db.fn.COUNT(Order.user).asc()
        ft = (User.id > 0)

        if begindate and enddate:
            begin = time.strptime(begindate, "%Y-%m-%d")
            end = time.strptime((enddate + " 23:59:59"), "%Y-%m-%d %H:%M:%S")
            ft = ft & (User.signuped > time.mktime(begin)) & (User.signuped < time.mktime(end))

        if key:
            keyword = '%' + key + '%'
            ft = ft & (User.username % keyword)
        if group > -1:
            ft = ft & (User.isactive == group)
        if grade > -1:
            ft = ft & (User.grade == grade)
        uq = User.select(User,db.fn.COUNT(Order.user).alias('order_count')).join(Order, db.JOIN_LEFT_OUTER,
                                    on=((User.id==Order.user) &
                                    (((Order.status>-1) & (Order.payment==0)) | ((Order.payment>0) &
                                    (Order.status>0))) & (Order.payment<9) &
                                    (Order.status<5))).where(ft).group_by(User.id)
        total = uq.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        if ordernum:
            try:
                order = Order.get(Order.ordernum == ordernum)
                users = User.select().where(User.username == order.user.username)
                totalpage = 1
                total = 1
            except Exception, e:
                users = None
                self.flash("信息不存在")
        else:   #db.fn.COUNT(Order.user)
            users = uq.order_by(order_str).paginate(page, pagesize)

        self.render('/admin/user/user.html', users=users, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='users', keyword=key, ordernum=ordernum,order_sign=order_sign,
                    begindate=begindate,enddate=enddate)

@route(r'/admin/feedback', name='admin_feedback')  # 意见反馈列表
class UserFeedbackHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        key = self.get_argument("keyword", None)
        begindate = self.get_argument("begindate", '')
        enddate = self.get_argument("enddate", '')
        has_read = self.get_argument("has_read", '')

        ft = (Feedback.id > 0)

        if begindate and enddate:
            begin = time.strptime(begindate, "%Y-%m-%d")
            end = time.strptime((enddate + " 23:59:59"), "%Y-%m-%d %H:%M:%S")
            ft = ft & (Feedback.created > time.mktime(begin)) & (Feedback.created < time.mktime(end))

        if key and key != 'None':
            keyword = '%' + key + '%'
            ft = ft & (Feedback.content % keyword)
        else:
            key = ''

        if has_read:
            ft = ft & (Feedback.has_read == has_read)

        uq = Feedback.select().where(ft)
        total = uq.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        lists = uq.order_by(Feedback.created.desc()).paginate(page, pagesize)

        self.render('/admin/user/feedback.html', lists=lists, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='feedback', keyword=key, begindate=begindate,enddate=enddate, has_read=has_read)

@route(r'/admin/feedback_del/(\d+)', name='admin_feedback_del')  # 意见反馈删除
class UserFeedbackDelHandler(AdminBaseHandler):
    def get(self, fid):
        p = Feedback.get(Feedback.id == fid)
        p.delete_instance()
        self.redirect('/admin/feedback')

@route(r'/admin/factory', name='admin_factory')  # 厂家管理
class FactoryHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        key = self.get_argument("keyword", None)
        group = int(self.get_argument("group", -1))
        ordernum = self.get_argument("ordernum", None)
        order_sign = self.get_argument("order_sign", "")
        # order_count = self.get_argument("order_count", "")
        begindate = self.get_argument("begindate", '')
        enddate = self.get_argument("enddate", '')
        # grade = int(self.get_argument("grade", -1))

        order_str = User.signuped.desc()
        # if order_sign == '0':
        #     order_str = User.signuped.desc()
        # elif order_sign == '1':
        #     order_str = User.signuped.asc()
        # elif order_sign == '2':
        #     order_str = db.fn.COUNT(Order.user).desc()
        # elif order_sign == '3':
        #     order_str = db.fn.COUNT(Order.user).asc()
        ft = (User.id > 0)

        if begindate and enddate:
            begin = time.strptime(begindate, "%Y-%m-%d")
            end = time.strptime((enddate + " 23:59:59"), "%Y-%m-%d %H:%M:%S")
            ft = ft & (User.signuped > time.mktime(begin)) & (User.signuped < time.mktime(end))

        if key:
            keyword = '%' + key + '%'
            ft = ft & (User.username % keyword)
        if group > -1:
            ft = ft & (User.isactive == group)
        ft = ft & ((User.grade == 2) | (User.grade == 3))
        uq = User.select().where(ft)
        total = uq.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        if ordernum:
            try:
                users = User.select().where(ft)
                totalpage = 1
                total = 1
            except Exception, e:
                users = None
                self.flash("信息不存在")
        else:   #db.fn.COUNT(Order.user)
            users = uq.order_by(order_str).paginate(page, pagesize)

        self.render('/admin/user/factory.html', users=users, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='factory', keyword=key, ordernum=ordernum,order_sign=order_sign,
                    begindate=begindate,enddate=enddate)


@route(r'/admin/factory/(\d+)', name='admin_edit_factory')  # 修改产品页
class EditFactoryHandler(AdminBaseHandler):
    def get(self, uid):
        areas = Area.select().where((Area.is_delete == 0) & (Area.pid == 0)).order_by(Area.code)
        default_province=''
        default_city=''
        default_district=''
        if uid == '0':
            u = None
            s = None
        else:
            u = User.get(User.id == uid)
            s = u.store
            if s:
                default_province = s.area_code[0:4]
                default_city = s.area_code[0:8]
                default_district = s.area_code
        self.render('admin/user/factory_edit.html', u=u, s=s, areas=areas, active='factory',default_province=default_province,default_city=default_city,default_district=default_district)

    def post(self, uid):
        username = self.get_argument("username", '')
        password = self.get_argument("password", '')
        mobile = self.get_argument("mobile", '')
        name = self.get_argument("name", '')
        province_code = self.get_argument("province_code", '')
        city_code = self.get_argument("city_code", '')
        district_code = self.get_argument("district_code", '')
        address = self.get_argument("address", '')
        link_man = self.get_argument("link_man", '')
        grade = self.get_argument("grade", '')

        content = {}
        try:
            if uid == '0':
                u = User()
                s = Store()
                u.gender = 2
                u.isactive = 1
                now = int(time.time())
                signupeddate = time.strftime('%Y-%m-%d', time.localtime(now))
                signupedtime = time.strftime('%H:%M:%S', time.localtime(now))
                u.signuped = now
                s.is_certified = 1
                s.check_state = 1
                s.is_recommend = 0
                s.last_update = now
                s.created = now
            else:
                u = User.get(User.id == uid)
                s = u.store
            if password:
                password = User.create_password(password)
                u.password = password
            s.name = name
            s.mobile = mobile
            s.area_code = district_code
            s.address = address
            s.link_man = link_man
            s.save()
            u.username = username
            u.mobile = mobile
            u.grade = grade
            u.store = s
            u.save()

            self.flash("保存成功")

            self.redirect('/admin/factory')
        except Exception, e:
            self.flash("保存失败，请联系管理员" + e.message)
            self.redirect('/admin/factory')


@route(r'/admin/user/(\d+)', name='admin_user_detail')  # 会员管详情
class UserDetailHandler(AdminBaseHandler):
    def get(self, uid):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        user = User.get(id=uid)
        ft = (CouponTotal.status == 0)
        ft = ft & (Coupon.status == 1)
        ft = ft & (Coupon.user == uid)
        coupons = Coupon.select(Coupon, CouponTotal).join(CouponTotal, on=(Coupon.coupontotal == CouponTotal.id)).where(
            ft)
        coupons_real = CouponReal.select().where((CouponReal.status == 1) & (CouponReal.user == uid))
        gifts = Gift.select().where(Gift.user == uid)
        o = Order.select().where((Order.status>-1) & (Order.user==user))
        total = o.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        orders = o.order_by(Order.ordered.desc()).paginate(page, pagesize)

        address = UserAddr.select().where((UserAddr.user == uid) & (UserAddr.isactive == 1)).order_by(UserAddr.id.desc())

        self.render('admin/user/user_detail.html', u=user, coupons=coupons,orders=orders, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, address=address, active='users', coupons_real=coupons_real, gifts=gifts)

    def post(self, uid):
        user = User.get(id=uid)
        user.email = self.get_argument("email", '')
        user.birthday = self.get_argument('birthday', '')
        score_type = int(self.get_argument("score_type", -1))
        # add_score = int(self.get_argument("add_score", 0))
        user.grade = int(self.get_argument("grade",0))
        user.isactive = int(self.get_argument("isactive",1))

        user.save()

        # if score_type != -1 and add_score != 0:
        #     stype=score_type
        #     jftype=1
        #     if score_type == 0:
        #         log = u'系统后台赠送积分：%s' %  add_score
        #     else:
        #         log = u'系统后台扣除积分：%s' %  add_score
        #     user.updatescore(stype,jftype,add_score,log)

        self.flash("保存成功")
        self.redirect('/admin/user/' + str(uid))


@route(r'/admin/changeuser/(\d+)/(\d+)', name='admin_changeuser')  # 禁用或启用用户
class ChangeUserHandler(AdminBaseHandler):
    def get(self, uid, status):
        content = {}
        user = User.get(id=uid)
        content['old_status'] = user.isactive
        user.isactive = status
        user.save()
        content['userid'] = uid
        content['operatetype'] = '修改用户状态'
        content['current_status'] = status
        self.flash("用户状态切换成功")
        AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        self.redirect("/admin/user/" + str(uid))


@route(r'/admin/products', name='admin_products')  # 商品管理
class ProductHandler(AdminBaseHandler):
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
        q = Product.select(Product, CategoryFront).join(CategoryFront).where(ft)
        total = q.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        products = q.order_by(Product.created.desc()).paginate(page, pagesize).aggregate_rows()

        categorys = CategoryFront.select(CategoryFront, db.fn.Left(CategoryFront.code, 2).alias('left2')). \
            where(db.fn.LENGTH(CategoryFront.code) == 6).order_by(CategoryFront.code, CategoryFront.slug)

        self.render('admin/product/products.html', products=products, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, categorys=categorys, cid=cid, active='ps', status=status, keyword=keyword,
                    dp=defaultstandard)


@route(r'/admin/product/(\d+)', name='admin_editproduct')  # 修改产品页
class EditProductHandler(AdminBaseHandler):
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
        self.render('admin/product/edit_product.html', p=p, categorys=categorys, attributes=attributes, active='ps',
                    default_brand=default_brand,default_xing=default_xing,default_year=default_year,
                    default_category=default_category,default_category2=default_category2,default_category3=default_category3)

    def post(self, pid):
        resume = self.get_argument("presume", '')
        name = self.get_argument("pname", '')
        tags = self.get_argument("tags", '')
        sku = self.get_argument("psku", '')
        intro = self.get_argument("pintro", '')
        # quantity = self.get_argument("pquantity", '')
        producer = self.get_argument("pproducer", '')
        metakeywords = self.get_argument("pmetakeywords", '')
        metadescription = self.get_argument("pmetadescription", '')
        metatitle = self.get_argument("pmetatitle", '')
        # category = int(self.get_argument("pcategory", '1'))
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
        is_bargain = int(self.get_argument("is_bargain", '0'))
        is_recommend = self.get_argument("is_recommend", '0')
        content = {}
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
            # p.categoryfront = category
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
            #p.quantity = int(quantity)
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
            p.is_bargain = is_bargain
            if is_recommend == '1':
                 p.is_recommend = 1
            else:
                 p.is_recommend = 0
            # p.validate()
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
                content['operatetype'] = '创建产品'
            else:
                content['operatetype'] = '修改产品'
                # content['oldproduct'] = simplejson.dumps(str(p))
            self.flash("保存成功")
            # 添加产品到StorePrice
            qstore=Store.select()
            for store in qstore:
                qi=StorePrice.select().where((StorePrice.store==store.id)&(StorePrice.product==p.id))
                if qi.count()<=0:#添加
                    ps = ProductStandard.get(ProductStandard.id == p.defaultstandard)
                    storeprice=StorePrice()
                    storeprice.product=p
                    storeprice.product_standard=p.defaultstandard
                    storeprice.store=store.id
                    storeprice.price=ps.price*2
                    storeprice.last_update_time=int(time.time())
                    storeprice.last_user_id=0
                    storeprice.save()
            content['pid'] = p.id
            AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
            self.redirect('/admin/product/' + str(p.id))
        except Exception, e:
            self.flash("保存失败，请联系管理员" + e.message)
            self.redirect('/admin/product/0')


@route(r'/admin/changeproduct/(\d+)/(\d+)', name='admin_changeproduct')  # 修改产品状态
class StatusProductHandler(AdminBaseHandler):
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
        # if int(status)==1 and p.xgtotalnum==0:
        #     self.flash("要上架的商品限购总数不能为0！")
        # else:
        p.save()
        AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        self.redirect('/admin/products?page=' + str(page) + '&pcategory=' + str(cid) + '&keyword='+ keyword +
                      '&defaultstandard=' + str(ds) + '&status=' + str(s))


@route(r'/admin/delpic/(\d+)', name='admin_delpic')  # 删除产品图片
class DelPicHandler(AdminBaseHandler):
    def get(self, pcid):
        p = ProductPic.get(ProductPic.id == pcid)
        content = {}
        content['operatetype'] = '删除产品图片'
        content['pcid'] = pcid
        content['path'] = p.path
        pid = p.product.id
        p.delete_instance()
        AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        self.redirect('/admin/product/' + str(pid))


@route(r'/admin/primarypic/(\d+)', name='admin_primarypic')  # 设置产品图片
class DelPicHandler(AdminBaseHandler):
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
        AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        self.redirect('/admin/product/' + str(p.product.id))


@route(r'/admin/delprice/(\d+)', name='admin_delprice')  # 删除产品价格
class DelPriceHandler(AdminBaseHandler):
    def get(self, psid):
        p = ProductStandard.get(ProductStandard.id == psid)
        content = {}
        content['operatetype'] = '删除产品价格信息'
        content['standard'] = simplejson.dumps(str(p))
        pid = p.product.id
        p.delete_instance()
        AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        self.redirect('/admin/product/' + str(pid))


@route(r'/admin/primaryprice/(\d+)', name='admin_primaryprice')  # 设置默认产品价格
class DelPriceHandler(AdminBaseHandler):
    def get(self, psid):
        p = ProductStandard.get(ProductStandard.id == psid)
        content = {}
        content['operatetype'] = '设置默认产品价格'
        content['standard'] = simplejson.dumps(str(p))
        p.product.defaultstandard = p.id
        p.product.updatedtime = int(time.time())
        p.product.updatedby = self.get_admin_user()
        p.product.save()
        AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        self.redirect('/admin/product/' + str(p.product.id))


@route(r'/admin/editprice/(\d+)/(\d+)', name='admin_editprice')  # 修改产品价格
class EditPriceHandler(AdminBaseHandler):
    def get(self, pid, sid):
        p = Product.get(Product.id == pid)
        if sid == '0':
            s = None
        else:
            s = ProductStandard.get(ProductStandard.id == sid)

        self.render('admin/product/standard.html', p=p, s=s, active='products')

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

        f = self.get_argument("f", '')
        now = datetime.datetime.now()


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
        s.save()
        list = simplejson.loads(relations)
        pslist = ProductStandard.select().where(ProductStandard.id << list)
        for ps in pslist:
            ps.relations = relations
            ps.save()
        # 添加产品到StorePrice
        # qstore=Store.select().where(Store.storetype==0)
        # for store in qstore:
        #     qi=StorePrice.select().where((StorePrice.store==store.id)&(StorePrice.product==p.id))
        #     if qi.count()>0 and  qi[0].price<=0:#修改价格
        #         qi[0].price=s.ourprice * 2;
        #         qi[0].last_update_time=int(time.time())
        #         qi[0].save()

        content['psid'] = s.id
        AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        admins = AdminUser.select()
        receivers = [n.email for n in admins if len(n.email) > 0]
        email = {u'receiver': receivers, u'subject': content['operatetype'], u'body': msg}
        try:
            create_msg(simplejson.dumps(email), 'email')
        except:
            pass
        self.redirect('/admin/product/' + str(pid))


@route(r'/admin/categorys', name='admin_categorys')  # 分类管理
class CategoryHandler(AdminBaseHandler):
    def get(self):
        subquery = Product.select(db.fn.COUNT(Product.id)).where(Product.categoryfront == CategoryFront.id)
        # categorys = CategoryFront.select(CategoryFront, subquery.alias('p_count')). \
        #     join(Product, db.JOIN_LEFT_OUTER).where(db.fn.LENGTH(CategoryFront.code) == 6). \
        #     group_by(CategoryFront).order_by(CategoryFront.code)
        categorys = CategoryFront.select(CategoryFront, subquery.alias('p_count')). \
            join(Product, db.JOIN_LEFT_OUTER).where(CategoryFront.pid==0). \
            group_by(CategoryFront).order_by(CategoryFront.code)
        self.render('admin/category.html', categorys=categorys, active='categorys')

@route(r'/admin/category_del/(\d+)', name='admin_category_del')  # 删除分类
class AdminCategoryDelHandler(AdminBaseHandler):
    def get(self,id):
        items_sub = CategoryFront.select().where((CategoryFront.pid == id)&(CategoryFront.isactive == 1))
        if items_sub.count() == 0:
            items_sub_product = Product.select().where(Product.categoryfront == id)
            if items_sub_product.count() == 0:
                category =CategoryFront.get(CategoryFront.id == id)
                category.isactive = 0
                category.save()
                self.flash(u"删除成功！")
            else:
                self.flash(u"产品分类有产品存在，请先删除分类下的产品！")
        else:
            self.flash(u"产品分类包括下级分类，请先删除下级分类！")
        self.redirect('/admin/categorys')

@route(r'/admin/category/(\d+)', name='admin_category_edit')  # 编辑分类
class AddAreaHandler(AdminBaseHandler):
    def get(self, id):
        pid =int(self.get_argument("pid", 0))
        category = None
        if int(id) > 0:
            category = CategoryFront.get(CategoryFront.id == id)
            pid = category.pid
        if pid > 0:
            brandP = CategoryFront.get(CategoryFront.id == pid)
        else:
            brandP = CategoryFront()
            brandP.id = 0
            brandP.name = "根目录"
        options_parent = "<option value=\"%s\" selected>%s</option>" % (brandP.id , brandP.name)
        is_continue = 0
        self.render('admin/category_edit.html', active='area', category=category, options_parent=options_parent, id=int(id), is_continue = is_continue)

    def post(self, id):
        pid = int(self.get_argument("pid", 0))
        name = self.get_argument("name", '')
        slug = int(self.get_argument("slug", 99))
        type = self.get_argument("type", '')
        if not name:
            self.flash(u"请输入名称！")
        if int(id) > 0:
            show_msg = "修改"
            category = CategoryFront.get(CategoryFront.id == id)
        else:
            show_msg = "添加"
            category = CategoryFront()
            category.pid = pid
        category.name = name
        category.slug = slug
        category.type = type
        try:
            if self.request.files:
                datetime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))  # 获取当前时间作为图片名称
                filename = str(datetime) + ".jpg"
                if not os.path.exists('upload/category'):
                        os.mkdir('upload/category')
                with open('upload/category/' + filename, "wb") as f:
                    f.write(self.request.files["file"][0]["body"])
                category.img_m = '/upload/category/' + filename
                # if self.settings['syncimg']:
                #     urls = []
                #     urls.append('http://admin.eofan.com'+'/upload/category/' + filename)
                #     create_msg(simplejson.dumps(urls), 'img')

            category.save()
            if pid > 0:
                categoryP = CategoryFront.get(CategoryFront.id == pid)
                categoryP.has_sub = 1
                categoryP.save()
                if int(id) == 0:
                    parent = CategoryFront.select(db.fn.Max(CategoryFront.code).alias('code')).where(CategoryFront.pid == pid)

                    if len(parent[0].code) > 4:
                        l_code = parent[0].code[0:len(parent[0].code) - 4]
                        r_code = parent[0].code[len(parent[0].code) - 4:len(parent[0].code)]
                        new_code = int(r_code) + 1
                        new_code = str(new_code).rjust(4, '0')
                        category.code = l_code + new_code
                        category.save()
                    else:
                        new_code = categoryP.code + '0001'
                        category.code = new_code
                        category.save()
            elif int(id) == 0:
                parent = CategoryFront.select(db.fn.Max(CategoryFront.code).alias('code')).where(CategoryFront.pid == 0)
                if parent[0].code:
                    new_code = int(parent[0].code) + 1
                else:
                    new_code = 1
                new_code = str(new_code).rjust(4, '0')
                category.code = new_code
                category.save()

            self.flash(show_msg + u"成功")
        except Exception, ex:
            self.flash(str(ex))
        self.redirect('/admin/categorys')


@route(r'/admin/category/list/(\d+)', name='admin_categorys_list')  # 分类产品列表管理
class CategoryListHandler(AdminBaseHandler):
    def get(self, cid):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']

        category = CategoryFront.get(id=cid)

        ft = ((Product.status > 0) & (Product.categoryfront == category))
        q = Product.select().where(ft)
        total = q.count()

        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        products = q.paginate(page, pagesize)

        self.render('admin/category_product.html', products=products, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, category=category, active='categorys')


@route(r'/admin/password', name='password')  # 密码管理
class PasswordHandler(AdminBaseHandler):
    def get(self):
        self.render('admin/password.html', active='password')

    def post(self):
        opassword = self.get_argument("Password", None)
        password = self.get_argument("NPassword", None)
        apassword = self.get_argument("RNPassword", None)
        if opassword and password and apassword:
            if len(password) < 6:
                self.flash("请确认输入6位以上新密码")
            elif password != apassword:
                self.flash("请确认新密码和重复密码一致")
            else:
                user = self.get_admin_user()
                if user.check_password(opassword):
                    user.password = AdminUser.create_password(password)
                    user.save()
                    self.session['admin'] = user
                    self.session.save()
                    self.flash("修改密码成功。")
                else:
                    self.flash("请输入正确的原始密码")
        else:
            self.flash("请输入原始密码和新密码")
        self.redirect('/admin/password')


@route(r'/admin/orders', name='admin_orders')  # 订单管理
class OrderHandler(AdminBaseHandler):
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

        ft = ft & (Order.order_type == order_type)
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
            for i in o.items:
                pr = Product_Reserve.select().where(Product_Reserve.product == i.product)
                if pr.count() > 0:
                    o.delivery_time = pr[0].delivery_time
        self.render('admin/order/orders.html', orders=orders, total=total, page=page, pagesize=pagesize,
        totalpage=totalpage, status=status, active='orders',begindate=begindate,enddate=enddate,keyword=keyword,
        delivery=delivery, phone=phone,order_type=order_type)

@route(r'/admin/bulk_store_sel', name='admin_bulk_store_sel')  # 选择散装产品
class AdminStoreSelHandler(AdminBaseHandler):
    def get(self):
        active = 'bulk_product_sel'
        stores=Store.select().where(Store.storetype==1).order_by(Store.id)
        self.render('/admin/order/bulk_store_sel.html', stores=stores, active=active)

@route(r'/admin/ajax/adminUpdateStorePrice', name='adminUpdateStorePrice')  # 将产品加入批发购物车
class AdminUpdateStorePriceHandler(AdminBaseHandler):
    def get(self):
        result = 0
        try:
            isid = int(self.get_argument("isid", 0))
            price = float(self.get_argument("price", 0.0))
            if self.get_admin_user():
                inventory = StorePrice.get(StorePrice.id==isid)
                inventory.price=price
                inventory.save()
                inventory.last_time=int(time.time())
                result=1
        except Exception, ex:
            logging.error(ex)
            result = 0
        self.write(simplejson.dumps(result))

@route(r'/admin/order/(\d+)', name='admin_order_detail')  # 订单详情
class OrderDetailHandler(AdminBaseHandler):
    def get(self, oid):
        o = Order.get(id=oid)
        num = '%' + o.ordernum + '%'
        topic = Topic.select().where(Topic.title % num).limit(1)
        tid = 0
        if topic.count() == 1:
            tid = topic[0].id
        stores=Store.select().where(Store.store_type==0)
        self.render('admin/order/order_detail.html', o=o,stores=stores, active='orders', tid=tid)

    def post(self, oid):
        o = Order.get(id=oid)
        summary = self.get_argument("psummary", '')
        flag = int(self.get_argument("order_flag", '0'))
        # payback = self.get_argument("payback", None)
        deliverynum = self.get_argument("deliverynum", '')
        delivery = self.get_argument('delivery', None)

        content = {}
        content['operatetype'] = '修改订单详情'
        content['order'] = simplejson.dumps(str(o))
        with db.handle.transaction():
            if o.deliverynum and (not o.deliverynum == deliverynum):
                o.deliverynum = deliverynum
                q = DeliveryNumbers.select().where(DeliveryNumbers.num == o.deliverynum)
                if q.count() > 0:
                    q[0].status = 0
                    q[0].save()
                q2 = DeliveryNumbers.select().where(DeliveryNumbers.num == deliverynum)
                if q2.count() > 0:
                    q2[0].status = 0
                    q2[0].save()
            if delivery == '':
                delivery = None
            content_d = {}
            content_d['order'] = simplejson.dumps(str(o))
            content_d['delivery'] = delivery
            if o.delivery != delivery:
                if o.delivery:
                    content_d['old_delivery'] = str(o.delivery)
                    content_d['text'] = u'修改物流公司，将原物流公司'+o.delivery.name+u'修改为' + delivery
                else:
                    content_d['old_delivery'] = ''
                    content_d['text'] = u'修改物流公司，将原物流公司 未指定 修改为' + delivery
                AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content_d)
            o.delivery = delivery
            o.deliverynum = deliverynum
            o.flag = flag
            o.summary = summary
            o.lasteditedby = self.get_admin_user().username
            o.lasteditedtime = int(time.time())
            # if payback:
            #     o.needpayback = 0
            o.save()
        self.flash("保存成功")
        AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        self.render('admin/order/order_detail.html', o=o, active='orders')


@route(r'/admin/order_payback', name='admin_order_payback')  # 退款订单列表
class OrderPayBackHandler(AdminBaseHandler):
    def get(self):
        status = int(self.get_argument("status", '0'))
        keyword = self.get_argument("keyword", '')
        ft = (PayBack.status == status)
        if len(keyword) > 0:
            keyw = '%' + keyword + '%'
            ft = ((Order.ordernum % keyw) | (Order.take_name % keyw) | (Order.take_tel % keyw))

        paybacks = PayBack.select(PayBack).join(Order).where(ft)
        self.render('admin/order/order_payback.html', paybacks=paybacks, keyword=keyword, active='order_payback', status=status)


@route(r'/admin/order/payback/(\d+)', name='admin_order_payback_by_admin')  # 管理员处理订单退款
class OrderPaybackHandler(AdminBaseHandler):
    def post(self, oid):
        order = Order.get(id=oid)
        msg = ''
        backprice = self.get_argument("backprice", '0')
        backreason = self.get_argument("backreason", '')
        payback_type = self.get_argument("payback_type", '2')  # 默认是原路退回
        hasprice = sum([n.price for n in order.paybacks if n.status > -1])
        hasprice = hasprice if hasprice else 0
        if len(backprice) > 0 and (not backprice == '0'):
            if payback_type == '1':  # 返回余额
                balance = Balance()
                balance.user = order.user
                balance.balance = float(backprice)
                balance.stype = 0
                balance.log = u'系统退款-订单编号：'+ order.ordernum
                balance.created = int(time.time())
                balance.save()
                msg = '退款成功'
            elif payback_type == '2':  # 原路返回
                if order.payment == 1 or order.payment == 3:
                    if (float(backprice) + hasprice) > float(order.currentprice - (order.pay_balance if order.pay_balance else 0)):
                        msg = '退款总金额已经超出用户支付金额，请检查'
                    else:
                        pb = PayBack()
                        pb.order = order
                        pb.user = order.user
                        pb.price = float(backprice)
                        pb.batch_no = ''
                        pb.trade_no = order.trade_no
                        pb.reason = backreason
                        pb.pay_account = order.pay_account
                        pb.back_by = 1
                        pb.createdby = self.get_admin_user().username
                        pb.createdtime = int(time.time())
                        pb.status = 0
                        pb.save()
                        msg = '退款成功'
                        admins = AdminUser.select(db.fn.Distinct(AdminUser.email)).where((AdminUser.roles % '%F%') | (AdminUser.roles % '%A%')).dicts()
                        receivers = [n['email'] for n in admins if len(n['email']) > 0]
                        body = u'订单号：'+order.ordernum+u', 需退款'+str(backprice)+u'元； 请核实并尽快处理'
                        email = {u'receiver': receivers, u'subject': u'产生取消订单，退款请求', u'body': body}
                        try:
                            create_msg(simplejson.dumps(email), 'email')
                        except:
                            pass
                elif order.payment == 2:
                    balance = Balance()
                    balance.user = order.user
                    balance.balance = float(backprice)
                    balance.stype = 0
                    balance.log = u'系统退款-订单编号：'+ order.ordernum
                    balance.created = int(time.time())
                    balance.save()
                    msg = '退款成功'
        else:
            msg = '退款金额输入错误'
        self.flash(msg)
        self.render('admin/order/order_detail.html', o=order, active='orders')


@route(r'/admin/skus', name='admin_skus')  # sku管理
class SKUHandler(AdminBaseHandler):
    def get(self):
        status = int(self.get_argument("status", -1))
        begindate = self.get_argument("begindate", '')
        enddate = self.get_argument("enddate", '')
        statuscheck = int(self.get_argument("statuscheck", -1))
        category = self.get_argument("category", '')
        ft = (Order.status > -1)&(Order.order_type==0)
        if status != -1:
            if status == 0:  # 待付款
                ft = ft & ((Order.status == 0) & (Order.payment == 1))
            elif status == 1:  # 待处理
                ft = ft & ((Order.status == 1) | ((Order.payment == 0) & (Order.status == 0)))
            else:
                ft = ft & (Order.status == status)
        else:
            if statuscheck != -1:
                if statuscheck == 0:  # 待付款
                    ft = ft & ((Order.status == 0) & (Order.payment == 1))
                elif statuscheck == 1:  # 待处理
                    ft = ft & ((Order.status == 1) | ((Order.payment == 0) & (Order.status == 0)))
                else:
                    ft = ft & (Order.status == statuscheck)

        if category == '01':
            ft = ft & (Product.sku % '01%')
        elif category == '02':
            ft = ft & (Product.sku % '02%')
        elif category == '03':
            ft = ft & (Product.sku % '03%')
        if begindate and enddate:
            begindate1 = time.strptime(begindate, "%Y-%m-%d %H:%M:%S")
            enddate1 = time.strptime(enddate, "%Y-%m-%d %H:%M:%S")
            ft = ft & (Order.ordered > time.mktime(begindate1)) & (Order.ordered < time.mktime(enddate1))

        skus = Product.select(Product, db.fn.SUM(OrderItem.quantity).alias('quantity'),
                              Product.quantity.alias('quantity1')). \
            join(OrderItem, on=(Product.id == OrderItem.product)). \
            join(Order, on=(Order.id == OrderItem.order)). \
            group_by(Product).where(ft).order_by(db.fn.SUM(OrderItem.quantity).desc(), Product.sku).aggregate_rows()

        self.render('admin/order/skus.html', skus=skus, status=status, active='skus', category=category,begindate=begindate,enddate=enddate)

@route(r'/admin/sum_skus', name='admin_sum_skus')  # sku管理
class SumSKUHandler(AdminBaseHandler):
    def get(self):
        status = int(self.get_argument("status", '0') if len(self.get_argument("status", '0')) > 0 else '0')
        begindate = self.get_argument("begindate", '')
        enddate = self.get_argument("enddate", '')
        category = self.get_argument("category", '')
        ft =  ((Order.status == 1) | (Order.status == 2) | ((Order.payment == 0) & (Order.status == 0)))&(Order.order_type==0)
        if category == '01':
            ft = ft & (Product.sku % '01%')
        elif category == '02':
            ft = ft & (Product.sku % '02%')
        elif category == '03':
            ft = ft & (Product.sku % '03%')
        if begindate and enddate:
            begindate1 = time.strptime(begindate, "%Y-%m-%d %H:%M:%S")
            enddate1 = time.strptime(enddate, "%Y-%m-%d %H:%M:%S")
            ft = ft & (Order.ordered > time.mktime(begindate1)) & (Order.ordered < time.mktime(enddate1))

        qskus = Product.select(Product, db.fn.SUM(OrderItem.quantity).alias('quantity'),
                              Product.quantity.alias('quantity1')). \
            join(OrderItem, on=(Product.id == OrderItem.product)). \
            join(Order, on=(Order.id == OrderItem.order)). \
            group_by(Product).where(ft).order_by(db.fn.SUM(OrderItem.quantity).desc(), Product.sku).aggregate_rows()

        skus=[]
        for s in qskus:
            skus.append({
                "name":s.name,
                "sku":s.sku,
                "standard_name":s.standards[0].name,
                "standard_weight":s.standards[0].weight,
                "quantity1":s.quantity1,
                "standard_ourprice":s.standards[0].ourprice,
                "quantity":s.quantity
            })
        self.render('admin/order/skus_sum.html', skus=skus, status=status, active='skus', category=category,begindate=begindate,enddate=enddate)

@route(r'/admin/ads', name='admin_ads')  # 首页广告
class AdHandler(AdminBaseHandler):
    def get(self):
        ads = Ad.select()
        self.render('admin/ad/ads.html', ads=ads, active='ads')

@route(r'/admin/ad_type', name='admin_ad_type')  # 广告类型
class AdTypeHandler(AdminBaseHandler):
    def get(self):
        ads = AdType.select()
        self.render('admin/ad/ad_type.html', ads=ads, active='ads')

@route(r'/admin/edit_ad_type/(\d+)', name='admin_edit_ad_type')
class EditAdTypeHandler(AdminBaseHandler):
    def get(self, aid):
        if aid == '0':
            ad_type = AdType()
        else:
            try:
                ad_type = AdType.get(id=int(aid))
            except:
                self.flash("此广告不存在")
                self.redirect("/admin/ad_type")
                return

        self.render('admin/ad/edit_ad_type.html', ad_type=ad_type, active='ads')

    def post(self, aid):
        aid = int(aid)
        name = self.get_argument("name", None)
        remark = self.get_argument("remark", None)

        try:
            if aid == 0:
                ad = AdType()
            else:
                ad = AdType.get(id=aid)
            ad.name = name
            ad.remark = remark
            ad.save()
            self.flash(u"广告类型修改成功")
            self.redirect("/admin/ad_type")
            return
        except Exception, ex:
            self.flash(str(ex))
            self.redirect("/admin/ad_type")
            # self.render('admin/ad/edit_ad_type.html', ad=ad, active='ads')

@route(r'/admin/addad', name='admin_addad')  # 添加广告
class AddAdHandler(AdminBaseHandler):
    def get(self):
        items = Area.select().where((Area.pid==0) & (Area.is_delete == 0) & (Area.is_site == 1)).order_by(Area.spell,Area.sort)
        adtypes = AdType().select()
        self.render('admin/ad/addad.html',items=items, adtypes=adtypes, active='ads')

    def post(self):
        url = self.get_argument("url", None)
        imgalt = self.get_argument("imgalt", None)
        sort = int(self.get_argument("sort", 1))
        type = int(self.get_argument("type", 0))
        province_code = self.get_argument("province_code", None)
        city_code = self.get_argument("city_code", None)
        remark = self.get_argument("remark", None)

        if self.request.files:
            ad = Ad()
            ad.url = url
            ad.atype = type
            ad.imgalt = imgalt
            ad.sort = sort
            ad.remark = remark
            try:
                if province_code != '' and city_code != '':
                    ad.city = city_code
                datetime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))  # 获取当前时间作为图片名称
                filename = str(datetime) + ".jpg"
                if not os.path.exists('upload/ad'):
                        os.mkdir('upload/ad')
                with open('upload/ad/' + filename, "wb") as f:
                    f.write(self.request.files["file"][0]["body"])

                ad.picurl = filename
                ad.save()
                if self.settings['syncimg']:
                    urls = []
                    urls.append('http://admin.eofan.com'+'/upload/ad/' + filename)
                    create_msg(simplejson.dumps(urls), 'img')
                self.flash(u"广告添加成功")
                self.redirect("/admin/ads")
            except Exception, ex:
                self.flash(str(ex))
        else:
            self.flash(u"请选择图片")
        self.render('admin/ad/addad.html', active='ads')


@route(r'/admin/editad/(\d+)', name='admin_editad')
class EditAdHandler(AdminBaseHandler):
    def get(self, aid):
        items = Area.select().where((Area.pid==0) & (Area.is_delete == 0) & (Area.is_site == 1)).order_by(Area.spell,Area.sort)
        aid = int(aid)

        try:
            ad = Ad.get(id=aid)
        except:
            self.flash("此广告不存在")
            self.redirect("/admin/ads")
            return
        adtypes = AdType.select()
        self.render('admin/ad/editad.html', items=items, ad=ad, adtypes=adtypes, active='ads')

    def post(self, aid):
        aid = int(aid)

        url = self.get_argument("url", None)
        imgalt = self.get_argument("imgalt", None)
        sort = int(self.get_argument("sort", 1))
        type = int(self.get_argument("type", 0))
        province_code = self.get_argument("province_code", None)
        city_code = self.get_argument("city_code", None)
        remark = self.get_argument("remark", None)
        try:
            ad = Ad.get(id=aid)
        except:
            self.flash("此广告不存在")
            self.redirect("/admin/ads")
            return

        ad.url = url
        ad.imgalt = imgalt
        ad.sort = sort
        ad.atype = type
        ad.remark = remark
        try:
            if province_code != '' and city_code != '':
                ad.city = city_code
            if self.request.files:
                datetime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))  # 获取当前时间作为图片名称
                filename = str(datetime) + ".jpg"
                with open('upload/ad/' + filename, "wb") as f:
                    f.write(self.request.files["file"][0]["body"])
                ad.picurl = filename
                if self.settings['syncimg']:
                    urls = []
                    urls.append('http://admin.eofan.com'+'/upload/ad/' + filename)
                    create_msg(simplejson.dumps(urls), 'img')
            ad.validate()
            ad.save()
            self.flash(u"广告修改成功")
            self.redirect("/admin/ads")
            return
        except Exception, ex:
            self.flash(str(ex))
            self.redirect("/admin/editad/"+str(aid))

        self.render('admin/ad/editad.html', ad=ad, active='ads')


@route(r'/admin/delad/(\d+)', name='admin_delad')
class DelAdHandler(AdminBaseHandler):
    def get(self, aid):
        Ad.delete().where(Ad.id == aid).execute()
        self.flash(u"广告删除成功")
        self.redirect("/admin/ads")


@route(r'/admin/pages', name='admin_pages')  # 静态页管理
class PageHandler(AdminBaseHandler):
    def get(self):
        keyword = self.get_argument("keyword", None)
        ft = (Page.isactive == 1)
        if keyword:
            keyword = '%' + keyword + '%'
            ft = ft & (Page.name % keyword)
        pages = Page.select().where(ft)
        self.render('admin/static_pages/pages.html', pages=pages, active='pages')


@route(r'/admin/delpage/(\d+)', name='admin_delpage')  # 删除静态页
class DelPageHandler(AdminBaseHandler):
    def get(self, pid):
        try:
            p = Page.get(id=pid)
            p.isactive = 0
            p.save()
        except:
            self.flash("删除失败")
        self.redirect("/admin/pages")


@route(r'/admin/editpage/(\d+)', name='admin_editpage')  # 修改静态页
class EditPageHandler(AdminBaseHandler):
    def get(self, pid):
        p = None
        if pid == '0':
            p = None
        else:
            p = Page.get(Page.id == pid)
        self.render('admin/static_pages/edit_page.html', p=p, active='pages')

    def post(self, pid):
        slug = self.get_argument("pslug", '')
        name = self.get_argument("pname", '')
        content = self.get_argument("pcontent", '')
        metakeywords = self.get_argument("pmetakeywords", '')
        metadescription = self.get_argument("pmetadescription", '')
        metatitle = self.get_argument("pmetatitle", '')
        title = self.get_argument("title", '')
        try:
            if pid == '0':
                p = Page()
            else:
                p = Page.get(Page.id == pid)
            p.updatedtime = int(time.time())
            p.updatedby = self.get_admin_user()
            p.name = name
            p.slug = slug
            p.content = content
            p.metakeywords = metakeywords
            p.metadescription = metadescription
            p.metatitle = metatitle
            p.title = title
            p.validate()
            p.save()
            self.flash("保存成功")
        except Exception, ex:
            self.flash("保存失败，请联系管理员，失败原因：" + ex.message)
        self.render('admin/static_pages/edit_page.html', p=p, active='pages')


@route(r'/admin/delivery/company', name='admin_delivery_company')  # 物流公司管理
class DeliveryCompanyHandler(AdminBaseHandler):
    def get(self):
        subquery = Order.select(db.fn.COUNT(Order.id)).where(Order.status == 3)
        subquery2 = Order.select(db.fn.COUNT(Order.id)).where(Order.status == 4)
        deliverys = Delivery.select(Delivery, subquery.alias('counting'), subquery2.alias('counted')). \
            join(Order, db.JOIN_LEFT_OUTER).group_by(Delivery)
        remaining = (DeliveryNumbers.select(db.fn.COUNT(DeliveryNumbers.id)).where(DeliveryNumbers.status==0)).scalar()
        self.render('admin/delivery.html', deliverys=deliverys, remaining=remaining, active='d_company')


@route(r'/admin/delivery/orders', name='admin_delivery_orders')  # 物流公司代发货管理
class DeliveryOrdersHandler(AdminBaseHandler):
    def get(self):
        d = int(self.get_argument("d", '-1'))
        order_type = int(self.get_argument("order_type", '0'))
        colors = ['style="background-color: #e4b9b9;"', 'style="background-color: #ccc;"']
        dictstyle = {}
        fn = (Order.status == 2)

        fn = fn & (Order.order_type == order_type)
        if d > -1:
            if d == 0:
                fn = fn & (Order.delivery == None)
            else:
                fn = fn & (Order.delivery == d)

        orders = Order.select(Order). \
            join(UserAddr, on=(Order.address == UserAddr.id)).where(fn). \
            order_by(UserAddr.mobile, UserAddr.address, Order.ordered.desc())
        deliverys = Delivery.select()
        g_orders = Order.select(Order). \
            join(UserAddr, on=(Order.address == UserAddr.id)).where((Order.status == 2)). \
            order_by(Order.deliverynum, Order.take_name, Order.take_tel, Order.ordered.desc()).group_by(Order.take_address,Order.take_tel)
        idx = 0
        gidx = 0    #已合并订单数
        for o in orders:
            if o.group_orders.count() > 0:
                groupo = GroupOrder.select().where(GroupOrder.name == o.group_orders[0].name)
                o.ip = o.group_orders[0].name
                if not dictstyle.has_key(o.ip):
                    dictstyle[o.ip] = colors[idx]
                    idx += 1
                    gidx += groupo.count() - 1
                    if idx > len(colors) - 1:
                        idx = 0
            for i in o.items:
                pr = Product_Reserve.select().where(Product_Reserve.product == i.product)
                if pr.count() > 0:
                    o.delivery_time = pr[0].delivery_time
        group_count = g_orders.count() + gidx
        c = orders.count()
        self.render('admin/d_orders.html', orders=orders, deliverys=deliverys, active='d_orders', styles=dictstyle,
                    group_count=group_count, c=c, d=d, order_type=order_type)


@route(r'/admin/blocks', name='admin_blocks')  # 首页展示管理
class BlockHandler(AdminBaseHandler):
    def get(self):
        blocks = PageBlock.select()
        self.render('admin/blocks.html', blocks=blocks, active='blocks')


@route(r'/admin/block/(\d+)', name='admin_block_edit')  # 首页展示管理修改
class BlockHandler(AdminBaseHandler):
    def get(self, bid):
        block = PageBlock.get(id=bid)
        self.render('admin/block_detail.html', block=block, active='blocks')

    def post(self, bid):
        l_c = {}
        content = self.get_argument("content", '')
        block = PageBlock.get(id=bid)
        l_c['standard'] = simplejson.dumps(content)
        block.content = content
        block.updatedtime = int(time.time())
        block.updatedby = self.get_admin_user()
        block.save()
        self.flash('保存成功')
        l_c['operatetype'] = u'修改首页展示'

        AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=l_c)
        self.render('admin/block_detail.html', block=block, active='blocks')


@route(r'/admin/coupon', name='admin_coupon')  # 优惠券管理
class CouponHandler(AdminBaseHandler):
    def get(self):
        type = self.get_argument('type', '1')
        if type == '1':
            cop = [co for co in CouponTotal.select()]
        elif type == '2':
            cop = CouponRealTotal.select().where(CouponRealTotal.status == 0).order_by(CouponRealTotal.createtime.desc())
        self.render('admin/coupon/list.html', cop=cop, active='coupon', type=type)

@route(r'/admin/addcoupon_real/(\d+)', name='add_coupon_real')  # 添加优惠券
class AddCouponRealHandler(AdminBaseHandler):
    def get(self, cid):
        if cid == '0':
            cp = None
        else:
            cp = CouponRealTotal.get(id=cid)
        products = Product.select().where(Product.status == 1).order_by(Product.sku.asc())
        self.render('admin/coupon/add_real.html', cp=cp, active='coupon', products=products)
    def post(self, cid):

        product = self.get_argument("product", "")
        name = self.get_argument("name", "")
        try:
            if cid == '0':
                cp = CouponRealTotal()
            else:
                cp = CouponRealTotal.get(id=cid)
            product = Product.get(id=product.split(';')[0])
            cp.product = product
            cp.product_standard = product.defaultstandard
            cp.name = name
            cp.createby = self.get_admin_user().username
            cp.createtime = int(time.time())
            cp.save()

            content = {}
            content['coupon_real_type'] = '添加实物优惠券'
            content['coupon_total_id'] = cp.id
            AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
            self.flash("保存成功。")
        except Exception, ex:
            logging.error(ex)
            self.flash("保存失败。")
        self.render('admin/coupon/add_real.html', cp=cp, active='coupon')

@route(r'/admin/addcoupon/(\d+)', name='addcoupon')  # 添加优惠券
class AddcouponHandler(AdminBaseHandler):
    def get(self, cid):
        if cid == '0':
            cp = CouponTotal()
        else:
            cp = CouponTotal.get(id=cid)
        now = time.strftime('%Y-%m-%d 00:00:00', time.localtime(time.time()))
        self.render('admin/coupon/add.html', cp=cp, active='coupon', now=now)

    def post(self, cid):
        j_name = self.get_argument('j_name', '')
        j_earn = self.get_argument('j_earn', '')
        j_min = self.get_argument('j_min', '')
        j_satrt = self.get_argument('j_satrt', '')
        j_end = self.get_argument('j_end', '')
        j_total = self.get_argument('j_total', '')
        if cid == '0':
            cp = CouponTotal()
        else:
            cp = CouponTotal.get(id=cid)
        try:
            cp.name = j_name
            cp.price = j_earn
            cp.minprice = j_min
            cp.starttime = int(time.mktime(time.strptime(j_satrt, "%Y-%m-%d %H:%M:%S")))
            cp.endtime = int(time.mktime(time.strptime(j_end, "%Y-%m-%d %H:%M:%S")))
            cp.total = j_total
            cp.createby = self.get_admin_user().username
            cp.createtime = int(time.time())
            cp.save()

            content = {}
            content['coupon_type'] = u'添加优惠券'
            content['coupon_total_id'] = cp.id
            AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
            self.flash("保存成功。")
        except Exception, ex:
            logging.error(ex)
            self.flash("保存失败。")
        self.render('admin/coupon/add.html', cp=cp, active='coupon')


@route(r'/admin/delcoupon/(\d+)', name='del_coupon')  # 禁用优惠券
class DelCouponHandler(AdminBaseHandler):
    def get(self, pid):
        p = CouponTotal.get(CouponTotal.id == pid)
        content = {}
        content['operatetype'] = '禁用优惠券'
        content['pid'] = pid
        content['old_status'] = p.status
        content['current_status'] = 1
        p.status = 1
        p.save()
        AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        cop = [co for co in CouponTotal.select()]
        self.render('admin/coupon/list.html', cop=cop, active='coupon')

@route(r'/admin/delete_coupon/(\d+)', name='delete_coupon')  # 删除优惠券
class DeleteCouponHandler(AdminBaseHandler):
    def get(self, pid):
        p = Coupon.get(Coupon.id == pid)
        content = {}
        content['operatetype'] = '删除用户优惠券'
        content['pid'] = pid
        uid = p.user.id
        content['user_id'] = uid
        p.status = 0
        p.user = None
        p.save()
        AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        self.redirect('/admin/user/' + str(uid))

@route(r'/admin/assign/(\d+)', name='assignshow')  # 显示可用优惠券
class ShowCouponHandler(AdminBaseHandler):
    def get(self, uid):
        ft = (CouponTotal.status == 0) & (Coupon.status == 0) & (Coupon.user >> None)
        cp = Coupon.select(Coupon, CouponTotal).join(CouponTotal, on=(Coupon.coupontotal == CouponTotal.id)).where(ft)
        self.render('admin/coupon/assign.html', cp=cp, uid=uid, active='coupon')

@route(r'/admin/show_coupon/(\d+)', name='show_coupon')  # 显示优惠券类别 新
class ShowCouponTotalHandler(AdminBaseHandler):
    def get(self, uid):
        cp = CouponTotal.select().where(CouponTotal.status==0).order_by(CouponTotal.createtime.desc())
        self.render('admin/coupon/create.html', cp=cp, uid=uid, active='coupon')

@route(r'/admin/create_coupon/(\d+)/(\d+)', name='create_coupon')  # 赠送优惠券 新
class CreateCouponHandler(AdminBaseHandler):
    def get(self, uid, cid):
        user = User.get(id=uid)
        admin_user = self.get_admin_user().username
        log = u'管理员 '+ admin_user + u' 后台赠送'
        result = create_coupon(user, cid, log)
        self.flash(result)
        #self.render('admin/coupon/create.html',uid=uid, active='coupon')
        self.redirect('/admin/user/' + str(uid))

@route(r'/admin/show_coupon_real/(\d+)', name='show_coupon_real')  # 显示实物优惠券类别 新
class ShowCouponTotalRealHandler(AdminBaseHandler):
    def get(self, uid):
        cp = CouponRealTotal.select().where(CouponRealTotal.status==0).order_by(CouponRealTotal.createtime.desc())
        self.render('admin/coupon/show_coupon_real.html', cp=cp, uid=uid, active='coupon')

@route(r'/admin/create_coupon_real/(\d+)/(\d+)', name='create_coupon_real')  # 赠送实物优惠券 新
class CreateCouponRealHandler(AdminBaseHandler):
    def get(self, uid, cid):
        user = User.get(id=uid)
        admin_user = self.get_admin_user().username
        result = create_coupon_real(user, cid, admin_user, 3)   # 3实物券发放，4转盘抽奖，9后台赠品
        self.flash(result)
        self.redirect('/admin/user/' + str(uid))

@route(r'/admin/assign/(\d+)/(\d+)', name='assigncoupon')  # 赠送优惠券
class AssignHandler(AdminBaseHandler):
    def get(self, uid, jid):
        ft = (CouponTotal.status == 0)
        ft = ft & (Coupon.status == 0)
        ft = ft & (Coupon.user == 0)
        cp = Coupon.get(id=jid)
        try:
            if cp.status == 0:
                cp.user = uid
                cp.createby = self.get_admin_user().username
                cp.createtime = int(time.time())
                cp.status = 1
                cp.starttime = int(time.time())
                cp.endtime = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 0:0:0", time.localtime(time.time()+ 86400 * 30)), "%Y-%m-%d 0:0:0")))
                cp.save()

                cp.coupontotal.quantity += 1
                cp.coupontotal.save()

                result = 1
                u = User.get(id = uid)
                content = u'尊敬的客户，恭喜您获得系统赠送优惠券：'+ str(cp.coupontotal.price) + u'元，请在有效期内使用。'
                sms = {'mobile': u.mobile, 'body': content, 'signtype': '1', 'isyzm': ''}
                create_msg(simplejson.dumps(sms), 'sms')
                self.flash("指派成功。")
            else:
                result = 0
                self.flash("指派失败。")
        except Exception, ex:
            logging.error(ex)
            result = 0
            self.flash("指派失败。")
        cp = Coupon.select(Coupon, CouponTotal).join(CouponTotal, on=(Coupon.coupontotal == CouponTotal.id)).where(ft)
        #self.render('admin/coupon/assign.html', cp=cp, uid=uid, active='cp')
        self.redirect('/admin/user/' + str(uid))


@route(r'/admin/library/in', name='admin_library_in')  # 入库管理
class InlibraryHandler(AdminBaseHandler):
    def get(self):
        subquery = Product.select(db.fn.COUNT(Product.id)).where(Product.categoryfront == CategoryFront.id)
        categorys = CategoryFront.select(CategoryFront, subquery.alias('p_count')). \
            join(Product, db.JOIN_LEFT_OUTER).where(db.fn.LENGTH(CategoryFront.code) == 6). \
            group_by(CategoryFront).order_by(CategoryFront.code)
        self.render('admin/library/inlibrary.html', categorys=categorys, active='r_in')


@route(r'/admin/library/inedit', name='admin_library_inedit')  # 入库管理-编辑
class EditInlibraryHandler(AdminBaseHandler):
    def get(self):
        categorys = Invoicing.select().where(Invoicing.status == 0).order_by(Invoicing.id)
        self.render('admin/library/inedit.html', categorys=categorys, active='r_in')


@route(r'/admin/library/out', name='admin_library_out')  # 入库管理
class OutlibraryHandler(AdminBaseHandler):
    def get(self):
        self.render('admin/library/outlibrary.html', active='r_out')


@route(r'/admin/library/(\d+)', name='del_library_in')  # 删除入库管理
class DellibraryHandler(AdminBaseHandler):
    def get(self, cid):
        invoicing = Invoicing.get(Invoicing.id == cid)
        invoicing.status = 1
        invoicing.save()
        categorys = Invoicing.select().where(Invoicing.status == 0).order_by(Invoicing.id)
        self.flash(u"删除成功")
        self.render('admin/library/inedit.html', categorys=categorys, active='r_in')

@route(r'/admin/library/in_list', name='admin_library_inlist')  # 入库管理
class InListHandler(AdminBaseHandler):
    def get(self):
        begindate = self.get_argument("begindate", None)
        enddate = self.get_argument("enddate", None)

        ft = (Invoicing.type == 0) & (Invoicing.status > -2) & (Invoicing.status < 1)
        if begindate and enddate:
            begindate = time.strptime(begindate, "%Y-%m-%d")
            enddate = time.strptime((enddate + " 23:59:59"), "%Y-%m-%d %H:%M:%S")
            ft = ft & (Invoicing.addtime >= time.mktime(begindate)) & (Invoicing.addtime < time.mktime(enddate))
        else:
            begindate = time.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
            ft = ft & (Invoicing.addtime == time.mktime(begindate))

        initems = Invoicing.select().where(ft).order_by(Invoicing.status)

        p = None
        products = Product.select().where(Product.status > 0).order_by(Product.id)    #  & (Product.status == 1)

        self.render('admin/library/in_list.html', initems=initems, p=p, products=products, active='r_in')


@route(r'/admin/library/out_list', name='admin_library_outlist')  # 出库管理
class OutListHandler(AdminBaseHandler):
    def get(self):
        begindate = self.get_argument("begindate", None)
        enddate = self.get_argument("enddate", None)

        ft = (Invoicing.type == 1) & (Invoicing.status == 0)
        if begindate and enddate:
            begindate = time.strptime(begindate, "%Y-%m-%d")
            enddate = time.strptime((enddate + " 23:59:59"), "%Y-%m-%d %H:%M:%S")
            ft = ft & (Invoicing.addtime >= time.mktime(begindate)) & (Invoicing.addtime < time.mktime(enddate))
        else:
            begindate = time.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
            ft = ft & (Invoicing.addtime == time.mktime(begindate))

        initems = Invoicing.select().where(ft)

        self.render('admin/library/out_list.html', initems=initems, active='r_out')


@route(r'/admin/library/add/(\d+)', name='admin_library_add')  # 添加/修改入库信息
class AddLibraryHandler(AdminBaseHandler):
    def get(self, iid):
        if str(iid) == '0':
            p = None
        else:
            p = Invoicing.get(Invoicing.id == iid)
        products = Product.select().where(Product.status > 0).order_by(Product.id)      # & (Product.status == 1)
        self.render('admin/library/in_add.html', p=p, products=products, active='r_in')

    def post(self, iid):
        product = int(self.get_argument("product", '0'))
        quantity = float(self.get_argument("quantity", '0.0'))  #净重
        price = float(self.get_argument("price", '0.0'))
        unitprice = float(self.get_argument("unitprice", '0.0'))
        product_from = self.get_argument("product_from", 'A')
        addtime = self.get_argument("addtime")
        buyer = self.get_argument("buyer", '')
        frombuyer = self.get_argument('frombuyer', None)
        gross_weight = float(self.get_argument("gross_weight", '0.0'))  #毛重
        old_quantity = 0


        pro = Product.get(id = product)
        ps = ProductStandard.get(id=pro.defaultstandard)
        list = simplejson.loads(ps.relations)
        pslist = ProductStandard.select().where(ProductStandard.id << list)

        try:
            if str(iid) == '0':
                i = Invoicing()
                if not frombuyer:
                    i.status = 0
                else:
                    i.status = -1
            else:
                i = Invoicing.get(Invoicing.id == iid)
                if i.status == 0:  # 如果是修改，则记录原始数值
                    old_quantity = i.quantity
                i.status = 0  # 入库成功
                #i.quantity = -i.quantity
                #i.type = 1
                #i.save()

            i.type = 0  #0入库，1出库
            i.product = product
            i.quantity = quantity
            i.price = price
            i.unitprice = unitprice
            i.args = product_from
            i.addtime = int(time.mktime(time.strptime(addtime, "%Y-%m-%d")))
            i.buyer = buyer
            i.gross_weight = gross_weight

            if not frombuyer:  # 管理员直接录入库存
                invo = Invoicing.select(Invoicing.id, Invoicing.unitprice).where((Invoicing.product  == product)&
                                             (Invoicing.type==0)&(Invoicing.status==0)).order_by(Invoicing.id.desc()).limit(1)
                if invo.count() > 0:
                    old_unitprice = invo[0].unitprice
                else:
                    old_unitprice = 0

                i.save()
                for n in pslist:
                    p = Product.get(id=n.product.id)
                    q = p.quantity
                    p.quantity = q + quantity - old_quantity
                    p.save()
                    if old_unitprice != 0:
                        # if unitprice != old_unitprice:
                        try:
                            ic = InvoicingChanged.get(InvoicingChanged.product == n.product.id)
                        except Exception, e:
                            ic = InvoicingChanged()
                        #if ic:
                        ic.product = n.product.id
                        ic.current_invoicing = i.id
                        ic.last_invoicing = invo[0].id
                        ic.last_unitprice = invo[0].unitprice
                        ic.current_unitprice = i.unitprice
                        ic.save()
            self.redirect('/admin/library/in_list')
        except Exception, e:
            self.flash("保存失败，请联系管理员" + e.message)
            self.redirect('/admin/library/add/0')


@route(r'/admin/library/delete/(\d+)', name='admin_library_delete')  # 删除入库信息/退货
class DeleteLibraryHandler(AdminBaseHandler):
    def get(self, iid):
        type = self.get_argument('type', None)

        i = Invoicing.get(Invoicing.id == iid)
        if i.status == -1:  # 退货
            i.status = -2
            i.save()
        elif i.status == 0:
            pro = Product.get(id = i.product.id)
            ps = ProductStandard.get(id=pro.defaultstandard)
            list = simplejson.loads(ps.relations)
            pslist = ProductStandard.select().where(ProductStandard.id << list)
            for n in pslist:
                p = Product.get(id=n.product.id)
                p.quantity -= i.quantity
                p.save()
                #InvoicingChanged.delete().where(InvoicingChanged.product == n.product.id).execute()

            i.quantity = -i.quantity
            i.status = 1
            #i.type = 1
            i.save()
        if type:
            self.redirect('/admin/library/out_list')
        else:
            self.redirect('/admin/library/in_list')


@route(r'/admin/checkwl', name='checkwuliu')  # 检查物流
class CheckWuLiuHandler(BaseHandler):
    def get(self):
        orders = Order.select().where(Order.status == 3).order_by(Order.id.asc())
        result = 0
        error = 0
        for order in orders:
            try:
                s = urllib2.urlopen(
                    "http://www.kuaidi100.com/query?type=zhaijisong&postid=" + str(order.deliverynum)).read()
                if "已签收" in s:
                    result += 1
                    # order.status = 4
                    # order.save()
                    OrderChangeStatus(order.id, 4, 0, self)

                    sign_time = int(time.mktime(time.strptime('2015-02-19', "%Y-%m-%d")))
                    if order.user.signuped < sign_time:
                        start_time = int(time.mktime(time.strptime('2015-03-01', "%Y-%m-%d")))
                        end_time = int(time.mktime(time.strptime('2015-03-08', "%Y-%m-%d")))
                        if (order.ordered > start_time) & (order.ordered < end_time):
                            b = Balance()
                            b.user = order.user
                            b.balance = round(((order.currentprice - order.shippingprice) * 0.1), 2)
                            b.stype = 0
                            b.log = u'老用户返利10%活动，返利金额：'+ order.ordernum
                            b.created = int(time.time())
                            b.save()

            except Exception, e:
                print e.message
                error += 1
        self.write(u"更新成功：" + str(result) + u'；更新失败：' + str(error))

@route(r'/admin/change_order_status', name='admin_change_order_status')  # 定时修改订单状态为正在处理
class ChangeOrderStatusHandler(BaseHandler):
    def get(self):
        msg = []
        two_our = (datetime.datetime.now() - datetime.timedelta(hours = 2)) #自动修改两小时之前的订单
        time_stamp = int(time.mktime(two_our.timetuple()))
        ft = Order.ordered < time_stamp
        orders = Order.select().where((Order.status == 1) & ft)
        ocount = orders.count()
        onum = ''
        msg1 = ''
        for o in orders:
            old_status = o.status
            o.status = 2
            o.lasteditedby = u"系统自动修改"
            o.lasteditedtime = int(time.time())
            o.save()
            onum += o.ordernum + u'，'

            #活动结束
            # if old_status < 2 and o.status == 2:
            #     msg += new_user_order_coupon(o)

        msg.insert(0, u'共有' + str(ocount) + u'个订单自动设置为正在处理。')
        msg.insert(1, u'订单编号为：' + onum)
        msg.insert(2, msg1)
        msg = u'<br/>'.join(msg)
        self.write(msg)

@route(r'/admin/library/inventory', name='admin_library_inventory')  # 库存盘点
class LibraryInventoryHandler(AdminBaseHandler):
    def get(self):
        status = int(self.get_argument('status', '1'))
        sku = self.get_argument('sku', '00')
        fn = Product.status > 0
        if status != 0:
            fn = fn & (Product.status == status)
        skus = '' + sku + '%'
        if sku != '00':
            fn = fn & (Product.sku % skus)
        products = Product.select(Product.updatedtime, Product.name,Product.id,Product.sku,Product.quantity,ProductStandard.weight).join(ProductStandard,on=(Product.defaultstandard==ProductStandard.id)).\
            where(fn).order_by(Product.id).dicts()
        self.render('admin/library/inventory.html', products=products, time=time, active='inventory',status=status,sku=sku)

@route(r'/admin/stores', name='admin_stores')  # 经销商管理
class StoresHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        check_state= int(self.get_argument("check_state", '-1') if self.get_argument("check_state", '-1') else '-1')
        is_recommend= int(self.get_argument("is_recommend", -1) if self.get_argument("is_recommend", '-1') else '-1')
        keyword = self.get_argument("keyword", "")
        ft = (User.grade != 2)
        if check_state>=0:
            ft = ft & (Store.check_state==check_state)
        if is_recommend>=0:
            ft = ft & (Store.is_recommend == is_recommend)
        if keyword:
            keyw = '%' + keyword.replace("'","''") + '%'
            ft = ft & (Store.name % keyw)
        cfs = User.select().join(Store,on=(Store.id==User.store)).where(ft)
#         sql = '''
#        SELECT a.id as user_id,a.isactive,c.`name` as province_name,d.`name` as city_name,e.`name` as district_name,b.* from tb_users a INNER JOIN tb_store b on a.store_id=b.id
# INNER JOIN tb_area c on left(b.area_code,4)=c.`code`
# INNER JOIN tb_area d on left(b.area_code,8)=d.`code`
# INNER JOIN tb_area e on b.area_code=e.`code`
#         '''
#         q = db.handle.execute_sql(sql % ( user.id))
#         items = q.fetchall()

        total = cfs.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize

        cfs = cfs.order_by(Store.id.desc()).paginate(page, pagesize)

        self.render('/admin/store/store.html', cfs=cfs, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='store', check_state=check_state, is_recommend=is_recommend, keyword=keyword)

@route(r'/admin/store_add/(\d+)', name='admin_store_add')  # 添加或修改经销商
class StoreAddHandler(AdminBaseHandler):
    def get(self, store_id):
        areas = Area.select().where((Area.is_delete == 0) & (Area.pid == 0)).order_by(Area.spell_abb, Area.sort)
        default_province=''
        default_city=''
        default_district=''
        if store_id != '0':
            user=None
            store = Store.get(id=store_id)
            users = User.select().where((User.store == store.id))
            if users.count()>0:
                user=users[0]
            if store:
                default_province = store.area_code[0:4]
                default_city = store.area_code[0:8]
                default_district = store.area_code
        else:
            store = None
            user=None

        self.render('admin/store/store_add.html', storenew=store, store_id=store_id,fuser=user, active='store', areas=areas,default_province=default_province,default_city=default_city,default_district=default_district)

    def post(self, storeid):
        username = self.get_argument('username', '')
        password = 'eofan123456'
        name = self.get_argument('name', '')
        province = self.get_argument('ddlProvince', '')
        city = self.get_argument('ddlCity', '')
        region = self.get_argument('ddlCounty', '')
        street = self.get_argument('ddlStreet', '')
        address = self.get_argument('address', '')
        x = self.get_argument('x', 0)
        y = self.get_argument('y', 0)
        storetype = int(self.get_argument('storetype', 0))
        status = int(self.get_argument('status', 0))
        byprice = float(self.get_argument('byprice', 0))
        freight = float(self.get_argument('freight', 0))
        psdistance = float(self.get_argument('psdistance', 0))
        quser = User.select().where((User.username == username) )
        qadminuser = AdminUser.select().where((AdminUser.username == username) )
        content_log={
            "action":"",
            "name":"",
            "province":"",
            "city":"",
            "region":"",
            "street":"",
            "address":"",
            "x":"",
            "y":"",
            "storetype":"",
            "status":"",
            "byprice":"",
            "freight":"",
            "psdistance":""
        }
        if storeid == '0':
            store = Store()
            store.created = int(time.time())
            content_log["action"]="create"
        else:
            store = Store.get(id=storeid)
            content_log["action"]="modify"
        store.name = name
        store.province = province
        store.city = city
        store.region = region
        store.street = street
        store.address = address
        store.x = x
        store.y = y
        store.storetype = storetype
        store.status = status
        store.byprice = byprice
        store.freight = freight
        store.psdistance = psdistance
        content_log["name"]=name
        content_log["province"]=province
        content_log["city"]=city
        content_log["region"]=region
        content_log["street"]=street
        content_log["address"]=address
        content_log["x"]=x
        content_log["y"]=y
        content_log["storetype"]=storetype
        content_log["status"]=status
        content_log["byprice"]=byprice
        content_log["freight"]=freight
        content_log["psdistance"]=psdistance

        adminUser=AdminUser();
        adminUser.username=username
        adminUser.password=AdminUser.create_password(password)
        adminUser.mobile=""
        adminUser.email=""
        adminUser.realname=""
        adminUser.roles="J"
        adminUser.signuped=0
        adminUser.lsignined=0
        adminUser.isactive=1
        if storeid == '0' and quser.count()>0:
            self.flash(u"用户名在前台用户中已经存在！")
            self.render('admin/store/store_add.html', store=store, storeid=storeid,adminUser=adminUser, active='store')
        elif storeid == '0' and qadminuser.count()>0:
            self.flash(u"用户名在后台用户中已经存在！")
            self.render('admin/store/store_add.html', store=store, storeid=storeid,adminUser=adminUser, active='store')
        else:
            store.save()
            AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content_log)
            if storeid == '0' or quser.count()<=0:
                user = User()
                user.username = username
                user.password = User.create_password(password)
                user.mobile=""
                now=int(time.time())
                user.signuped = now
                user.lsignined = now
                user.signupeddate = time.strftime('%Y-%m-%d', time.localtime(now))
                user.signupedtime = time.strftime('%H:%M:%S', time.localtime(now))
                user.phoneactived = 2
                user.isactive = 0
                user.save()
            if storeid == '0' or qadminuser.count()<=0:
                adminUser.store=store.id
                adminUser.front_user=user.id
                adminUser.save()

            self.flash(u"经销商编辑成功")
            self.redirect("/admin/stores")

@route(r'/admin/store_user/(\d+)/(\d+)', name='admin_store_user')  # 经销商用户管理
class StoreUserHandler(AdminBaseHandler):
    def get(self, storeid,adminid):
        try:
            qadminuser =  AdminUser.select().where((AdminUser.store ==storeid) & (AdminUser.front_user >0 ) )
            store=Store.get(Store.id==storeid)
            if int(adminid)>0:
                adminUser=AdminUser.get(AdminUser.id==adminid)
            else:
                adminUser=None
            page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
            pagesize = self.settings['admin_pagesize']

            total = qadminuser.count()
            if total % pagesize > 0:
                totalpage = total / pagesize + 1
            else:
                totalpage = total / pagesize

            ivs = qadminuser.order_by(AdminUser.id.desc()).paginate(page, pagesize)
        except:
            self.write("程序出错了，可能是参数传递错误！")

        self.render('admin/store/store_user.html', ivs=ivs,storenew=store,adminUser=adminUser,total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='store')

    def post(self, storeid,adminid):
        storeid=int(storeid)
        adminid=int(adminid)
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        realname = self.get_argument('realname', '')
        mobile = self.get_argument('mobile', '')
        email = self.get_argument('email', '')
        isactive=self.get_argument('isactive', '')
        hasprice=self.get_argument('hasprice', '')
        if storeid==0:
            self.flash("经销商参数传递错误！")
        else:
            if adminid>0:
                adminUser=AdminUser.get(AdminUser.id==adminid)
                if password:
                    adminUser.password=AdminUser.create_password(password)
            else:
                adminUser=AdminUser();
                adminUser.signuped=int(time.time())
                adminUser.lsignined=0
                adminUser.password=AdminUser.create_password(password)
            qadmin=AdminUser.select().where(AdminUser.store==storeid)
            if qadmin.count()>0:
                adminUser.front_user=qadmin[0].front_user
            adminUser.username=username
            adminUser.mobile=mobile
            adminUser.email=email
            adminUser.realname=realname
            adminUser.store=storeid
            if hasprice:
                adminUser.roles="J+"
            else:
                adminUser.roles="J"
            if isactive:
                adminUser.isactive=1
            else:
                adminUser.isactive=0
            adminUser.save()
            self.flash("提交成功")
        self.redirect('/admin/store_user/' + str(storeid)+"/0")

@route(r'/admin/store/price', name='admin_store_price')  # 库存价格管理
class AdminStoreInventoryHandler(AdminBaseHandler):
    def get(self):
        keyword=self.get_argument("keyword","").strip()
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        fillprice = int(self.get_argument("fillprice", '0') if len(self.get_argument("fillprice", '0')) > 0 else '0')
        pagesize = self.settings['admin_pagesize']
        store_id = int(self.get_argument('store_id','0') if len(self.get_argument("store_id", '0')) > 0 else '0')

        ft = (Product.status >= 1)
        ft = ft & (Product.is_store == 0)
        ft = ft & (Store.storetype ==1 )#self.get_store_user().store
        ftunprice=ft
        ftunprice = ftunprice & (StorePrice.price <= 0)
        if fillprice>0:
            ft = ft & (StorePrice.price <= 0)
        if keyword:
            keyw = '%' + keyword.replace("'","''") + '%'
            ft = ft & (Product.name % keyw)
        if store_id:
            ft = ft & (StorePrice.store == store_id)
            ftunprice = ftunprice & (StorePrice.store == store_id)
        q = StorePrice.select(StorePrice,ProductStandard,Product).join(Product,
                                                                  on=(
                                                                      StorePrice.product == Product.id)).join(ProductStandard,
                                                                  on=(
                                                                      StorePrice.product_standard == ProductStandard.id)).join(Store,
            on=(Store.id==StorePrice.store)).where(ft).order_by(Product.status)
        total = q.count()

        qunprice = StorePrice.select(StorePrice,ProductStandard,Product).join(Product,
                                                                  on=(
                                                                      StorePrice.product == Product.id)).join(ProductStandard,
                                                                  on=(
                                                                      StorePrice.product_standard == ProductStandard.id)).join(Store,
            on=(Store.id==StorePrice.store)).where(ftunprice)
        totalunprice = qunprice.count()

        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        inventorys = q.paginate(page, pagesize)
        stores=Store.select().where(Store.storetype==1).order_by(Store.id)
        self.render('admin/store/price.html', inventorys=inventorys, total=total, page=page, pagesize=pagesize,
        totalpage=totalpage,  active='store_price',fillprice=fillprice,keyword=keyword,totalunprice=totalunprice,store_id=store_id,stores=stores)

@route(r'/admin/mobile/ads', name='admin_mobile_ads')  # 手机端广告管理
class MobileADSHandler(AdminBaseHandler):
    def get(self):
        ads = Ad.select().where(Ad.atype == 3)
        self.render('admin/mobile/ads.html', ads=ads, active='m_ads')

@route(r'/admin/mobile/blocks', name='admin_mobile_blocks')  # 手机端展示设计
class MobileBlocksHandler(AdminBaseHandler):
    def get(self):
        blocks = MobileBlock.select()
        self.render('/admin/mobile/blocks.html', blocks=blocks, active='m_blocks')

@route(r'/admin/mobile/block/(\d+)', name='admin_mobile_block_edit')  # 手机端首页展示管理修改
class MobileBlockHandler(AdminBaseHandler):
    def get(self, bid):
        block = MobileBlock.get(id=bid)
        self.render('admin/mobile/block_detail.html', block=block, active='m_blocks')

    def post(self, bid):
        l_c = {}
        content = self.get_argument("content", '')
        block = MobileBlock.get(id=bid)
        l_c['standard'] = simplejson.dumps(content)
        block.content = content
        block.updatedtime = int(time.time())
        block.updatedby = self.get_admin_user()
        block.save()
        self.flash('保存成功')
        l_c['operatetype'] = '修改手机端首页展示'

        AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=l_c)
        self.render('admin/mobile/block_detail.html', block=block, active='m_blocks')

@route(r'/admin/order_replace/(\d+)', name='admin_order_replace')  # 补单
class OrderReplaceHandler(AdminBaseHandler):
    def get(self, oid):
        o = Order.get(id=oid)
        products = Product.select().where(Product.status == 1).order_by(Product.sku.desc())
        self.render('admin/order/order_replace.html', o=o, products=products, active='orders', userid=o.user.id)

    def post(self, oid):
        pid = self.get_arguments('hidpid', [0])
        carts = json.loads(pid[0])
        message = self.get_argument('message', '')
        totalPrice = self.get_argument('orderPrice', 0)
        take_name = self.get_argument('take_name', '')
        take_address = self.get_argument('take_address', '')
        take_tel = self.get_argument('take_tel', '')
        old = Order.get(id=oid)
        order = Order()

        order.user = old.user
        order.address = old.address
        order.distributiontime = old.distributiontime
        order.message = message
        order.isinvoice = old.isinvoice
        order.invoicesub = old.invoicesub
        order.invoicename = old.invoicename
        order.invoicecontent = old.invoicecontent
        order.shippingprice = 0
        order.price = totalPrice
        order.currentprice = totalPrice
        order.ordered = int(time.time())
        order.ip = self.request.remote_ip
        order.status = 1
        order.payment = 9
        order.take_name = take_name
        order.take_tel = take_tel
        order.take_address = take_address
        order.lasteditedby = self.get_admin_user().username
        order.lasteditedtime = int(time.time())
        order.ordereddate = time.strftime('%Y-%m-%d', time.localtime(order.ordered))    #下单日期，文本格式
        order.orderedtime = time.strftime('%H:%M:%S', time.localtime(order.ordered))    #下单时间，文本格式
        order.save()
        order.ordernum = 'U' + str(old.user.id) + '-S' + str(order.id)
        order.save()
        order_weight = 0.0
        for c in carts:
            product = Product.get(id=c["pid"])
            orderItem = OrderItem()
            orderItem.product = product.id
            orderItem.order = order.id
            orderItem.product_standard = product.defaultstandard
            ps = ProductStandard.get(id=product.defaultstandard)
            orderItem.price = ps.price
            orderItem.quantity = c["quantity"]
            orderItem.weight = ps.weight
            orderItem.product_standard_name = ps.name
            orderItem.save()
            order_weight += round((ps.weight / 500 * float(c["quantity"])), 2)
        order.weight = order_weight
        if (order_weight > int(order_weight)):
            order.freight = 5 + int(order_weight - 1.0) * 0.5  # 5是首重运费，order_weight单位是斤，超过一公斤每斤加五毛，不足一斤算一斤
        else:
            order.freight = 5 + (order_weight - 2) * 0.5
        order.save()
        self.flash("补发成功")
        AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()))
        self.redirect('/admin/user/' + str(order.user.id))


@route(r'/admin/order_update/(\d+)', name='admin_order_update')  # 修改订单
class OrderUpdateHandler(AdminBaseHandler):
    def get(self, oid):
        o = Order.get(id=oid)
        products = Product.select().where(Product.status == 1).order_by(Product.sku.desc())
        self.render('admin/order/order_update.html', o=o, products=products, active='orders',userid=o.user.id)

    def post(self, oid):
        message = self.get_argument('message', '')
        take_name = self.get_argument('take_name', '')
        take_address = self.get_argument('take_address', '')
        take_tel = self.get_argument('take_tel', '')

        order = Order.get(id=oid)
        order.take_name = take_name
        order.take_tel = take_tel
        order.take_address = take_address
        order.lasteditedby = self.get_admin_user().username
        order.lasteditedtime = int(time.time())
        order.message = message
        order.save()
        self.redirect('/admin/user/' + str(order.user.id))


@route(r'/admin/library/loss/(\d+)', name='admin_library_loss')  # 损耗情况
class LossHandler(AdminBaseHandler):
    def get(self, pid):
        inventory = Inventory.select().where(Inventory.product == pid).order_by(Inventory.updatedtime.desc())
        self.render('admin/library/loss_list.html', inventory=inventory, active='inventory')


@route(r'/admin/comment', name='admin_comment')  # 商品评价管理
class CommentHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", None)
        begin_date = self.get_argument("begindate", '')
        end_date = self.get_argument("enddate", '')
        uid = self.get_argument("uid",None)
        pid = self.get_argument("pid", None)
        status = int(self.get_argument("status", -1))
        ft = (Comment.id > 0)

        if begin_date and end_date:
            begindate = time.strptime(begin_date, "%Y-%m-%d")
            enddate = time.strptime((end_date + " 23:59:59"), "%Y-%m-%d %H:%M:%S")
            ft = ft & (Comment.created >= time.mktime(begindate)) & (Comment.created < time.mktime(enddate))
        if keyword:
            keyword = '%' + keyword + '%'
            ft = ft & (Comment.comment % keyword)
        if status > -1:
            ft = ft & (Comment.status == status)
        if uid:
            ft = ft & (Comment.user == uid)
        if pid:
            ft = ft & (Comment.product == pid)
        uq = Comment.select().where(ft)
        total = uq.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize

        cs = uq.order_by(Comment.created.desc()).paginate(page, pagesize)

        self.render('/admin/consult/comment.html', cs=cs, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='comment', uid=uid,pid=pid, status=status, begindate=begin_date, enddate=end_date)


@route(r'/admin/commentcheck/(\d+)', name='admin_comment_check')  # 商品评价审核
class CommentCheckHandler(AdminBaseHandler):
    def get(self, cid):
        status = int(self.get_argument("status", 1))
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        uid = self.get_argument("uid",None)
        pid = self.get_argument("pid", None)
        begin_date = self.get_argument("begindate", '')
        end_date = self.get_argument("enddate", '')

        admin_user = self.get_admin_user()
        comment = Comment.get(id=cid)
        comment.status = status
        comment.approvedtime = int(time.time())
        comment.approvedby = admin_user.id
        comment.save()
        self.redirect('/admin/comment?page='+ str(page) + '&uid='+ str(uid) +'&pid='+ str(pid) + '&begindate='+begin_date +
        '&enddate=' + end_date)

@route(r'/admin/tel_order', name='admin_tel_order')  # 电话下单
class TelOrderHandler(AdminBaseHandler):
    def get(self):
        type = self.get_argument('type', '0')
        active = 'tel_order'
        if type == '1':
            products1 = ProductStandard.select(ProductStandard, Product).join(Product). \
                where((Product.status == 1) & (Product.sku % '01%') & (Product.is_index == 1))
            products2 = ProductStandard.select(ProductStandard, Product).join(Product). \
                where((Product.status == 1) & (Product.sku % '02%') & (Product.is_index == 1))
            active = 'tel_order_event'
        else:
            products1 = ProductStandard.select(ProductStandard, Product).join(Product). \
                where((Product.status == 1) & (Product.sku % '01%'))
            products2 = ProductStandard.select(ProductStandard, Product).join(Product). \
                where((Product.status == 1) & (Product.sku % '02%'))
            active = 'tel_order'

        # products = Product.select().where(Product.status == 1).order_by(Product.sku.desc())
        self.render('/admin/order/tel_order.html', products1=products1, products2=products2, active=active)

    def post(self):
        pid = self.get_arguments('hidpid', [0])
        carts = json.loads(pid[0])
        message = self.get_argument('message', '')
        totalPrice = self.get_argument('orderPrice', 0)
        take_name = self.get_argument('take_name', '')
        take_address = self.get_argument('take_address', '')
        take_tel = self.get_argument('take_tel', '')
        distributiontime = self.get_argument('distributiontime', '工作日/周末/假日均可')
        user_name = self.get_argument('user_name', '')
        user_id = self.get_argument('user_id', '')
        province = self.get_argument('ddlProvince', '陕西')
        city = self.get_argument('ddlCity', '西安')
        region = self.get_argument('ddlCounty', '')
        street = self.get_argument('ddlStreet', '')
        currentPrice = self.get_argument('txtOrderPrice', 0)
        shippingprice = self.get_argument('hidShippingprice', 0)

        if user_id:
            user = User.get(id=int(user_id))
        else:
            user = User()
            user.username = user_name
            user.mobile = user_name
            user.password = User.create_password('123456')
            now = int(time.time())
            signupeddate = time.strftime('%Y-%m-%d', time.localtime(now))
            signupedtime = time.strftime('%H:%M:%S', time.localtime(now))
            user = User.create(username=user.username, password=user.password, mobile=user.mobile,
                               signuped=now, lsignined=now, phoneactived=0,
                               signupeddate=signupeddate, signupedtime=signupedtime)
        address_id = self.get_argument('hidAddressID', '')
        userAddr = UserAddr()
        userAddr.user = user.id
        userAddr.address = take_address
        userAddr.mobile = take_tel
        userAddr.province = province
        userAddr.city = city
        userAddr.region = region
        userAddr.street = street
        userAddr.name = take_name
        userAddr.isdefault = 1
        if (address_id != ''):
            userAddr.id = address_id
        listUserAddrs = UserAddr.select().where((UserAddr.user == user.id) & (UserAddr.isdefault == 1))
        for listUserAddr in listUserAddrs:
            listUserAddr.isdefault = 0
            listUserAddr.save()
        userAddr.save()

        order = Order()

        order.user = user.id
        order.address = userAddr.id
        order.distributiontime = distributiontime
        order.message = message
        # order.isinvoice = old.isinvoice
        #order.invoicesub = old.invoicesub
        #order.invoicename = old.invoicename
        #order.invoicecontent = old.invoicecontent
        order.shippingprice = shippingprice
        order.price = totalPrice
        order.currentprice = currentPrice
        order.ordered = int(time.time())
        order.ip = self.request.remote_ip
        order.status = 1    #3月16日修改 后台下单不要直接转为“正在处理”
        order.payment = 0  #支付方式  0货到付款
        order.take_name = take_name
        order.take_tel = take_tel
        order.take_address = city + ' ' + region + ' ' + street + ' ' + take_address
        order.lasteditedby = self.get_admin_user().username
        order.lasteditedtime = int(time.time())
        order.ordereddate = time.strftime('%Y-%m-%d', time.localtime(order.ordered))    #下单日期，文本格式
        order.orderedtime = time.strftime('%H:%M:%S', time.localtime(order.ordered))    #下单时间，文本格式
        order.order_from = 3    #后台下单
        order.save()
        order.ordernum = 'U' + str(user.id) + '-S' + str(order.id)
        order.save()
        order_weight = 0.0
        for c in carts:
            product = Product.get(id=c["pid"])
            orderItem = OrderItem()
            orderItem.product = product.id
            orderItem.order = order.id
            orderItem.product_standard = product.defaultstandard
            ps = ProductStandard.get(id=product.defaultstandard)
            orderItem.price = ps.price
            orderItem.quantity = c["quantity"]
            orderItem.weight = ps.weight
            orderItem.product_standard_name = ps.name
            orderItem.save()


            product = Product.get(id = product.id)
            product.orders = product.orders + 1
            product.save()
            #根据仓库 张宏伟要求，取消下单时扣除库存和用户取消订单返回库存功能 2015-03-24修改
            '''i = Invoicing()
            i.type = 1 #0入库，1出库
            i.product = product.id
            i.quantity = round((ps.weight / 500 * float(c["quantity"])), 2)
            i.price = round((ps.price * float(c["quantity"])), 2)
            i.unitprice =ps.price
            i.args = order.ordernum
            i.addtime = int(time.mktime(time.strptime(time.strftime('%Y-%m-%d',time.localtime(time.time())),"%Y-%m-%d")))
            i.save()

            pro = Product.get(id = product.id)
            ps = ProductStandard.get(id=pro.defaultstandard)
            list = simplejson.loads(ps.relations)
            pslist = ProductStandard.select().where(ProductStandard.id << list)
            for n in pslist:
                p = Product.get(id=n.product.id)
                p.quantity -= round((ps.weight / 500 * float(c["quantity"])), 2)
                p.save()
                #对于低于库存警戒线时报警
                if p.quantity < 5:
                    body = p.name + u' 当前理论库存数量为' + str(p.quantity) + u'斤，请关注库存情况。'
                    ausers = AdminUser.select().where((AdminUser.mobile != '') & (AdminUser.isactive == 1) & (AdminUser.roles % '%B%'))
                    sms = {'apptype': 2, 'body': body, 'receiver': []}
                    for au in ausers:
                        sms['receiver'].append(au.mobile)'''


            order_weight += round((ps.weight / 500 * float(c["quantity"])), 2)
        order.weight = order_weight
        if (order_weight > int(order_weight)):
            order.freight = 5 + int(order_weight - 1.0) * 0.5  #5是首重运费，order_weight单位是斤，超过一公斤每斤加五毛，不足一斤算一斤
        else:
            order.freight = 5 + (order_weight - 2) * 0.5
        order.save()

        msg = ''
        #活动结束
        # msg = new_user_order_coupon(order)
        self.flash(
            u"电话下单成功！ 订单编号：" + order.ordernum + u"； 收件人：" + order.take_name + u"； 联系电话：" + order.take_tel + u"； 收货地址：" + order.take_address + u"； 订单金额：" + str(
                order.currentprice) + u"；" + msg)
        AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()))
        self.redirect('/admin/tel_order')


@route(r'/admin/attribute', name='admin_attribute')  # 商品属性
class AttributeHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        attr = int(self.get_argument("attr", 1))
        ft = (ProductAttribute.id > 0)

        ft = ft & (ProductAttribute.attribute == attr)
        uq = ProductAttribute.select().where(ft)
        total = uq.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize

        cs = uq.order_by(ProductAttribute.created.desc(), ProductAttribute.sort.asc()).paginate(page, pagesize)

        self.render('/admin/product/attribute.html', cs=cs, total=total, attr=attr, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='attribute')


@route(r'/admin/set_attribute', name='admin_set_attribute')  # 商品属性
class SetAttributeHandler(AdminBaseHandler):
    def get(self):
        attributes = Attribute.select().where((Attribute.type == 1) & (Attribute.isactive == 1))
        products = ProductStandard.select(ProductStandard, Product).join(Product).where(Product.status == 1)
        attr = int(self.get_argument("attr", 1))
        self.render('/admin/product/set_attribute.html', products=products, attributes=attributes, attr=attr,
                    active='attribute')

    def post(self):
        pid = self.get_arguments('product_id', [0])
        attr = int(self.get_argument('attr', 0))
        if pid:
            products = Product.select().where(Product.id << pid)
            for p in products:
                pa = ProductAttribute()
                pa.product = p.id
                pa.attribute = attr
                pa.created = int(time.time())
                # pa.sort =
                try:
                    checkpa = ProductAttribute.get(
                        (ProductAttribute.product == p.id) & (ProductAttribute.attribute == attr))
                except Exception, ex:
                    checkpa = None
                if checkpa:
                    pass
                else:
                    pa.save()
        self.redirect('/admin/attribute?attr=' + str(attr))


@route(r'/admin/attr_delete/(\d+)', name='admin_attr_delete')
class AttrDeleteHandler(AdminBaseHandler):
    def get(self, aid):
        attr = int(self.get_argument('attr', 0))
        ProductAttribute.delete().where(ProductAttribute.id == aid).execute()
        # self.flash(u"删除成功")
        self.redirect('/admin/attribute?attr=' + str(attr))


@route(r'/admin/attr_modify/(\d+)', name='admin_attr_modify')
class AttrModifyHandler(AdminBaseHandler):
    def get(self, aid):
        attributes = Attribute.select().where((Attribute.type == 1) & (Attribute.isactive == 1))
        pa = ProductAttribute.get(id=aid)
        attr = int(self.get_argument('attr', 0))
        self.render('/admin/product/modify_attribute.html', pa=pa, attributes=attributes, attr=attr, active='attribute')

    def post(self, aid):
        attr = int(self.get_argument('attribute', 0))
        sort = int(self.get_argument('sort', 0))
        pa = ProductAttribute.get(id=aid)
        if pa:
            pa.attribute = attr
            pa.sort = sort
            pa.id = aid
            pa.save()
        self.redirect('/admin/attribute?attr=' + str(attr))

@route(r'/admin/sms_send', name='admin_sms_send')  # 短信群发
class OrderUpdateHandler(AdminBaseHandler):
    def get(self):
        self.render('admin/SMS_send.html', active='sms_send')

    def post(self):
        content_log = {}
        number = self.get_argument('number', '')
        content = self.get_argument('content', '')
        title = self.get_argument('title', '')
        is_users = self.get_argument('is_users', '')
        user_type = int(self.get_argument('user_type',-1))
        sms_type = int(self.get_argument('sms_type',-1))
        if sms_type == 0:
            if is_users:
                if is_users == 'all_user':
                    content_log['content'] = u'为用户 所有用户 推送极光消息，消息内容：' + content
                    create_msg(simplejson.dumps({'body': content}), 'all_jpush')
                    self.flash("推送成功")
                elif is_users == 'user':
                    if number:
                        content_log['content'] = u'为用户 ' + number + u' 推送极光消息，消息内容：' + content
                        num = number.split(',')
                        for n in num:
                            sms = {'apptype': 1, 'body': content, 'receiver': [n]}
                            create_msg(simplejson.dumps(sms), 'jpush')
                        self.flash("推送成功")
                    else:
                        self.flash("请输入电话号码！")
                elif is_users == 'group_user':
                    if user_type > -1:
                        content_log['content'] = u'为用户组 ' + str(user_type) + u' 推送极光消息，消息内容：' + content
                        create_msg(simplejson.dumps({'body': content, 'grade': user_type}), 'group_jpush')
                        self.flash("推送成功")
                        # users = User.select(User.mobile).where((User.grade == user_type) & (User.isactive == 1)).dicts()
                        # for u in users:
                        #     if len(u['mobile']) == 11:
                        #         sms = {'apptype': 1, 'body': content, 'receiver': [u['mobile']]}
                        #         create_msg(simplejson.dumps(sms), 'jpush')
                    else:
                        self.flash("请选择分组")
        elif sms_type == 1:
            if is_users:
                if is_users == 'all_user':
                    content_log['content'] = u'为所有用户发送消息，消息内容：' + content

                    users = User.select(User.mobile).where(User.isactive == 1).dicts()
                    mobiles = ''
                    for u in users:
                        #获取所有用户手机号码并于英文逗号隔开
                        if len(u['mobile']) == 11:
                            mobiles += u['mobile'] + ','
                    j = 0
                    #每次发送号码不能大于600个 7200字符
                    while j < (users.count() + 599) / 600:
                        if len(mobiles) > 7200:
                            cells = mobiles[0:7200]
                        else:
                            cells = mobiles
                        sms = {'mobile': cells, 'body': content, 'signtype': '1', 'isyzm': ''}
                        create_msg(simplejson.dumps(sms), 'sms')
                        #删除已发送的手机号码
                        mobiles = mobiles[(j+1)*7200:]
                        j += 1
                    # create_msg(simplejson.dumps({'body': content}), 'all_sms')
                    self.flash("发送成功")
                elif is_users == 'user':
                    if number:
                        content_log['content'] = u'为用户 ' + str(number) + u' 发送短信，消息内容：' + content
                        # num = number.split(',')
                        sms = {'mobile': number, 'body': content, 'signtype': '1', 'isyzm': ''}
                        create_msg(simplejson.dumps(sms), 'sms')
                        self.flash("发送成功")
                    else:
                        self.flash("请输入电话号码！")
                elif is_users == 'group_user':
                    if user_type > -1:
                        content_log['content'] = u'为用户组 ' + str(user_type) + u' 群发送短信，短信内容：' + content

                        users = User.select(User.mobile).where((User.grade == user_type) & (User.isactive == 1)).dicts()
                        mobiles = ''
                        for u in users:
                            #获取所有用户手机号码并于英文逗号隔开
                            if len(u['mobile']) == 11:
                                mobiles += u['mobile'] + ','
                        j = 0
                        #每次发送号码不能大于600个 7200字符
                        while j < (users.count() + 599) / 600:
                            if len(mobiles) > 7200:
                                cells = mobiles[0:7200]
                            else:
                                cells = mobiles
                            sms = {'mobile': cells, 'body': content, 'signtype': '1', 'isyzm': ''}
                            create_msg(simplejson.dumps(sms), 'sms')
                            #删除已发送的手机号码
                            mobiles = mobiles[(j+1)*7200:]
                            j += 1


                        # create_msg(simplejson.dumps({'body': content, 'grade': user_type}), 'group_sms')
                        self.flash("发送成功")
                    else:
                        self.flash("请选择分组")
        elif sms_type == 2:
            if is_users and title:
                if is_users == 'all_user':
                    content_log['content'] = u'为所有用户发送站内消息，消息内容：' + content

                    users = User.select().where(User.isactive == 1)
                    mobiles = ''
                    for u in users:
                        UserMessage.create(user=u, username=u.username, type=0, is_send=0, title=title,
                             content=content, has_read=0, send_time=int(time.time()))
                    self.flash("发送成功")
                elif is_users == 'user':
                    if number:
                        content_log['content'] = u'为用户 ' + str(number) + u' 发送站内消息，消息内容：' + content
                        numbers=number.split(',')
                        users = User.select().where((User.username << numbers) & (User.isactive == 1))
                        for u in users:
                            UserMessage.create(user=u, username=u.username, type=0, is_send=0, title=title,
                                 content=content, has_read=0, send_time=int(time.time()))
                        self.flash("发送成功")
                    else:
                        self.flash("请输入电话号码！")
                elif is_users == 'group_user':
                    if user_type > -1:
                        content_log['content'] = u'为用户组 ' + str(user_type) + u' 群发送站内消息，短信内容：' + content

                        users = User.select().where((User.grade == user_type) & (User.isactive == 1))
                        for u in users:
                            UserMessage.create(user=u, username=u.username, type=0, is_send=0, title=title,
                                 content=content, has_read=0, send_time=int(time.time()))
                        self.flash("发送成功")
                    else:
                        self.flash("请选择分组")
                AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content_log)

        self.render('admin/SMS_send.html', active='sms_send')


@route(r'/admin/user/balance/history/(\d+)', name='admin_user_balance_history')  # 查看用户余额历史
class UserBalanceHistoryHandler(AdminBaseHandler):
    def get(self, userid):
        page = int(self.get_argument("page", 1))
        pagesize = self.settings['admin_pagesize']
        q = Balance.select().where((Balance.user==userid) & (Balance.isactive==1))

        total = q.count()


        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        b = q.order_by(Balance.created.desc()).paginate(page, pagesize)

        self.render('/admin/user/user_balance_history.html', balance=b, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, userid=userid)

@route(r'/admin/user/score/history/(\d+)', name='admin_user_score_history')  # 查看用户余额历史
class UserBalanceHistoryHandler(AdminBaseHandler):
    def get(self, userid):
        page = int(self.get_argument("page", 1))
        pagesize = self.settings['admin_pagesize']
        q = Score.select().where((Score.user==userid) )
        # Score.select().where(Score.user == userNew.id)

        total = q.count()


        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        b = q.order_by(Score.id.desc()).paginate(page, pagesize)

        self.render('/admin/user/user_score_history.html', score=b, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, userid=userid)

@route(r'/admin/del_orderitem/(\d+)', name='admin_del_orderitem')  # 删除订单项
class DeleteOrderItemHandler(AdminBaseHandler):
    def get(self, iid):
        oid = int(self.get_argument('oid', 0))
        free_ship = float(setting.FreeshippingFee)
        ship_free = float(setting.ShippingFee)
        if oid != 0:
            item = OrderItem.get(id=iid)
            o = Order.get(id=oid)
            o.price -= item.price * item.quantity
            o.currentprice -= item.price * item.quantity
            o.weight -= round((item.product_standard.weight / 500 * item.quantity), 2)
            if (o.weight > int(o.weight)):
                o.freight = 5 + int(o.weight - 1.0) * 0.5  #5是首重运费，order_weight单位是斤，超过一公斤每斤加五毛，不足一斤算一斤
            else:
                o.freight = 5 + (o.weight - 2) * 0.5
            if o.shippingprice != ship_free:
                if free_ship > (o.currentprice - o.shippingprice):
                    o.currentprice += ship_free
                    o.shippingprice = ship_free
            OrderItem.delete().where(OrderItem.id == iid).execute()
            o.save()
            self.redirect('/admin/order_update/' + str(oid))

@route(r'/admin/gifts', name='admin_gifts')  # 赠品/补发品信息
class GiftHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        key = self.get_argument("keyword", None)
        group = int(self.get_argument("group", -1))
        ft = (Gift.id > 0)

        if key:
            keyword = '%' + key + '%'
            ft = ft & (User.username % keyword)
        if group > -1:
            ft = ft & (Gift.status == group)
        uq = Gift.select(Gift).join(User,on=(Gift.user==User.id)).where(ft)
        total = uq.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize

        gifts = uq.order_by(Gift.created.desc()).paginate(page, pagesize)

        self.render('/admin/order/gifts.html', gifts=gifts, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='gifts', keyword=key)

@route(r'/admin/add_gift/(\d+)', name='admin_add_gift')  # 赠品下发
class AddGiftHandler(AdminBaseHandler):
    def get(self, uid):
        u = User.get(id=uid)
        products = Product.select().where(Product.status == 1).order_by(Product.sku.desc())
        self.render('admin/order/add_gift.html', u=u, products=products, active='users')

    def post(self, uid):
        pid = self.get_arguments('hidpid', [0])
        carts = json.loads(pid[0])
        message = self.get_argument('message', '')
        admin_user = self.get_admin_user()

        for c in carts:
            product = Product.get(id=c["pid"])
            gift = Gift()
            gift.user = uid
            gift.product = product.id
            gift.product_standard = product.defaultstandard
            gift.quantity = c["quantity"]
            gift.created = int(time.time())
            gift.created_by = admin_user.id
            gift.status = 0
            gift.type = 9   # 9表示后台赠送 对应orderItem表中的item_type
            gift.end_time = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 0:0:0", time.localtime(time.time()+ 86400 * 30)), "%Y-%m-%d 0:0:0")))
            gift.save()
        self.flash("提交成功")
        self.redirect('/admin/user/' + str(uid))

@route(r'/admin/user_interview/(\d+)', name='admin_user_interview')  # 访谈记录
class UserInterviewHandler(AdminBaseHandler):
    def get(self, uid):
        u = User.get(id=uid)

        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']

        ft = (UserInterview.status ==1)&(UserInterview.user==uid)

        uq = UserInterview.select(UserInterview).join(AdminUser,on=(UserInterview.admin==AdminUser.id)).where(ft)
        total = uq.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize

        ivs = uq.order_by(UserInterview.viewtime.desc()).paginate(page, pagesize)

        self.render('admin/user/user_interview.html', u=u, ivs=ivs,total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='users')
    ##过滤HTML中的标签
    #将HTML中标签等信息去掉
    #@param htmlstr HTML字符串.
    def filter_tags(self,htmlstr):
        #先过滤CDATA
        re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
        re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
        re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
        re_br=re.compile('<br\s*?/?>')#处理换行
        re_h=re.compile('</?\w+[^>]*>')#HTML标签
        re_comment=re.compile('<!--[^>]*-->')#HTML注释
        s=re_cdata.sub('',htmlstr)#去掉CDATA
        s=re_script.sub('',s) #去掉SCRIPT
        s=re_style.sub('',s)#去掉style
        s=re_br.sub('\n',s)#将br转换为换行
        s=re_h.sub('',s) #去掉HTML 标签
        s=re_comment.sub('',s)#去掉HTML注释
        #去掉多余的空行
        blank_line=re.compile('\n+')
        s=blank_line.sub('\n',s)
        s=self.replaceCharEntity(s)#替换实体
        return s
    ##替换常用HTML字符实体.
    #使用正常的字符替换HTML中特殊的字符实体.
    #你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
    #@param htmlstr HTML字符串.
    def replaceCharEntity(self,htmlstr):
        CHAR_ENTITIES={'nbsp':' ','160':' ',
                    'lt':'<','60':'<',
                    'gt':'>','62':'>',
                    'amp':'&','38':'&',
                    'quot':'"','34':'"',}

        re_charEntity=re.compile(r'&#?(?P<name>\w+);')
        sz=re_charEntity.search(htmlstr)
        while sz:
            entity=sz.group()#entity全称，如&gt;
            key=sz.group('name')#去除&;后entity,如&gt;为gt
            try:
                htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
                sz=re_charEntity.search(htmlstr)
            except KeyError:
                #以空串代替
                htmlstr=re_charEntity.sub('',htmlstr,1)
                sz=re_charEntity.search(htmlstr)
        return htmlstr
    def post(self, uid):
        title = self.get_argument('title', '')
        content = self.get_argument('content', '')
        title=self.filter_tags(title)
        content=self.filter_tags(content)
        content=content.replace('\r\n','<br>')
        admin_user = self.get_admin_user()
        ui = UserInterview()
        ui.admin = admin_user.id
        ui.user = uid
        ui.title = title
        ui.content =content
        ui.viewtime = int(time.time())
        ui.status = 1
        ui.save()
        self.flash("提交成功")
        self.redirect('/admin/user/user_interview/' + str(uid))
@route(r'/admin/interview', name='admin_interview')  # 访谈记录
class UserInterviewHandler(AdminBaseHandler):
    def get(self):
        keyword = self.get_argument("keyword", None)
        ft = (UserInterview.status ==1)

        if keyword:
            keyword = '%' + keyword + '%'
            ft = ft & (AdminUser.username % keyword)

        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        uq = UserInterview.select(UserInterview).join(AdminUser,on=(UserInterview.admin==AdminUser.id)).where(ft)
        total = uq.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize

        ivs = uq.order_by(UserInterview.viewtime.desc()).paginate(page, pagesize)

        self.render('admin/user/interview.html', ivs=ivs,total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='interview',keyword=keyword)

@route(r'/admin/add_topic/(\d+)', name='admin_add_topic')  # 添加话题
class AddTopicHandler(AdminBaseHandler):
    def get(self, cid):
        onum = self.get_argument("order", None)
        title = ''
        if onum:
            title = u'订单编号：'+onum
        if cid != '0':
            t = Topic.get(Topic.id == cid)
        else:
            t = None
        users = AdminUser.select()
        self.render('/admin/topic/add_topic.html', t=t, users=users, active='topic',title=title)
    def post(self, cid):
        admin_user = self.get_admin_user()
        title = self.get_argument('title', '')
        content = self.get_argument('content', '')
        executor = int(self.get_argument('executor',0))
        if cid == '0':
            t = Topic()
        else:
            t = Topic.get(Topic.id == cid)
        t.title = title
        t.content = content
        t.created = int(time.time())
        t.created_by = admin_user.id
        if executor:
            t.executor = executor
        t.status = 0
        t.save()
        body =  admin_user.username + u'：' + content
        ausers = AdminUser.select().where((AdminUser.mobile != '') & (AdminUser.isactive == 1))
        sms = {'apptype': 4, 'body': body, 'receiver': []}
        for au in ausers:
            sms['receiver'].append(au.mobile)
        create_msg(simplejson.dumps(sms), 'jpush')
        #self.flash("添加成功")
        self.redirect('/admin/topic')
@route(r'/admin/topic', name='admin_topic')  # 话题列表
class TopicHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        status = int(self.get_argument('status', -1))
        if status != -1:
            top = Topic.select().where(Topic.status == status)
        else:
            top = Topic.select().where(Topic.status != -1)
        total = top.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        t = top.order_by(Topic.created.desc()).paginate(page, pagesize)
        self.render('/admin/topic/topic.html', topic=t, active='topic', total=total, page=page,
                    pagesize=pagesize, totalpage=totalpage,status=status)

@route(r'/admin/discuss/(\d+)', name='admin_discuss')  # 话题详细
class DiscussHandler(AdminBaseHandler):
    def get(self, tid):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        if tid != '0':
            t = Topic.get(Topic.id == tid)
            dis = Topic_Discuss.select().where(Topic_Discuss.topic == tid)
            total = dis.count()
            if total % pagesize > 0:
                totalpage = total / pagesize + 1
            else:
                totalpage = total / pagesize
            discuss = dis.order_by(Topic_Discuss.created.desc()).paginate(page, pagesize)
        else:
            t = None
        self.render('/admin/topic/discuss.html', t=t,discuss=discuss, active='topic', total=total, page=page,
                    pagesize=pagesize, totalpage=totalpage)
    def post(self, tid):
        admin_user = self.get_admin_user()
        content = self.get_argument('content', '')
        t = Topic.get(id = tid)
        discuss = Topic_Discuss()
        discuss.content = content
        discuss.topic = tid
        discuss.created = int(time.time())
        discuss.created_by = admin_user.id
        discuss.save()
        body =  admin_user.username + u'：' + content
        ausers = AdminUser.select().where((AdminUser.mobile != '') & (AdminUser.isactive == 1))
        c = ausers.count()
        sms = {'apptype': 4, 'body': body, 'receiver': []}
        for au in ausers:
            sms['receiver'].append(au.mobile)
        create_msg(simplejson.dumps(sms), 'jpush')

        self.redirect('/admin/discuss/' + tid)

@route(r'/admin/change_topic/(\d+)', name='admin_change_topic')  # 改变话题状态
class ChangeTopicHandler(AdminBaseHandler):
    def get(self, tid):
        admin_user = self.get_admin_user()
        status = int(self.get_argument('status', 0))
        top = Topic.get(id = tid)
        top.status = status
        if status == 1:
            top.completed = int(time.time())
            top.complete_by = admin_user.id
        elif status == 2:
            top.closed = int(time.time())
            top.close_by = admin_user.id
        top.save()
        self.redirect('/admin/topic')

@route(r'/admin/hot_search', name='admin_hot_search')  # 热门搜索
class HotSearchHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        status = int(self.get_argument('status', -1))
        if status != -1:
            search = Hot_Search.select().where(Hot_Search.status == status)
        else:
            search = Hot_Search.select().where(Hot_Search.status != -1)
        total = search.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        s = search.order_by(Hot_Search.quantity.desc()).paginate(page, pagesize)
        self.render('/admin/topic/search.html', search=s, active='hot_search', total=total, page=page,
                    pagesize=pagesize, totalpage=totalpage, status=status)

@route(r'/admin/search_change_status/(\d+)', name='admin_search_change_status')  #更改搜索关键词状态
class SearchChangeStatusHandler(AdminBaseHandler):
    def get(self, tid):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        status = int(self.get_argument('status', 0))
        s = int(self.get_argument('s', 0))
        hot = Hot_Search.get(id = tid)
        hot.status = status
        hot.save()
        self.redirect('/admin/hot_search?status='+str(s)+'&page=' + str(page))

@route(r'/admin/check_order_timeout', name='admin_check_order_timeout')  # 定时清理超过48小时的待款状态订单
class CheckOrderTimeoutHandler(BaseHandler):
    def get(self):
        msg = []
        two_day = (datetime.datetime.now() - datetime.timedelta(hours = 48)) #自动修改两天之前的待付款订单
        time_stamp = int(time.mktime(two_day.timetuple()))
        ft = Order.ordered < time_stamp
        orders = Order.select().where((Order.status == 0) & ft & ((Order.payment == 1) | (Order.payment == 3)))
        ocount = orders.count()
        onum = ''
        msg1 = ''
        for o in orders:
            OrderChangeStatus(o.id, 5, 0, self)
            OrderChangeStatus(o.id, -1, 0, self)
            o.lasteditedby = u"订单超过48小时未付款，系统自动设置为已删除"
            o.lasteditedtime = int(time.time())
            o.status = -1
            o.save()
            onum += o.ordernum + u'，'

        msg.insert(0, u'共有' + str(ocount) + u'个订单超过48小时未付款，系统自动设置为已删除。')
        msg.insert(1, u'订单编号为：' + onum)
        msg = u'<br/>'.join(msg)
        self.write(msg)

@route(r'/admin/recompute_avg_quantity', name='admin_recompute_avg_quantity')  # 定时统计所有产品最近一周的平均销量
class RecomputeAvgQuantityHandler(BaseHandler):
    def ComputeQuantity(self,pid):
        quantity=0;
        days=7
        end_time=time.mktime(time.strptime(datetime.datetime.now().strftime('%Y-%m-%d'),"%Y-%m-%d"))
        begin_time=end_time-days*24*60*60

        qoi=OrderItem.select().join(Order).where((Order.ordered>begin_time)&(Order.ordered<end_time)&(OrderItem.product==pid)
                                                 &(((Order.status>=1)&( Order.status<=4 )&( Order.payment>0))|((Order.payment==0  )&( Order.status< 5))))

        for oi in qoi:
            quantity=quantity+oi.weight*oi.quantity

        quantity=quantity/days # 单日销量，按斤
        return quantity;
    def get(self):
        msg = []
        qproduct = Product.select().where((Product.is_store == 0) )
        ocount=qproduct.count()
        for p in qproduct:
            p.avg_quantity=self.ComputeQuantity(p.id)
            p.save()

        msg.insert(0, u'共有' + str(ocount) + u'个产品的销量重新计算。')
        msg = u'<br/>'.join(msg)
        self.write(msg)

@route(r'/admin/check_activity_order_timeout', name='admin_check_activity_order_timeout')  # 定时清理超过30分钟的待款状态订单
class CheckOrderTimeoutHandler(BaseHandler):
    def get(self):
        msg = []
        two_day = (datetime.datetime.now() - datetime.timedelta(minutes = 30)) #自动修改30分钟之前的待付款订单
        time_stamp = int(time.mktime(two_day.timetuple()))
        ft = Order.ordered < time_stamp
        orders = OrderItem.select().join(Order, on=(Order.id == OrderItem.order)).where((Order.status == 0) & ft &
                                (OrderItem.item_type == 1))
        ocount = orders.count()
        onum = ''

        for o in orders:
            if o.order.status == 0:
                OrderChangeStatus(o.order.id, 5, 0, self)
                OrderChangeStatus(o.order.id, -1, 0, self)
                o.order.lasteditedby = u"活动订单超过30分钟未付款，系统自动设置为已删除"
                o.order.lasteditedtime = int(time.time())
                o.order.status = -1
                o.order.save()
            pa = Product_Activity.select().where(Product_Activity.product == o.product).order_by(Product_Activity.created.desc())
            if pa.count() > 0:
                pa[0].quantity += 1
                pa[0].save()

            onum += o.order.ordernum + u'，'

        msg.insert(0, u'共有' + str(ocount) + u'个活动商品超过30分钟未付款，系统自动设置为已删除。')
        msg.insert(1, u'订单编号为：' + onum)
        msg = u'<br/>'.join(msg)
        self.write(msg)

@route(r'/admin/consult', name='admin_consult')  # 售后咨询
class ConsultHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        userid = self.get_argument("uid",None)
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", None)
        status = int(self.get_argument("status", -1))
        ft = (Consult.id > 0)

        if keyword:
            keyword = '%' + keyword + '%'
            ft = ft & (Consult.content % keyword)
        if status > -1:
            ft = ft & (Consult.isactive == status)
        if userid:
            ft = ft & (Consult.user == userid)
        uq = Consult.select().where(ft)
        total = uq.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize

        cs = uq.order_by(Consult.created.desc()).paginate(page, pagesize)

        self.render('/admin/consult/consult_list.html', cs=cs, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='consult', uid=userid, status=status)

@route(r'/admin/consult_reply/(\d+)', name='admin_consult_reply')  # 售后咨询回复
class ConsultReplyHandler(AdminBaseHandler):
    def get(self,cid):
        c = Consult.get(id = cid)
        self.render('/admin/consult/consult_reply.html', c=c, active='consult')
    def post(self,cid):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        uid = self.get_argument("uid",None)
        status = self.get_argument("status",None)
        reply_content = self.get_argument("reply_content", "")
        c = Consult.get(id = cid)
        c.reply_content = reply_content
        c.reply_time = int(time.time())
        c.isactive = 2  # 2 代表已回复
        c.save()
        self.redirect('/admin/consult?page=' + str(page) + '&uid=' + str(uid) + '&status=' + str(status))

@route(r'/admin/comment_reply/(\d+)', name='admin_comment_reply')  # 商品评价回复
class CommentReplyHandler(AdminBaseHandler):
    def get(self,cid):
        c = Comment.get(id = cid)
        self.render('/admin/consult/comment_reply.html', c=c, active='comment')
    def post(self,cid):
        reply_content = self.get_argument("reply_content", "")
        status = int(self.get_argument("status", 0))
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        uid = self.get_argument("uid",None)
        pid = self.get_argument("pid", None)
        begin_date = self.get_argument("begindate", '')
        end_date = self.get_argument("enddate", '')
        c = Comment.get(id = cid)
        c.reply_content = reply_content
        c.reply_time = int(time.time())
        if status:
            c.status = status
        c.save()
        self.redirect('/admin/comment?page='+ str(page) + '&uid='+ str(uid) +'&pid='+ str(pid) + '&begindate='+
         begin_date + '&enddate=' + end_date)


@route(r'/admin/product/activity', name='admin_product_activity')  # 限时抢购商品
class ProductActivityHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", None)
        #status = int(self.get_argument("status", 1))
        ft = ((Product_Activity.id > 0) & (Product_Activity.type == 1) & (Product_Activity.status > 0))

        if keyword:
            keyword = '%' + keyword + '%'
            ft = ft & (Product_Activity.product.name % keyword)
        #if status > -1:
        #    ft = ft & (Product_Activity.status == status)
        pa = Product_Activity.select().where(ft)
        total = pa.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize

        pas = pa.order_by(Product_Activity.created.desc()).paginate(page, pagesize)
        for n in pas:
            flymscount = self.application.session_store.get_session('psid_'+str(n.product_standard.id), '')
            n.quantity = flymscount if flymscount else 0
        self.render('/admin/product/product_activity.html', pas=pas, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='product_activity')


@route(r'/admin/product/activity/edit/(\d+)', name='admin_product_activity_edit')  # 编辑限时抢购商品
class ProductActivityEditHandler(AdminBaseHandler):
    def get(self, cid):
        if str(cid) == '0':
            pa = None
        else:
            pa = Product_Activity.get(Product_Activity.id == cid)
            flymscount = self.application.session_store.get_session('psid_'+str(pa.product_standard.id), '')
            pa.quantity = flymscount if flymscount else 0
        products = Product.select().where(Product.status == 1).order_by(Product.sku.asc())

        self.render('/admin/product/product_activity_edit.html', pa=pa, products=products,cid=str(cid), active='product_activity')

    def post(self, cid):
        product = self.get_argument("product", "")
        quantity = int(self.get_argument("quantity", 0))
        begin_time = self.get_argument("begin_time", "")
        end_time = self.get_argument("end_time", "")
        price = float(self.get_argument("price", 1.0))
        platform = int(self.get_argument("platform", 0))
        status = int(self.get_argument("status", 0))
        try:
            if cid == '0':
                c = Product_Activity()
            else:
                c = Product_Activity.get(id=cid)
            product = Product.get(id=product.split(';')[0])
            c.product = product
            c.product_standard = product.defaultstandard
            c.quantity = quantity
            c.begin_time = time.mktime(time.strptime(begin_time, "%Y-%m-%d %H:%M:%S"))
            c.end_time = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
            c.price = price
            c.platform = platform
            c.created = int(time.time())
            c.created_by = self.get_admin_user()
            if status:
                c.status = status
            c.save()
            self.flash("操作成功！")
            key = 'psid_' + str(c.product_standard.id)
            self.application.session_store.set_session(key, c.quantity, None, expiry=24*60*60*10)
            # value = self.application.session_store.get_session(key,None)
        except Exception, ex:
            logging.error(u'编辑活动商品失败：'+ex.message)
            self.flash("操作失败！"+ex.message)
        self.redirect('/admin/product/activity/edit/'+cid)


@route(r'/admin/product_activity/change/(\d+)', name='admin_product_activity_change')  # 删除限时抢购商品
class ProductActivityEditHandler(AdminBaseHandler):
    def get(self, cid):
        status = int(self.get_argument("status", 0))
        if cid:
            pa = Product_Activity.get(Product_Activity.id == cid)
            pa.status = status
            pa.save()
        self.redirect('/admin/product/activity')


@route(r'/admin/product/jfmanager', name='admin_product_jfmanager')  # 积分换购
class ProductJFManagerHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", None)
        # status = int(self.get_argument("status", 1))
        ft = ((Product_Activity.id > 0) & (Product_Activity.type == 2) & (Product_Activity.status > 0))

        if keyword:
            keyword = '%' + keyword + '%'
            ft = ft & (Product_Activity.product.name % keyword)
        # if status > -1:
        #     ft = ft & (Product_Activity.status == status)
        pa = Product_Activity.select().where(ft)
        total = pa.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize

        pas = pa.order_by(Product_Activity.created.desc()).paginate(page, pagesize)

        self.render('/admin/product/product_jfmanager.html', pas=pas, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='product_jfmanager')


@route(r'/admin/product/jfmanager/edit/(\d+)', name='admin_product_jfmanager_edit')  # 编辑积分换购
class ProductJFManagerEditHandler(AdminBaseHandler):
    def get(self, cid):
        if str(cid) == '0':
            pa = None
        else:
            pa = Product_Activity.get(Product_Activity.id == cid)
        products = Product.select().where(Product.status == 1).order_by(Product.sku.asc())
        self.render('/admin/product/product_jfmanager_edit.html', pa=pa, products=products,cid=str(cid), active='product_jfmanager')

    def post(self, cid):
        product = self.get_argument("product", "")
        quantity = int(self.get_argument("quantity", 0))
        begin_time = self.get_argument("begin_time", "")
        end_time = self.get_argument("end_time", "")
        price = float(self.get_argument("price", 1.0))
        platform = int(self.get_argument("platform", 0))
        status = int(self.get_argument("status", 0))
        try:
            if cid == '0':
                c = Product_Activity()
            else:
                c = Product_Activity.get(id=cid)
            product = Product.get(id=product.split(';')[0])
            c.product = product
            c.product_standard = product.defaultstandard
            c.quantity = quantity
            c.begin_time = time.mktime(time.strptime(begin_time, "%Y-%m-%d %H:%M:%S"))
            c.end_time = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
            c.price = price
            c.platform = platform
            c.created = int(time.time())
            c.created_by = self.get_admin_user()
            c.type = 2
            if status:
                c.status = status
            c.save()
            self.flash("操作成功！")
        except Exception, ex:
            logging.error(u'编辑积分换购商品失败：'+ex.message)
            self.flash("操作失败！")
        self.redirect('/admin/product/jfmanager/edit/'+cid)


@route(r'/admin/product_jfmanager/change/(\d+)', name='admin_product_jfmanager_change')  # 删除积分换购
class ProductJFManagerEditHandler(AdminBaseHandler):
    def get(self, cid):
        status = int(self.get_argument("status", 0))
        if cid:
            pa = Product_Activity.get(Product_Activity.id == cid)
            pa.status = status
            pa.save()
        self.redirect('/admin/product/jfmanager')

@route(r'/admin/product/raffle_list', name='admin_product_raffle_list')  # 奖品列表
class ProductActivityHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", None)
        #status = int(self.get_argument("status", 1))
        ft = (User_Raffle_Log.id > 0)
        if keyword:
            keyword = '%' + keyword + '%'
            ft = ft & (User_Raffle_Log.draw_name % keyword)
        ft = ft & (User_Raffle_Log.draw_level << [1,2,7,8,9] )  # 仅显示实物奖品
        raffle = User_Raffle_Log.select().where(ft)
        total = raffle.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize

        raffles = raffle.order_by(User_Raffle_Log.created.desc()).paginate(page, pagesize)

        self.render('/admin/product/raffle_list.html', raffles=raffles, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='raffle')

@route(r'/admin/raffle/change/(\d+)', name='admin_raffle_change')  # 删除获奖信息
class ProductJFManagerEditHandler(AdminBaseHandler):
    def get(self, cid):
        status = int(self.get_argument("status", 0))
        if cid:
            r = User_Raffle_Log.get(User_Raffle_Log.id == cid)
            r.delete_instance()
        self.redirect('/admin/product/raffle_list')

@route(r'/admin/delete_coupon_real/(\d+)', name='delete_coupon_real')  # 删除实物优惠券
class DeleteCouponRealHandler(AdminBaseHandler):
    def get(self, cid):
        c = CouponReal.get(CouponReal.id == cid)
        content = {}
        content['operatetype'] = u'删除用户实物券'
        content['pid'] = cid
        uid = c.user.id
        content['user_id'] = uid
        c.status = 0
        c.user = None
        c.save()
        AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        self.redirect('/admin/user/' + str(uid))

@route(r'/admin/delete_gift/(\d+)', name='delete_gift')  # 删除用户赠品信息
class DeleteGiftHandler(AdminBaseHandler):
    def get(self, gid):
        c = Gift.get(Gift.id == gid)
        content = {}
        content['operatetype'] = u'删除用户实物券'
        content['pid'] = gid
        uid = c.user.id
        content['user_id'] = uid
        if c.status != 1:
            Gift.delete().where(Gift.id == gid).execute()
            self.flash(u"删除成功！")
        else:
            self.flash(u"商品已领取，无法删除！")
        AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        self.redirect('/admin/user/' + str(uid))


@route(r'/wl/login', name='delivery_login')  # 物流公司登录
class DeliveryLoginHandler(BaseHandler):
    def get(self):
        self.render('/admin/delivery/login.html')
    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)

        if username and password:
            if (username == u'速尚') and (password == 'sushang'):
                self.set_secure_cookie('wl', username, expires_days=1)
                self.redirect("/wl/order")
            else:
                self.flash("用户名或密码错误！")

        else:
            self.flash("请输入用户名或者密码！")

@route(r'/wl/order', name='delivery_order')  # 物流公司订单管理
class DeliveryOrderHandler(BaseHandler):
    def get(self):
        name = self.get_secure_cookie('wl')
        if name == '速尚':
            page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
            status = int(self.get_argument("status", 3))
            pagesize = self.settings['admin_pagesize']
            keyword = self.get_argument("keyword", '')
            begindate = self.get_argument("begindate", '')
            enddate = self.get_argument("enddate", '')
            statuscheck = int(self.get_argument("statuscheck", '-1') if len(self.get_argument("statuscheck", '1')) > 0 else '-1')

            ft = ((Order.status == 4) | (Order.status == 3)) & (Order.delivery == 2)

            phone = self.get_argument("phone", '')

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
                    else:
                        ft = ft & (Order.status == status)
                else:
                    if statuscheck != -1 and statuscheck != '':
                        if statuscheck == 0:  # 待付款
                            ft = ft & ((Order.status == 0) & ((Order.payment == 1 | (Order.payment == 3))))
                        elif statuscheck == 1:  # 待处理
                            ft = ft & ((Order.status == 1) | ((Order.payment == 0) & (Order.status == 0)))
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
                oCount = DeliveryOrderStatus.select().where((DeliveryOrderStatus.order == o.id)).count()
                if oCount>0:
                    o.pay_response = '1'
            self.render('admin/delivery/orders.html', orders=orders, total=total, page=page, pagesize=pagesize,username=unicode(name, "utf-8"),
            totalpage=totalpage, status=status, active='orders', begindate=begindate, enddate=enddate, keyword=keyword,phone=phone)
        else:
            self.redirect("/wl/login")

@route(r'/wl/mark', name='delivery_mark')  # 物流公司标记未送达原因
class DeliveryMarkHandler(BaseHandler):
    def get(self):
        name = self.get_secure_cookie('wl')
        if name == '速尚':
            oid = self.get_argument("oid", '')
            if oid:
                order = Order.select().where(Order.id == oid)[0]
                try:
                    dos = DeliveryOrderStatus.select().where(DeliveryOrderStatus.order == oid)[0]
                except:
                    dos = None
            else:
                order = None
                dos = None
            self.render('admin/delivery/mark.html', o=order, oid=oid, dos=dos)
        else:
            self.redirect("/wl/login")
    def post(self):
        oid = self.get_argument("oid", '')
        did = self.get_argument("delivery", '')
        content = self.get_argument("content", '')
        order = Order.select().where(Order.id == oid)
        if oid:
            dos = DeliveryOrderStatus.select().where((DeliveryOrderStatus.order == oid) & (DeliveryOrderStatus.delivery == did))
            if dos.count() < 1:
                os = DeliveryOrderStatus()
                dos = None
            else:
                os = dos[0]
                dos = dos[0]
            os.delivery = did
            os.order = oid
            os.content = content
            os.save()
            self.flash("提交成功！")
        else:
            dos = None
            self.flash("提交失败！")
        self.render('admin/delivery/mark.html', o=order[0], dos=dos)

@route(r'/wl/kdy_info', name='delivery_kdy_info')  # 快递员信息
class DeliveryMarkHandler(BaseHandler):
    def get(self):
        name = self.get_secure_cookie('wl')
        if name == '速尚':
            oid = self.get_argument("oid", '')
            if oid:
                order = Order.select().where(Order.id == oid)[0]
            else:
                order = None
            self.render('admin/delivery/kdyinfo.html', o=order, oid=oid)
        else:
            self.redirect("/wl/login")
    def post(self):
        oid = self.get_argument("oid", '')
        kdy_name = self.get_argument("kdy_name", '')
        kdy_mobile = self.get_argument("kdy_mobile", '')

        if oid:
            order = Order.get(Order.id == oid)
            order.kdy_name = kdy_name
            order.kdy_mobile = kdy_mobile
            order.save()
            self.flash("提交成功！")
        else:
            self.flash("提交失败！")
        self.render('admin/delivery/kdyinfo.html', o=order)

@route(r'/admin/product/price_list', name='admin_product_price_list')  # 商品价格列表
class ProductPriceListHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = 200
        keyword = self.get_argument("keyword", None)
        ft = (Product.id > 0)
        if keyword:
            keyword = '%' + keyword + '%'
            ft = ft & (Product.name % keyword)
        product = ProductStandard.select(ProductStandard,
                                          (ProductStandard.price/ProductStandard.weight*500).alias('uprice')).\
            join(Product, on=((Product.id == ProductStandard.product) & (Product.status==1)))
        total = product.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize

        products = product.order_by(Product.id).paginate(page, pagesize)

        self.render('/admin/product/price_list.html', products=products, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='price')

@route(r'/admin/other/query_vcode', name='other_query_vcode')  # 查询验证码
class AddGiftHandler(AdminBaseHandler):
    def get(self):
        mobile = self.get_argument('mobile', '')
        if mobile:
            try:
                uv = UserVcode.select().where(UserVcode.mobile == mobile).order_by(UserVcode.created.desc())[0]
                self.flash("查询成功！")
            except:
                uv = None
                self.flash("查询失败，没有查询到验证码，请重试！")
        else:
            uv = None
            self.flash("请输入手机号码！")
        self.render('admin/other/query_vcode.html', uv=uv, mobile=mobile, active='users')
    def post(self):
        mobile = self.get_argument('mobile', '')
        if mobile:
            try:
                uv = UserVcode.select().where(UserVcode.mobile == mobile)[0]
            except:
                uv = None
        else:
            uv = None
        self.render('admin/other/query_vcode.html', uv=uv,mobile=mobile, active='users')

@route(r'/admin/medias', name='admin_medias')  # 媒体报道
class MediaHandler(AdminBaseHandler):
    def get(self):
        medias = MediaNews.select().order_by(MediaNews.sort.desc())
        self.render('admin/ad/medias.html', medias=medias, active='medias')

@route(r'/admin/media/(\d+)', name='admin_editmedia')   # 媒体报道编辑
class EditMediaHandler(AdminBaseHandler):
    def get(self, aid):
        if str(aid) == '0':
            ad = None
        else:
            ad = MediaNews.get(MediaNews.id == aid)
        aid = int(aid)

        self.render('admin/ad/edit_media.html', ad=ad, active='media')

    def post(self, aid):
        url = self.get_argument("url", '')
        imgalt = self.get_argument("imgalt", '')
        title = self.get_argument("title", '')
        content = self.get_argument("content", '')
        sort = int(self.get_argument("sort", 1))
        if aid == '0':
            ad = MediaNews()
        else:
            ad = MediaNews.get(id=aid)

        ad.url = url
        ad.imgalt = imgalt
        ad.sort = sort
        ad.title = title
        ad.content = content
        ad.created = int(time.time())
        try:
            if self.request.files:
                datetime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))  # 获取当前时间作为图片名称
                filename = str(datetime) + ".jpg"
                with open('upload/media/' + filename, "wb") as f:
                    f.write(self.request.files["file"][0]["body"])
                ad.picurl = filename
                if self.settings['syncimg']:
                    urls = []
                    urls.append('http://admin.eofan.com'+'/upload/media/' + filename)
                    create_msg(simplejson.dumps(urls), 'img')
            # ad.validate()
            ad.save()
            # self.flash(u"媒体报道编辑成功")
        except Exception, ex:
            self.flash(str(ex))
        self.redirect("/admin/medias")


@route(r'/admin/del_media/(\d+)', name='admin_delmedia')    # 媒体报道删除
class DelMediaHandler(AdminBaseHandler):
    def get(self, aid):
        MediaNews.delete().where(MediaNews.id == aid).execute()
        # self.flash(u"媒体报道删除成功")
        self.redirect("/admin/medias")

@route(r'/admin/product/reserve', name='admin_product_reserve')  # 预售商品
class ProductReserveHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", None)
        #status = int(self.get_argument("status", 1))
        ft = ((Product_Reserve.id > 0) & (Product_Reserve.status > 0))

        if keyword:
            keyword = '%' + keyword + '%'
            ft = ft & (Product_Reserve.product.name % keyword)
        #if status > -1:
        #    ft = ft & (Product_Reserve.status == status)
        pa = Product_Reserve.select().where(ft)
        total = pa.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize

        pas = pa.order_by(Product_Reserve.created.desc()).paginate(page, pagesize)

        self.render('/admin/product/product_reserve.html', pas=pas, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='reserve')


@route(r'/admin/product/reserve/edit/(\d+)', name='admin_product_reserve_edit')  # 编辑预售商品
class ProductReserveEditHandler(AdminBaseHandler):
    def get(self, cid):
        if str(cid) == '0':
            pa = None
        else:
            pa = Product_Reserve.get(Product_Reserve.id == cid)
        products = Product.select().order_by(Product.sku.asc()) #.where(Product.status == 1)

        self.render('/admin/product/product_reserve_edit.html', pa=pa, products=products,cid=str(cid), active='reserve')

    def post(self, cid):
        product = self.get_argument("product", "")
        quantity = int(self.get_argument("quantity", 0))
        begin_time = self.get_argument("begin_time", "")
        end_time = self.get_argument("end_time", "")
        price = float(self.get_argument("price", 1.0))
        platform = int(self.get_argument("platform", 0))
        status = int(self.get_argument("status", 0))
        quantity_stage1 = int(self.get_argument("quantity_stage1", 0))
        price_stage1 = float(self.get_argument("price_stage1", 1.0))
        quantity_stage2 = int(self.get_argument("quantity_stage2", 0))
        price_stage2 = float(self.get_argument("price_stage2", 1.0))
        delivery_time = self.get_argument("delivery_time", "")
        try:
            if cid == '0':
                c = Product_Reserve()
            else:
                c = Product_Reserve.get(id=cid)
            product = Product.get(id=product.split(';')[0])
            c.product = product
            c.product_standard = product.defaultstandard
            c.quantity = quantity
            c.begin_time = time.mktime(time.strptime(begin_time, "%Y-%m-%d %H:%M:%S"))
            c.end_time = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
            c.price = price
            c.platform = platform
            c.created = int(time.time())
            c.created_by = self.get_admin_user()
            c.quantity_stage1 = quantity_stage1
            c.price_stage1 = price_stage1
            c.quantity_stage2 = quantity_stage2
            c.price_stage2 = price_stage2
            c.delivery_time = time.mktime(time.strptime(delivery_time, "%Y-%m-%d %H:%M:%S"))
            if status:
                c.status = status
            c.save()

            p = Product.get(id = product)
            p.is_reserve = 1
            p.reserve_time = time.mktime(time.strptime(delivery_time, "%Y-%m-%d %H:%M:%S"))
            p.save()
            self.flash("操作成功！")
        except Exception, ex:
            logging.error(u'编辑活动商品失败：'+ex.message)
            self.flash("操作失败！"+ex.message)
        self.redirect('/admin/product/reserve/edit/'+cid)


@route(r'/admin/product_reserve/change/(\d+)', name='admin_product_reserve_change')  # 更改预售商品状态
class ProductReserveEditHandler(AdminBaseHandler):
    def get(self, cid):
        status = int(self.get_argument("status", 0))
        if cid:
            pa = Product_Reserve.get(Product_Reserve.id == cid)
            pa.status = status
            pa.save()
        self.redirect('/admin/product/reserve')

@route(r'/admin/delivery_order', name='admin_delivery_order')  # 当日发货订单数据
class DeliveryOrderHandler(AdminBaseHandler):
    def get(self):
        result = []
        date = self.get_argument('begindate', '')
        if date:
            begindate = time.mktime(time.strptime(date, "%Y-%m-%d"))
            enddate = time.mktime(time.strptime((date + " 23:59:59"), "%Y-%m-%d %H:%M:%S"))
        else:
            begindate = time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime(time.time())), "%Y-%m-%d"))
            enddate = time.mktime(time.strptime(time.strftime("%Y-%m-%d 23:59:59", time.localtime(time.time())), "%Y-%m-%d %H:%M:%S"))

        sql = '''
        SELECT a.id, a.sku, a.name as pname, a.defaultstandard as psid, e.price,truncate((e.price/e.weight*500),2) as uprice,
        e.name as psname, e.weight,
        (case when (select sum(b.quantity) from jz_order_items b Inner Join jz_orders c On(c.id = b.order_id) where b.product_id = a.id
        and (c.status > 0) and (c.status<5) AND (c.delivery_time > %s) AND (c.delivery_time < %s)) is  null then 0 else
        (select sum(b.quantity) from jz_order_items b Inner Join jz_orders c On(c.id = b.order_id) where b.product_id = a.id
        and (c.status > 0) and (c.status<5) AND (c.delivery_time > %s) AND (c.delivery_time < %s))
         end) as sale_quantity,truncate(
        (case when(select d.unitprice from jz_invoicing as d where d.product_id = a.id order by id desc limit 1) is null then 0 else
         (select d.unitprice from jz_invoicing as d where d.product_id = a.id order by id desc limit 1) end)
         ,2)  as cprice FROM jz_product AS a Inner Join jz_product_standard as e on(e.product_id = a.id)
        where a.status=1 GROUP BY a.id, a.sku, a.name, a.defaultstandard,cprice ORDER BY a.id;
        '''
        q = db.handle.execute_sql(sql % (begindate, enddate, begindate, enddate))

        for row in q.fetchall():
            result.append({'pname': row[2], 'psname': row[6], 'weight': row[7], 'uprice': row[5], 'price': row[4], 'sale_quantity': row[8], 'cprice': row[9]})
        self.render('/admin/other/delivery_order.html',q=result, begindate=date)

@route(r'/admin/offline_products', name='admin_offline_products')  # 门店商品管理
class ProductHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", None)
        barcode = self.get_argument("barcode", None)
        status = int(self.get_argument("status", '0') if len(self.get_argument("status", '0')) > 0 else '0')
        begindate = self.get_argument("begindate", '')
        enddate = self.get_argument("enddate", '')
        store_id = int(self.get_argument('store_id','0') if len(self.get_argument("store_id", '0')) > 0 else '0')

        if status == 0 or status == 1 or status == 2:
            ft = (ProductOffline.status >= 0) & (ProductOffline.status <= 2)
        elif status == 3:
            ft = (ProductOffline.status == 3)
        elif status == 4 or status == 5:
            ft = (ProductOffline.status >= 4) & (ProductOffline.status <= 5)
        else:
            ft = (ProductOffline.status >= 0)

        if keyword:
            keyw = '%' + keyword + '%'
            ft = ft & (Product.name % keyw)
        if barcode:
            b = '%' + barcode + '%'
            ft = ft & (ProductOffline.barcode % b)
        if store_id:
            ft = ft & (ProductOffline.store == store_id)

        if not begindate:
            lastDate = datetime.date.today() - datetime.timedelta(days=1)
            begindate=lastDate.strftime('%Y-%m-%d')
        if not enddate:
            enddate=datetime.date.today().strftime('%Y-%m-%d')

        begin = time.strptime(begindate, "%Y-%m-%d")
        end = time.strptime((enddate + " 23:59:59"), "%Y-%m-%d %H:%M:%S")
        if status==2:
            ft = ft & (ProductOffline.in_time > time.mktime(begin)) & (ProductOffline.in_time < time.mktime(end))
        elif status==3:
            ft = ft & (ProductOffline.sale_time > time.mktime(begin)) & (ProductOffline.sale_time < time.mktime(end))
        elif status==4:
            ft = ft & (ProductOffline.cancel_time > time.mktime(begin)) & (ProductOffline.cancel_time < time.mktime(end))
        else:
            ft = ft & (ProductOffline.out_time > time.mktime(begin)) & (ProductOffline.out_time < time.mktime(end))

        q = ProductOffline.select(ProductOffline, Product).join(Product).where(ft)
        total = q.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        products = q.order_by(ProductOffline.id.desc()).paginate(page, pagesize).aggregate_rows()

        stores=Store.select().where(Store.storetype==0).order_by(Store.id)
        self.render('admin/product/offline_products.html', products=products, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, barcode=barcode, active='store_p', status=status, keyword=keyword,begindate=begindate,enddate=enddate,stores=stores,store_id=store_id)

@route(r'/admin/test', name='admin_test')  # 测试mongoDB
class AdminTestHandler(AdminBaseHandler):
    def get(self):
        content = {}
        content['user_id'] = self.get_admin_user().id
        content['datetime'] = time.time()
        content['content'] = u'测试日志内容'
        content['order_id'] = u'2012'
        result = sys_log_data(content)
        print result

@route(r'/admin/test_import', name='admin_test_import')  # 测试将AdminLog导入mongoDB
class AdminTestImportHandler(AdminBaseHandler):
    def get(self):
        log = AdminLog.select().order_by(AdminLog.id.desc()).limit(100)
        result = import_log_data(log)
        print result

@route(r'/admin/zhicai', name='admin_zhicai')  # 直采统计
class AdminZhiCaiHandler(AdminBaseHandler):
    def get(self):
        result = []
        begin = self.get_argument('begindate', '')
        end = self.get_argument('enddate', '')
        if begin and end:
            begindate = time.mktime(time.strptime(begin, "%Y-%m-%d"))
            enddate = time.mktime(time.strptime((end + " 00:00:00"), "%Y-%m-%d %H:%M:%S"))
        else:
            begindate = time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime(time.time() - 86400 * 7)), "%Y-%m-%d"))
            enddate = time.mktime(time.strptime(time.strftime("%Y-%m-%d 00:00:00", time.localtime(time.time())), "%Y-%m-%d %H:%M:%S"))

        sql = '''
        Select c.name,c.producer,truncate(e.weight*count(b.quantity)/500,2) as s_weight,
        e.price,truncate(e.price/e.weight*500,2) as s_price, count(b.quantity) as s_quantity,e.weight,
        truncate(b.price*count(b.quantity),2) as s_total_price,
        truncate((select unitprice from jz_invoicing d where d.product_id=c.id order by id desc limit 1),2) as c_price,c.bz_days, c.id, c.status From
        jz_orders a,jz_order_items b, jz_product c, jz_product_standard e
        where a.id=b.order_id and b.product_id=c.id and e.product_id=c.id and c.args='B' and a.ordered > %s and a.ordered < %s and a.store_id is null
        and a.status>1 and a.status<5 group by c.name;
        '''
        q = db.handle.execute_sql(sql % (begindate, enddate))

        for row in q.fetchall():
            result.append({'id':row[10], 'name': row[0], 'producer': row[1], 's_weight': row[2], 'price': row[3], 's_price': row[4], 's_quantity': row[5],
                           'weight': row[6],'s_total_price': row[7],'c_price': row[8], 'bz_days': row[9],'status':row[11]})
        self.render('/admin/other/zhicai.html',q=result, begindate=begin, enddate=end, active='price')

@route(r'/admin/brand', name='admin_brand')  # 车型品牌管理
class BrandHandler(AdminBaseHandler):
    def get(self):
        items = Brand.select().where((Brand.pid==0) & (Brand.is_delete == 0)).order_by(Brand.spell,Brand.sort)
        self.render('admin/brand/list.html', items=items, active='brand')

@route(r'/admin/brand_add/(\d+)', name='admin_brand_add')  # 添加品牌
class AddBrandHandler(AdminBaseHandler):
    def get(self,id):
        pid =int(self.get_argument("pid", 0))
        brand = None
        options_parent = ""
        if int(id) > 0:
            brand = Brand.get(Brand.id == id)
            pid = brand.pid
            # options_parent = self.init_parents(brand.pid)
        # else:
            # options_parent = self.init_parents(int(pid))
        if pid > 0:
            brandP = Brand.get(Brand.id == pid)
        else:
            brandP = Brand()
            brandP.id = 0
            brandP.name = "根目录"
        options_parent = "<option value=\"%s\" selected>%s</option>" % (brandP.id , brandP.name)
        is_continue = 0
        self.render('admin/brand/add.html', active='brand', brand=brand, options_parent=options_parent,id=int(id), is_continue = is_continue)

    def post(self,id):
        pid = int(self.get_argument("pid", 0))
        name = self.get_argument("name", '')
        is_luxurious = int(self.get_argument("is_luxurious", '0'))
        is_continue = 0 # int(self.get_argument("is_continue", '0'))
        spell = self.get_argument("spell", '')
        spell_abb = self.get_argument("spell_abb", '')
        sort = int(self.get_argument("sort", 99))
        if not name:
            self.flash(u"请输入名称！")
        show_msg = ""
        if int(id) > 0:
            show_msg = "修改"
            brand = Brand.get(Brand.id == id)
        else:
            show_msg = "添加"
            brand = Brand()
            brand.pid = pid
            if pid > 0:
                brandP = Brand.get(Brand.id == pid)
                parent = Brand.select(db.fn.Max(Brand.code).alias('code')).where(Brand.pid == pid)
                if parent.count() > 0 :
                    l_code = parent[0].code[0:len(parent[0].code) - 4]
                    r_code = parent[0].code[len(parent[0].code) - 4:len(parent[0].code)]
                    new_code = int(r_code) + 1
                    new_code = str(new_code).rjust(4, '0')
                    brand.code = l_code + new_code
                    # brand.save()
                else:
                    new_code = brandP.code + '0001'
                    brand.code = new_code
                    # category.save()
            else:
                parent = Brand.select(db.fn.Max(Brand.code).alias('code')).where(Brand.pid == 0)
                if parent.count() > 0:
                    new_code = int(parent[0].code) + 1
                    new_code = str(new_code).rjust(4, '0')
                    brand.code = new_code
                else:
                    brand.code = "0001"
        brand.name = name
        brand.is_luxurious = is_luxurious
        brand.spell = spell
        brand.spell_abb = spell_abb
        brand.sort = sort
        try:
            brand.save()
            if pid>0 :
                brandP=Brand.get(Brand.id == pid)
                brandP.has_sub = 1
                brandP.save()
            self.flash(show_msg + u"成功")
        except Exception, ex:
            self.flash(str(ex))
        if is_continue==1:
            self.redirect('/admin/brand_add/0')
        else:
            self.redirect('/admin/brand')
    def init_parents(self, sel_id):
        item_template = "<option value=\"%s\">%s</option>"
        item_template_selected = "<option value=\"%s\" selected>%s</option>"
        options_parent=item_template % ("0" , "根目录")
        if sel_id==0:
            options_parent=item_template_selected % ("0" , "根目录")
        items = Brand.select().where(Brand.pid == 0).order_by(Brand.spell,Brand.sort)
        for item in items:
            blank = "├";
            name= "╋" + item.name
            if sel_id==item.id:
                options_parent = options_parent + item_template_selected % (item.id , name)
            else:
                options_parent = options_parent + item_template % (item.id , name)
            items_sub = Brand.select().where(Brand.pid == item.id).order_by(Brand.spell,Brand.sort)
            if items_sub.count() > 0:
                options_parent = options_parent + self.bind_sub(items_sub, blank, sel_id)
        return options_parent

    def bind_sub(self,items_sub, blank, sel_id):
        item_template = "<option value=\"%s\">%s</option>"
        item_template_selected = "<option value=\"%s\" selected>%s</option>"
        options_sub=""
        for item in items_sub:
            name= blank +"『" + item.name+ "』"
            if sel_id==item.id:
                options_sub = options_sub + item_template_selected  % (item.id , name)
            else:
                options_sub = options_sub + item_template  % (item.id , name)

            items_sub1 = Brand.select().where(Brand.pid == item.id).order_by(Brand.spell,Brand.sort)

            blank2 = blank + "─";
            if items_sub1.count() > 0:
                options_sub = options_sub + self.bind_sub(items_sub1, blank2, item_template)
        return options_sub

@route(r'/admin/brand_del/(\d+)', name='admin_brand_del')  # 删除品牌
class AddBrandHandler(AdminBaseHandler):
    def get(self,id):
        items_sub = Brand.select().where(Brand.pid == id)
        if items_sub.count() == 0:
            Brand.delete().where(Brand.id == id).execute()
            self.flash(u"删除成功！")
        else:
            self.flash(u"品牌包括下级分类，请先删除下级分类！")
        self.redirect('/admin/brand')

@route(r'/admin/area', name='admin_area')  # 区域管理
class AreaHandler(AdminBaseHandler):
    def get(self):
        items = Area.select().where((Area.pid==0) & (Area.is_delete == 0)).order_by(Area.sort,Area.id,Area.spell)
        self.render('admin/area/list.html', items=items, active='area')

@route(r'/admin/site', name='admin_site')  # 站点管理
class SiteHandler(AdminBaseHandler):
    def get(self):
        items = Area.select().where((Area.pid==0) & (Area.is_delete == 0) & (Area.is_site == 1)).order_by(Area.sort,Area.id,Area.spell)
        self.render('admin/area/site.html', items=items, active='site')

@route(r'/admin/area_add/(\d+)', name='admin_area_add')  # 添加区域
class AddAreaHandler(AdminBaseHandler):
    def get(self,id):
        pid =int(self.get_argument("pid", 0))
        area = None
        options_parent = ""
        if int(id) > 0:
            area = Area.get(Area.id == id)
            pid = area.pid
            # options_parent = self.init_parents(area.pid)
        # else:
            # options_parent = self.init_parents(int(pid))
        if pid > 0:
            brandP = Area.get(Area.id == pid)
        else:
            brandP = Area()
            brandP.id = 0
            brandP.name = "根目录"
        options_parent = "<option value=\"%s\" selected>%s</option>" % (brandP.id , brandP.name)
        is_continue = 0
        self.render('admin/area/add.html', active='area', area=area, options_parent=options_parent, id=int(id), is_continue = is_continue)

    def post(self,id):
        pid = int(self.get_argument("pid", 0))
        name = self.get_argument("name", '')
        is_site = int(self.get_argument("is_site", '0'))
        is_continue = 0 # int(self.get_argument("is_continue", '0'))
        spell = self.get_argument("spell", '')
        spell_abb = self.get_argument("spell_abb", '')
        sort = int(self.get_argument("sort", 99))
        if not name:
            self.flash(u"请输入名称！")
        show_msg = ""
        if int(id) > 0:
            show_msg = "修改"
            area = Area.get(Area.id == id)
        else:
            show_msg = "添加"
            area = Area()
            area.pid = pid
            if pid > 0:
                brandP = Area.get(Area.id == pid)
                parent = Area.select(db.fn.Max(Area.code).alias('code')).where(Area.pid == pid)
                if parent.count() > 0 :
                    l_code = parent[0].code[0:len(parent[0].code) - 4]
                    r_code = parent[0].code[len(parent[0].code) - 4:len(parent[0].code)]
                    new_code = int(r_code) + 1
                    new_code = str(new_code).rjust(4, '0')
                    area.code = l_code + new_code
                    # brand.save()
                else:
                    new_code = brandP.code + '0001'
                    area.code = new_code
                    # category.save()
            else:
                parent = Area.select(db.fn.Max(Area.code).alias('code')).where(Area.pid == 0)
                if parent.count() > 0:
                    new_code = int(parent[0].code) + 1
                    new_code = str(new_code).rjust(4, '0')
                    area.code = new_code
                else:
                    area.code = "0001"
        area.name = name
        area.is_site = is_site
        area.spell = spell
        area.spell_abb = spell_abb
        area.sort = sort
        try:
            area.save()
            if pid>0 :
                brandP=Area.get(Area.id == pid)
                brandP.has_sub = 1
                brandP.save()
            self.flash(show_msg + u"成功")
        except Exception, ex:
            self.flash(str(ex))
        if is_continue==1:
            self.redirect('/admin/brandadd/0')
        else:
            self.redirect('/admin/area')

@route(r'/admin/area_del/(\d+)', name='admin_area_del')  # 删除区域
class AdminAreaDelHandler(AdminBaseHandler):
    def get(self,id):
        items_sub = Area.select().where(Area.pid == id)
        if items_sub.count() == 0:
            Area.delete().where(Area.id == id).execute()
            self.flash(u"删除成功！")
        else:
            self.flash(u"区域包括下级分类，请先删除下级分类！")
        self.redirect('/admin/area')

@route(r'/admin/question', name='admin_question')  # 问答管理
class AdminQuestionHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", None)
        begindate = self.get_argument("begindate", '')
        enddate = self.get_argument("enddate", '')

        order_str = Question.created.desc()
        ft = (Question.is_delete == 0)

        if begindate and enddate:
            begin = time.strptime(begindate, "%Y-%m-%d")
            end = time.strptime((enddate + " 23:59:59"), "%Y-%m-%d %H:%M:%S")
            ft = ft & (Question.created > time.mktime(begin)) & (Question.created < time.mktime(end))

        if keyword:
            keyw = '%' + keyword + '%'
            ft = ft & (Question.content % keyw)

        q = Question.select().where(ft)
        total = q.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        lists = q.order_by(order_str).paginate(page, pagesize)

        self.render('/admin/ask/question.html', lists=lists, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='question', keyword=keyword,
                    begindate=begindate,enddate=enddate)

@route(r'/admin/question_del/(\d+)', name='admin_question_del')  # 删除问答
class QuestionDelHandler(AdminBaseHandler):
    def get(self,id):
        items_sub = Answer.select().where(Answer.question == id)
        for item in items_sub:
            item.is_delete = 1
            item.save()
        question = Question.get(Question.id == id)
        question.is_delete = 1
        question.save()
        # Question.delete().where(Question.id == id).execute()
        self.flash(u"删除成功！")
        self.redirect('/admin/question')


@route(r'/admin/question/(\d+)', name='admin_question_show')  # 问答详细
class QuestionShowHandler(AdminBaseHandler):
    def get(self, pid):
        p = Question.get(Question.id == pid)
        items_sub = Answer.select().where((Answer.question == pid)&(Answer.is_delete == 0))
        self.render('admin/ask/question_edit.html', p=p, items_sub=items_sub, active='question')


@route(r'/admin/question/(\d+)/(\d+)', name='admin_question_answer_del')  # 回答删除
class QuestionDelAnswerHandler(AdminBaseHandler):
    def get(self, pid, aid):
        p = Question.get(Question.id == pid)
        a = Answer.get(Answer.id == aid)
        a.is_delete = 1
        a.save()
        p.answers = p.answers -1
        p.save()
        self.redirect("/admin/question/"+pid)

@route(r'/admin/question_best/(\d+)/(\d+)', name='admin_question_best')  # 问答最佳
class QuestionAnswerBestHandler(AdminBaseHandler):
    def get(self, pid, aid):
        qa = Answer.select().where(Answer.question == pid)
        for a in qa:
            a.is_best = 0
            if a.id == int(aid):
                a.is_best = 1
            a.save()
        self.redirect("/admin/question/"+pid)

@route(r'/admin/circle', name='admin_circle')  # 圈子管理
class AdminCircleHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", None)
        begindate = self.get_argument("begindate", '')
        enddate = self.get_argument("enddate", '')

        order_str = CircleTopic.created.desc()
        ft = (CircleTopic.is_delete == 0)

        if begindate and enddate:
            begin = time.strptime(begindate, "%Y-%m-%d")
            end = time.strptime((enddate + " 23:59:59"), "%Y-%m-%d %H:%M:%S")
            ft = ft & (CircleTopic.created > time.mktime(begin)) & (CircleTopic.created < time.mktime(end))

        if keyword:
            keyw = '%' + keyword + '%'
            ft = ft & (CircleTopic.content % keyw)

        q = CircleTopic.select().where(ft)
        total = q.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        lists = q.order_by(order_str).paginate(page, pagesize)

        self.render('/admin/circle/topic.html', lists=lists, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='circle', keyword=keyword,
                    begindate=begindate,enddate=enddate)

@route(r'/admin/circle/(\d+)', name='admin_circle_show')  # 圈子详细
class CircleShowHandler(AdminBaseHandler):
    def get(self, pid):
        p = CircleTopic.get(CircleTopic.id == pid)
        # replies = CircleTopicReply.select().where((CircleTopicReply.is_delete == 0)&(CircleTopicReply.topic == pid))
        self.render('admin/circle/topic_edit.html', p=p, active='circle')

@route(r'/admin/circle_del/(\d+)', name='admin_circle_del')  # 删除问答
class CircleTopicDelHandler(AdminBaseHandler):
    def get(self,id):
        # items_sub = Answer.select().where(Answer.question == id)
        # for item in items_sub:
        #     item.is_delete = 1
        #     item.save()
        question = CircleTopic.get(CircleTopic.id == id)
        question.is_delete = 1
        question.save()
        # Question.delete().where(Question.id == id).execute()
        self.flash(u"删除成功！")
        self.redirect('/admin/circle')

@route(r'/admin/circle/(\d+)/(\d+)', name='admin_circle_reply_del')  # 圈子删除回复
class CircleTopicDelReplyHandler(AdminBaseHandler):
    def get(self, pid, aid):
        # a = CircleTopicReply.get(CircleTopicReply.id == aid)
        # a.delete()
        # a.save()

        CircleTopicReply.delete().where(CircleTopicReply.id == aid).execute()
        self.flash(u"回复删除成功")

        self.redirect("/admin/circle/"+pid)

@route(r'/admin/withdraw', name='admin_withdraw')  # 提现管理列表
class UserWithdrawHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        key = self.get_argument("keyword", None)
        begindate = self.get_argument("begindate", '')
        enddate = self.get_argument("enddate", '')
        status = self.get_argument("status", '')

        ft = (Withdraw.id > 0)

        if begindate and enddate:
            begin = time.strptime(begindate, "%Y-%m-%d")
            end = time.strptime((enddate + " 23:59:59"), "%Y-%m-%d %H:%M:%S")
            ft = ft & (Withdraw.apply_time > time.mktime(begin)) & (Withdraw.apply_time < time.mktime(end))

        if status:
            ft = ft & (Withdraw.status == status)
        if key:
            keyword = '%' + key + '%'
            ft = ft & ((User.username % keyword)|((User.mobile % keyword)))
            uq = Withdraw.select().join(User,on=(Withdraw.user == User.id)).where(ft)
        else:
            uq = Withdraw.select().where(ft)
        total = uq.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        lists = uq.order_by(Withdraw.apply_time.desc()).paginate(page, pagesize)

        self.render('/admin/user/withdraw.html', lists=lists, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='withdraw', keyword=key, begindate=begindate,enddate=enddate, status=status)

@route(r'/admin/admin_user/(\d+)', name='admin_admin_user')  # 管理员管理
class AdminUserHandler(AdminBaseHandler):
    def get(self, adminid):
        try:
            qadminuser =  AdminUser.select()
            if int(adminid)>0:
                adminUser=AdminUser.get(AdminUser.id==adminid)
            else:
                adminUser=None
            page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
            pagesize = self.settings['admin_pagesize']

            total = qadminuser.count()
            if total % pagesize > 0:
                totalpage = total / pagesize + 1
            else:
                totalpage = total / pagesize

            ivs = qadminuser.order_by(AdminUser.id.desc()).paginate(page, pagesize)
        except:
            self.write("程序出错了，可能是参数传递错误！")

        self.render('admin/admin/user.html', ivs=ivs,adminUser=adminUser,total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='admin_user')

    def post(self, adminid):
        adminid=int(adminid)
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        realname = self.get_argument('realname', '')
        mobile = self.get_argument('mobile', '')
        email = self.get_argument('email', '')
        roles = self.get_argument('roles', '')
        isactive=self.get_argument('isactive', '')

        if adminid>0:
            adminUser=AdminUser.get(AdminUser.id==adminid)
            if password:
                adminUser.password=AdminUser.create_password(password)
        else:
            adminUser=AdminUser();
            adminUser.signuped=int(time.time())
            adminUser.lsignined=0
            adminUser.password=AdminUser.create_password(password)

        adminUser.username=username
        adminUser.mobile=mobile
        adminUser.email=email
        adminUser.roles=roles
        adminUser.realname=realname
        if isactive:
            adminUser.isactive=1
        else:
            adminUser.isactive=0
        adminUser.save()
        self.flash("提交成功")
        self.redirect("/admin/admin_user/0")


@route(r'/admin/update', name='admin_update')  # 更新管理
class AdminMobileUpdateHandler(AdminBaseHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']

        order_str = MobileUpdate.updatedtime.desc()
        # ft = (MobileUpdate.is_delete == 0)


        q = MobileUpdate.select()
        total = q.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        lists = q.order_by(order_str).paginate(page, pagesize)

        self.render('/admin/update/update.html', lists=lists, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, active='update')

@route(r'/admin/update/(\d+)', name='admin_update_show')  # 圈子详细
class MobileUpdateShowHandler(AdminBaseHandler):
    def get(self, pid):
        if pid == '0':
            t = None
        else:
            t = MobileUpdate.get(MobileUpdate.id == pid)

        self.render('admin/update/update_edit.html', t=t, active='update')

    def post(self, pid):
        if pid == '0':
            p = MobileUpdate();
        else:
            p = MobileUpdate.get(MobileUpdate.id == pid)
        user=self.get_admin_user()
        name = self.get_argument("name", '')
        version = self.get_argument("version", '')
        path = self.get_argument("path", '')
        client = self.get_argument("client", '')
        state = int(self.get_argument("state", '0'))
        p.name = name
        p.version = version
        p.path = path
        p.client = client
        if state == 1:
             p.state = 1
        else:
             p.state = 0
        p.updatedby = user.id
        p.updatedtime = int(time.time())
        p.save()
        self.flash("保存成功")
        self.redirect('/admin/update')


@route(r'/admin/update_del/(\d+)', name='admin_update_del')  # 删除问答
class MobileUpdateDelHandler(AdminBaseHandler):
    def get(self,id):
        # items_sub = Answer.select().where(Answer.question == id)
        # for item in items_sub:
        #     item.is_delete = 1
        #     item.save()
        # question = MobileUpdate.get(MobileUpdate.id == id)
        # question.is_delete = 1
        # question.save()
        MobileUpdate.delete().where(MobileUpdate.id == id).execute()
        self.flash(u"删除成功！")
        self.redirect('/admin/update')