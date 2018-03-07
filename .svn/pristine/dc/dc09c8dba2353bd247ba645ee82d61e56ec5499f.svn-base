#!/usr/bin/env python
# coding=utf8

import logging
from handler import BaseHandler
from handler import BaseWithCityHandler
from lib.route import route
from lib.emailhelper import sendemail
from lib.mqhelper import create_msg
from lib.filter import filter_tags
from bootloader import db
import time
import simplejson
import tornado.escape
from model import AdminUser, User, Product, CategoryFront, Order, Ad, Page, Delivery, ProductPic, ProductStandard, \
    UserVcode, PageBlock, Fav, Oauth,Comment,ProductAttribute,Hot_Search,User_Promote,CouponTotal,Coupon,Cart,\
    Product_Activity,User_Raffle_Log, MediaNews,Product_Reserve,Store,Category_Store,Inventory_Store,ProductOffline,\
    StorePrice,User_Browse, Area, StoreNews, StoreNewsCategory, FavStore
from activity import new_user_balance
from activity import old_new_user_raffle
import base64
import httplib as client
import os
import random

def __init__(self, **settings):
    self.Tel = settings['COM_TEL']

@route(r'/', name='index')  #首页
class IndexHandler(BaseWithCityHandler):
    def get(self):
        # 根据用户浏览情况实现猜你喜欢
        try:
            ub = User_Browse.select().where(User_Browse.user == self.current_user.id)
            category_ids = [n.category_front for n in ub]
            similar_list = Product.select().where(Product.categoryfront << category_ids)
            similar_id = [n.defaultstandard for n in similar_list]
            cnxh_list = ProductStandard.select().join(Product).where((ProductStandard.id << random.sample(similar_id, 6)) & (Product.is_pass==1))
        except:
            cnxh_list = ProductStandard.select().join(Product).where((Product.status == 1) & (Product.is_pass==1)).order_by(Product.views.desc()).limit(6)

        city_id = self.get_secure_cookie("city_id")
        city_code = self.get_secure_cookie("city_code")
        code = city_code + '%'

        ft = (Product.status == 1)
        if city_code:
            ft = ft & (Product.area_code % code)
        qcpj_list = ProductStandard.select(ProductStandard, Product).join(Product, on=(ProductStandard.product == Product.id)).\
            join(CategoryFront, on=(Product.categoryfront == CategoryFront.id)).where(ft & (CategoryFront.type=='1') & (Product.is_pass==1)).order_by(Product.orders).limit(10)
        qcpj_recommend = ProductStandard.select(ProductStandard, Product).join(Product, on=(ProductStandard.product == Product.id)).\
            join(CategoryFront, on=(Product.categoryfront == CategoryFront.id)).where(ft & (CategoryFront.type=='1') & (Product.is_recommend == 1) & (Product.is_pass==1)).order_by(Product.orders).limit(10)
        qcpj_bargain = ProductStandard.select(ProductStandard, Product).join(Product, on=(ProductStandard.product == Product.id)).\
            join(CategoryFront, on=(Product.categoryfront == CategoryFront.id)).where(ft & (CategoryFront.type=='1') & (Product.is_bargain == 2) & (Product.is_pass==1)).order_by(Product.orders).limit(10)

        qcfw_list = ProductStandard.select(ProductStandard, Product).join(Product, on=(ProductStandard.product == Product.id)).\
            join(CategoryFront, on=(Product.categoryfront == CategoryFront.id)).where(ft & (CategoryFront.type=='2') & (Product.is_pass==1)).order_by(Product.orders).limit(10)
        qcfw_recommend = ProductStandard.select(ProductStandard, Product).join(Product, on=(ProductStandard.product == Product.id)).\
            join(CategoryFront, on=(Product.categoryfront == CategoryFront.id)).where(ft & (CategoryFront.type=='2') & (Product.is_recommend == 1) & (Product.is_pass==1)).order_by(Product.orders).limit(10)
        qcfw_bargain = ProductStandard.select(ProductStandard, Product).join(Product, on=(ProductStandard.product == Product.id)).\
            join(CategoryFront, on=(Product.categoryfront == CategoryFront.id)).where(ft & (CategoryFront.type=='2') & (Product.is_bargain == 2) & (Product.is_pass==1)).order_by(Product.orders).limit(10)

        store_list = Store.select().where((Store.check_state == 1) & (Store.area_code % code)).order_by(Store.clicks.desc()).limit(10)
        store_recommend = Store.select().where((Store.check_state == 1) & (Store.area_code % code) & (Store.is_recommend == 1)).order_by(Store.clicks.desc()).limit(10)
        store_date = Store.select().where((Store.check_state == 1) & (Store.area_code % code)).order_by(Store.created.desc()).limit(10)

        banner1 = Ad.select().where(Ad.atype == 1).order_by(Ad.sort.desc()).limit(5)
        banner2 = Ad.select().where(Ad.atype == 2).order_by(Ad.sort.desc()).limit(9)

        category1 = CategoryFront.select().where((CategoryFront.type == 1) & (CategoryFront.isactive == 1) & (db.fn.Length(CategoryFront.code) == 12)).limit(30)
        category2 = CategoryFront.select().where((CategoryFront.type == 2) & (CategoryFront.isactive == 1) & (db.fn.Length(CategoryFront.code) == 12)).limit(30)

        area = Area.select().where(Area.pid == city_id)
        recommend = ProductStandard.select().join(Product, on=(Product.id == ProductStandard.product)).\
            where((Product.attribute == 2) & (Product.is_pass==1)).order_by(Product.updatedtime.desc()).limit(6)
        news = MediaNews.select().order_by(MediaNews.sort.desc()).limit(4)
        self.render("site/index.html", show_menu=1, cnxh=cnxh_list, qcpj=qcpj_list, qcfw=qcfw_list, stores=store_list,
                    banner1=banner1,banner=enumerate(banner1), banner2=banner2, category1=category1, category2=category2, area=area, recommend=recommend,
                    store_recommend=store_recommend, store_date=store_date, qcpj_recommend=qcpj_recommend, qcpj_bargain=qcpj_bargain,
                    qcfw_recommend=qcfw_recommend, qcfw_bargain=qcfw_bargain, news=news)

@route(r'/signin', name='signin')  #登录
class SignInHandler(BaseWithCityHandler):
    def get(self):
        if self.get_current_user():
            self.redirect("/")
            return

        oauth = None
        if 'oauth' in self.session:
            oauth = self.session['oauth']

        self.render("site/sigin.html", oauth=oauth, next=self.next_url)

    def post(self):
        if self.get_current_user():
            self.redirect("/")
            return

        mobile = self.get_argument("mobile", None)
        password = self.get_argument("password", None)

        if mobile and password:
            try:
                users = User.select().where(User.username == mobile)
                if users.count() > 0:
                    user = users[0]
                    if user.check_password(password):
                        if user.isactive > 0:
                            user.updatesignin()

                            self.session['user'] = user

                            if 'oauth' in self.session:
                                oauth = self.session['oauth']

                                o = Oauth()
                                o.uid = user.id
                                o.openid = oauth['id']
                                o.src = oauth['src']
                                o.save()

                                del self.session['oauth']

                            self.session.save()

                            self.redirect(self.next_url)
                            return
                        else:
                            self.flash("此账户被禁止登录，请联系管理员。")
                    else:
                        self.flash("密码错误")
                else:
                    self.flash("此用户不存在")
            except Exception, ex:
                #logging.error(ex)
                self.flash("此用户不存在")
        else:
            self.flash("请输入用户名或者密码")

        self.render("site/sigin.html", next=self.next_url)


@route(r'/signout', name='signout')  #退出
class SignOutHandler(BaseWithCityHandler):
    def get(self):
        if "user" in self.session:
            del self.session["user"]
            self.session.save()
        self.redirect(self.next_url)


@route(r'/signup', name='signup')  #注册
class SignUpHandler(BaseWithCityHandler):
    def get(self):
        if self.get_current_user():
            self.redirect("/")
            return
        mobile = self.get_argument("mobile", None)
        c = self.get_argument("c", None)
        oauth = None
        promote_user = ''
        try:
            if 'oauth' in self.session:
                oauth = self.session['oauth']
            if c:
                promote_user = base64.decodestring(c)
        except:
            pass
        self.render("site/sigup.html", oauth=oauth, mobile=mobile, pu=promote_user)

    def post(self):
        if self.get_current_user():
            self.redirect("/")
            return

        mobile = self.get_argument("mobile", None)
        password = self.get_argument("password", None)
        apassword = self.get_argument("apassword", None)
        vcode = self.get_argument("vcode", None)
        nextUrl = self.get_argument("next_url", '/')
        promote = self.get_argument("promote", None)
        user_type = self.get_argument("user_type", '0')

        user = User()
        user.username = mobile
        user.password = User.create_password(password)
        try:
            user.validate()

            if password and apassword:
                if promote:
                    if promote == mobile:
                        self.flash("推荐人不能填写自己！")
                        self.render("site/sigup.html", mobile=mobile, pu=promote)
                        return
                    users = User.select().where(User.mobile == promote)
                    if users.count() < 1:
                        self.flash("推荐人不存在！")
                        self.render("site/sigup.html", mobile=mobile, pu=promote)
                        return

                if len(password) < 6:
                    self.flash("请确认输入6位以上新密码")
                elif password != apassword:
                    self.flash("请确认新密码和重复密码一致")
                else:
                    if UserVcode.select().where((UserVcode.mobile == mobile) & (UserVcode.vcode == vcode) & (
                                UserVcode.flag == 0)).count() > 0:
                        now = int(time.time())
                        signupeddate = time.strftime('%Y-%m-%d', time.localtime(now))
                        signupedtime = time.strftime('%H:%M:%S', time.localtime(now))
                        user = User.create(username=user.username, password=user.password, mobile=user.mobile,
                                           signuped=now, lsignined=now, phoneactived=0, signupeddate=signupeddate,
                                           signupedtime=signupedtime)   # , grade=user_type

                        if 'oauth' in self.session:
                            oauth = self.session['oauth']
                            o = Oauth()
                            o.uid = user.id
                            o.openid = oauth['id']
                            o.src = oauth['src']
                            o.save()

                            del self.session['oauth']
                            self.session.save()
                        try:
                            admins = AdminUser.select()
                            receivers = [n.email for n in admins if len(n.email)>0]
                            email = {u'receiver': receivers, u'subject':u'网站新用户注册提醒',u'body': u"有新用户注册车装甲；注册名为：" + user.username}
                            #create_msg(simplejson.dumps(email), 'email')
                        except Exception, e:
                            print e
                        self.session['user']=user
                        self.session.save()

                        # 取消老推新送优惠券功能。
                        #old_new_user_coupon(promote, user)
                        # 老推新注册送抽奖机会
                        old_new_user_raffle(promote, user)
                        # 新用户注册即送10元账户余额
                        new_user_balance(user)

                        next_url = '/' # ?n=frist tornado.escape.url_unescape(nextUrl)
                        self.redirect(next_url)
                        return
                    else:
                        self.flash("请输入正确的验证码")
            else:
                self.flash("请输入密码和确认密码")
        except Exception, ex:
            self.flash(str(ex))
        self.render("site/sigup.html", mobile=mobile)


@route(r'/help/about', name='help_about')  # 帮助 - 关于我们
class LogoutHandler(BaseWithCityHandler):
    def get(self):
        self.render('site/help/about.html')


@route(r'/help/member', name='help_member')  # 帮助 - 会员说明
class LogoutHandler(BaseWithCityHandler):
    def get(self):
        self.render('site/help/member.html')


@route(r'/help/service', name='help_service')  # 帮助 - 售后服务
class LogoutHandler(BaseWithCityHandler):
    def get(self):
        self.render('site/help/service.html')


@route(r'/help/pay', name='help_pay')  # 帮助 - 支付方式
class LogoutHandler(BaseWithCityHandler):
    def get(self):
        self.render('site/help/pay.html')


@route(r'/help/delivery', name='help_delivery')  # 帮助 - 配送范围
class LogoutHandler(BaseWithCityHandler):
    def get(self):
        self.render('site/help/delivery.html')


@route(r'/help/shopping', name='help_shopping')  # 帮助 - 购物指南
class LogoutHandler(BaseWithCityHandler):
    def get(self):
        self.render('site/help/shopping.html')


@route(r'/product/(\d+)', name='product_detail')  # 产品详情
class ProductHandler(BaseWithCityHandler):
    def get(self, psid):
        flag = -1  # 产品状态：-1 不是秒杀产品 0未开始，1正在进行，2已结束
        datetime = int(time.time())
        pa = Product_Activity.select(Product_Activity,(Product_Activity.begin_time - datetime).alias('begin_count'),
                                     (Product_Activity.end_time - datetime).alias('end_count')).\
            where((Product_Activity.status == 1) & (Product_Activity.product_standard == psid) & (Product_Activity.type == 1)).\
            order_by(Product_Activity.end_time.desc())

        quantity = 0
        if pa.count() > 0:
            quantity = self.application.session_store.get_session('psid_'+ str(pa[0].product_standard.id),None)
            if (datetime >= pa[0].begin_time) and (quantity > 0) and (datetime < pa[0].end_time):
                flag = 1
            elif datetime > pa[0].begin_time or quantity <= 0:
                flag = 2
            elif datetime < pa[0].begin_time:
                flag = 0
        ps = ProductStandard.select().where(ProductStandard.id == psid)
        if ps.count() == 0:
            self.set_status(404)
            return self.render('site/404.html')
        else:
            ps = ps[0]
            if flag == 1:
                p = pa[0].product
                pics2 = p.pics
                ca = p.sku[0:2] + '%'
            else:
                p = ps.product
                pics2 = p.pics
                ca = p.sku[0:2] + '%'

            p.prompt = p.prompt.replace("；", "；</br>")
            p.prompt = p.prompt.replace(";", ";</br>")

            list = simplejson.loads(ps.relations)
            pslist = ProductStandard.select().where(ProductStandard.id << list)
            standards = []
            for idx, val in enumerate(list):
                for n in pslist:
                    if n.id == val and (n.product.status == 1):
                        standards.append(n)
                        break

            populars = Product.select().where((Product.sku % ca) & (Product.id != p.id ) & (Product.status == 1 )). \
            order_by(Product.orders.desc()).paginate(1, 5).aggregate_rows()
            pics = [ProductPic(path=p.cover)] + [n for n in pics2 if not n.path == p.cover]
            fav = False
            if self.current_user:
                q = Fav.select().where((Fav.product == p.id) & (Fav.user == self.current_user.id))
                if q.count() > 0:
                    fav = True

                self.create_browse(psid, p.id, p.categoryfront.id)
            # comments = []
            # for n in pslist:
            #     comment = Comment.select().where((Comment.product == n.product.id) & ((Comment.status == 1) | (Comment.status == 2)))
            #     for c in comment:
            #         comments.append(c)
            comments = Comment.select().where((Comment.product == n.product.id) & ((Comment.status == 1) | (Comment.status == 2)))
            page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
            pagesize = self.settings['admin_pagesize']
            total = comments.count()
            if total % pagesize > 0:
                totalpage = total / pagesize + 1
            else:
                totalpage = total / pagesize
            cs = comments.order_by(Comment.created.desc()).paginate(page, pagesize)

            pr = None
            if p.is_reserve == 1:
                prs = Product_Reserve.select().where(Product_Reserve.product_standard == psid)
                if prs.count() > 0:
                   pr = prs[0]
            self.render('site/product.html', p=p, pics=pics, populars=populars, standards=standards, ps=ps, fav=fav,
                        comments=cs, total=total, page=page, pagesize=pagesize,totalpage=totalpage, flag=flag, pa=pa,
                        quantity=quantity, pr=pr)

    def create_browse(self, psid, pid, cfid):
        # 判断用户浏览记录表中是否存在该商品
        ub_exist = User_Browse().select().where((User_Browse.user == self.current_user.id) & (User_Browse.product == pid))
        if ub_exist.count() > 0:
            pass
        else:
            # 创建用户浏览记录
            ub = User_Browse()
            ub.user = self.current_user.id
            ub.product = pid
            ub.product_standard = psid
            ub.category_front = cfid
            ub.created = int(time.time())
            ub.save()
            # 如何该用户浏览记录大于5条，按队列顺序删除超出的数据
            ub_count = User_Browse.select().where(User_Browse.user == self.current_user.id)
            if ub_count.count() > 5:
                del_count = ub_count.count() - 5
                del_ub = User_Browse.select().where(User_Browse.user == self.current_user.id).order_by(User_Browse.created).limit(del_count)
                del_id = [n.id for n in del_ub]
                User_Browse.delete().where(User_Browse.id << del_id).execute()


@route(r'/need', name='need')  # 每日必需
class NeedHandler(BaseWithCityHandler):
    def get(self):
        nlist = simplejson.loads(PageBlock.select().where(PageBlock.key == 'needflist')[0].content)
        nflist = ProductStandard.select(ProductStandard, Product).join(Product). \
            where((ProductStandard.id << nlist) & (Product.status == 1))
        resultflist = []
        for idx, val in enumerate(nlist):
            for n in nflist:
                if n.id == val:
                    resultflist.append(n)
                    break

        nlist2 = simplejson.loads(PageBlock.select().where(PageBlock.key == 'needvlist')[0].content)
        nvlist = ProductStandard.select(ProductStandard, Product).join(Product). \
            where((ProductStandard.id << nlist2) & (Product.status == 1))
        resultvlist = []
        for idx, val in enumerate(nlist2):
            for n in nvlist:
                if n.id == val:
                    resultvlist.append(n)
                    break
        self.render("site/need.html", nflist=resultflist, nvlist=resultvlist)


@route(r'/forgotpassword', name='forgotpassword')  # 找回密码
class ForgotpasswordHandler(BaseWithCityHandler):
    def get(self):
        mobile = self.get_argument("mobile", '')
        self.render('site/forgotpassword.html', mobile=mobile)

    def post(self):
        mobile = self.get_argument("mobile", '')
        vcode = self.get_argument("vcode", None)
        if (not mobile == '') and vcode:
            if UserVcode.select().where((UserVcode.mobile == mobile) & (UserVcode.vcode == vcode) & (
                        UserVcode.flag == 1)).count() > 0:
                self.set_secure_cookie('mobile', mobile, expires_days=1)
                self.render('site/resetpassword.html', mobile=mobile)
            else:
                self.flash("请输入正确的验证码")
                self.render('site/forgotpassword.html', mobile=mobile)
        else:
            self.flash("请输入电话号码和验证码")
            self.render('site/forgotpassword.html', mobile=mobile)


@route(r'/resetpassword', name='resetpassword')  # 重置密码
class ResetpasswordHandler(BaseWithCityHandler):
    def post(self):
        password = self.get_argument("password", None)
        apassword = self.get_argument("apassword", None)
        mobile = self.get_secure_cookie('mobile', None)
        if mobile and password and apassword and (password == apassword):
            user = User.select().where(User.username == mobile)[0]
            user.password = User.create_password(password)
            user.save()
            self.clear_cookie('mobile')
            self.flash('密码修改成功，请登录')
            self.redirect('/signin')
        else:
            self.flash('两次密码输入不一致')
            self.render('site/resetpassword.html', mobile=mobile)


@route(r'/category/(\d+)', name='category')  #分类列表
class CategoryHandler(BaseWithCityHandler):
    def get(self, cid):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        cid = str(cid).rjust(4, '0')
        cc_cid = str(cid).rjust(4, '0')
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", None)
        orderby = self.get_argument("orderby", None)
        desc = int(self.get_argument("desc", 1))
        count = 0
        current_category = ''

        city_id = self.get_secure_cookie("city_id")
        city_code = self.get_secure_cookie("city_code")
        brand_code = self.get_secure_cookie("brand_code")
        code = city_code + '%'

        ft = (Product.status == 1) & (Product.is_pass == 1)
        if city_code:
            ft = ft & (Product.area_code % code)
        if brand_code:
            ft = ft & ((Product.brand_code == brand_code)| (Product.brand_code=='0'))
        c_cid = ''
        if cid != '0000':
            try:
                current_category = CategoryFront.get(CategoryFront.code == cid.replace('%', ''))
            except Exception, e:
                self.redirect('/category/0')
            if len(cid) > 4:
                c_cid = cid[0:8]
            else:
                c_cid = cid
            child_cid = cid[0:4] + '%'
            cid = cid + '%'
            cid = cid.replace('%%', '%')
            ft = ft & (CategoryFront.code % cid)
        else:
            child_cid = '0001%'
        if keyword:
            key = '%' + keyword + '%'
            ft = ft & (Product.name % key)

            hs = Hot_Search.select().where(Hot_Search.keywords == keyword).limit(1)
            if hs.count() > 0:
                hs[0].quantity += 1
                hs[0].last_time = int(time.time())
                hs[0].save()
            else:
                hot = Hot_Search()
                hot.keywords = keyword
                hot.quantity = 1
                hot.status = 0
                hot.last_time = int(time.time())
                hot.save()

        q = ProductStandard.select(ProductStandard, Product).join(Product,
                                                                  on=(ProductStandard.id == Product.defaultstandard)). \
            join(CategoryFront, on=(Product.categoryfront == CategoryFront.id)).where(ft & (ProductStandard.is_show == 1))
        total = q.count()

        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize

        if not orderby:
            orderby = 'orders'

        if desc == 1:
            if orderby == 'orders':
                ps = q.order_by(Product.orders.desc()).paginate(page, pagesize)
            elif orderby == 'views':
                ps = q.order_by(Product.views.desc()).paginate(page, pagesize)
            elif orderby == 'price':
                ps = q.order_by(ProductStandard.price.desc()).paginate(page, pagesize)
            else:
                ps = q.order_by(Product.orders.desc()).paginate(page, pagesize)
        else:
            if orderby == 'orders':
                ps = q.order_by(Product.orders).paginate(page, pagesize)
            elif orderby == 'views':
                ps = q.order_by(Product.views).paginate(page, pagesize)
            elif orderby == 'price':
                ps = q.order_by(ProductStandard.price).paginate(page, pagesize)
            else:
                ps = q.order_by(Product.orders).paginate(page, pagesize)
        child = CategoryFront.select(CategoryFront.name,CategoryFront.code).where((db.fn.Length(CategoryFront.code) == 8)
                    & CategoryFront.code % child_cid).group_by(CategoryFront.name,CategoryFront.code).order_by(CategoryFront.code)

        ccid = c_cid + '%'
        ccid = ccid.replace('%%', '%')
        p = ProductStandard.select(ProductStandard, Product).join(Product,
                                                                  on=(ProductStandard.id == Product.defaultstandard) & (Product.status == 1 )). \
            join(CategoryFront, on=(Product.categoryfront == CategoryFront.id)).where(CategoryFront.code % ccid)
        hot = p.order_by(Product.orders.desc()).limit(5)

        child_category = CategoryFront.select(CategoryFront.name,CategoryFront.code).join(Product,on=(Product.categoryfront == CategoryFront.id)).where((db.fn.Length(CategoryFront.code) == 12) & (CategoryFront.code % ccid) & (Product.status == 1)).group_by(CategoryFront.name,CategoryFront.code).order_by(CategoryFront.code).limit(20)

        cid = cid.replace('%', '')
        self.render('site/category.html', standards=enumerate(ps), total=total, page=page, pagesize=pagesize,
                    cid=(cid if cid else ''),
                    totalpage=totalpage, keyword=(keyword if keyword else ''), orderby=orderby, desc=desc,child=child,
                    hot=hot,child_category=child_category,c_cid=c_cid,cc_cid=cc_cid,current_category=current_category)


@route(r'/qianggou', name='qianggou')  #抢购
class QiangGouHandler(BaseWithCityHandler):
    def get(self):
        self.render('site/qianggou.html')


@route(r'/mobileclient', name='mobileclient')  #手机客户端介绍
class MobileClientHandler(BaseWithCityHandler):
    def get(self):
        self.render('site/mobileclient.html')


@route(r'/discuss', name='discuss')  #用户反馈
class DiscussHandler(BaseWithCityHandler):
    def get(self):
        self.render('site/duoshuo.html')

@route(r'/oauth/api', name='oauth_api')  #Oauth认证
class OauthApiHandler(BaseWithCityHandler):
    def get(self):
        self.render('site/api.html')


@route(r'/act/test', name='act_test')  #活动测试页
class ActTestHandler(BaseWithCityHandler):
    def get(self):
        self.render('site/act/test.html')

@route(r'/invite_friends', name='invite_friends')  #老推新活动页
class InviteFriendsHandler(BaseWithCityHandler):
    def get(self):
        self.render('activity/invite_friends.html')

@route(r'/select_city', name='select_city')  # 选择城市
class SelectCityHandler(BaseWithCityHandler):
    def get(self):
        items = Area.select().where((Area.pid==0) & (Area.is_delete == 0) & (Area.is_site == 1)).order_by(Area.spell,Area.sort)
        items_recommend = Area.select().where((Area.pid!=0) & (Area.is_delete == 0) & (Area.is_site == 1)).order_by(Area.sort).limit(10)
        items_spell = Area.select().where((Area.pid!=0) & (Area.is_delete == 0) & (Area.is_site == 1)).order_by(Area.spell)
        list_spell=[]
        if items_spell:
            first_spell = ""
            last_first_spell = "_"
            spell_count=-1
            for item in items_spell:
                first_spell = item.spell[0]
                if first_spell == last_first_spell:
                    list_spell[spell_count]["citys"].append({
                        "id":item.id,
                        "code":item.code,
                        "name":item.name
                    })
                else:
                    spell_count = spell_count + 1
                    list_spell.append({
                        "first":first_spell,
                        "citys":[]
                    })
                    list_spell[spell_count]["citys"].append({
                        "id":item.id,
                        "code":item.code,
                        "name":item.name
                    })
                last_first_spell = first_spell
        self.render('site/select_city.html', items=items, items_recommend=items_recommend, list_spell=list_spell, is_select_city=1)

    def post(self):
        city_id = self.get_argument("city_id",None)
        if city_id:
            city = Area.get(Area.id==int(city_id))
            self.set_secure_cookie("city_id",city_id, expires_days=1000)
            self.set_secure_cookie("city_code",city.code, expires_days=1000)
            self.set_secure_cookie("city_name",city.name, expires_days=1000)
            self.redirect("/")

@route(r'/set_cookie', name='set_cookie')  # 设置cookie
class SelectCityHandler(BaseWithCityHandler):
    def post(self):
        set_type = int(self.get_argument("set_type",-1))
        if set_type==0: #
            brand_code = self.get_argument("brand_code", None)
            brand_name = self.get_argument("brand_name", None)
            brand_image = self.get_argument("brand_image", None)
            url = self.get_argument("url",None)
            self.set_secure_cookie("brand_code", brand_code, expires_days=1000)
            self.set_secure_cookie("brand_name", brand_name, expires_days=1000)
            self.set_secure_cookie("brand_image", brand_image, expires_days=1000)
            if url:
                self.redirect(url)

@route(r'/topup_activity', name='topup_activity')  #充值返利活动页
class TopUpActivityHandler(BaseWithCityHandler):
    def get(self):
        self.render('activity/topup_activity.html')


@route(r'/invite_friends_mobile', name='invite_friends_mobile')  #老推新活动页
class InviteFriendsHandler(BaseWithCityHandler):
    def get(self):
        self.render('activity/invite_friends_mobile.html')

@route(r'/topup_activity_mobile', name='topup_activity_mobile')  #充值返利活动页
class TopUpActivityHandler(BaseWithCityHandler):
    def get(self):
        self.render('activity/topup_activity_mobile.html')

@route(r'/lucky_draw', name='lucky_draw')  #幸运抽奖活动页
class LuckyDrawHandler(BaseWithCityHandler):
    def get(self):
        urs = User_Raffle_Log.select().where(User_Raffle_Log.draw_level < 10).order_by(User_Raffle_Log.created.desc()).limit(50)
        self.render('activity/lucky_draw.html', urs=urs)

@route(r'/lucky_draw_mobile', name='lucky_draw_mobile')  #幸运抽奖活动页
class LuckyDrawMobileHandler(BaseWithCityHandler):
    def get(self):
        urs = User_Raffle_Log.select().where(User_Raffle_Log.draw_level < 10).order_by(User_Raffle_Log.created.desc()).limit(50)
        self.render('activity/lucky_draw_mobile.html', urs=urs)

@route(r'/prize_list', name='prize_list')  # 获奖信息
class PrizeListHandler(BaseWithCityHandler):
    def get(self):
        urs = User_Raffle_Log.select().where(User_Raffle_Log.user == self.current_user)
        self.render('activity/prize_list.html', urs=urs)

@route(r'/gift', name='gift')  # 首单礼赠送
class GiftHandler(BaseWithCityHandler):
    def get(self):
        self.render('activity/check_gift.html')
    def post(self):
        mobile = self.get_argument("mobile", None)
        msg = ''
        u = None
        if mobile:
            try:
                u = User.get(User.username == mobile)
            except Exception, ex:
                msg = u'用户信息不存在！'
        else:
            msg = u'请输入手机号码'
        self.flash(msg)
        self.render('activity/check_gift.html', u=u)

@route(r'/help/media', name='help_media')  # 帮助 - 媒体报道
class HelpMediaHandler(BaseWithCityHandler):
    def get(self):
        madias = MediaNews.select().order_by(MediaNews.sort.desc())
        self.render('site/help/media.html', madias=madias)

@route(r'/yuding', name='yuding')  # 商品预定
class HelpMediaHandler(BaseWithCityHandler):
    def get(self):
        # begindate = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 0:0:0"), "%Y-%m-%d 0:0:0")))
        # enddate = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 23:59:59"), "%Y-%m-%d 23:59:59")))
        datetime = int(time.time())
        pr = Product_Reserve.select(Product_Reserve,(Product_Reserve.end_time - datetime).alias('begin_count')).\
            where(Product_Reserve.status == 1).order_by(Product_Reserve.id.desc())
        i = 0
        for p in pr:
            i = i + 1
            p.quantity_stage2  = i
        prs = Product_Reserve.select(Product_Reserve).\
            where((Product_Reserve.status != 1) & (Product_Reserve.end_time < datetime)).order_by(Product_Reserve.id.desc())

        self.render('site/reserve.html', pr=pr,prs=prs, datetime=datetime)

@route(r'/huangou', name='huangou')  # 积分换购
class JiFenHuangGouHandler(BaseWithCityHandler):
    def get(self):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", None)
        orderby = self.get_argument("orderby", None)
        desc = int(self.get_argument("desc", 1))
        ft = (Product.status == 1)
        c_cid= ''

        child_cid = '02%'

        q = ProductStandard.select(ProductStandard, Product).join(Product,
                            on=(ProductStandard.id == Product.defaultstandard)).where(ft & (Product.is_score == 1))
        total = q.count()

        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize

        if not orderby:
            orderby = 'orders'

        if desc == 1:
            if orderby == 'orders':
                ps = q.order_by(Product.orders.desc()).paginate(page, pagesize)
            elif orderby == 'views':
                ps = q.order_by(Product.views.desc()).paginate(page, pagesize)
            elif orderby == 'price':
                ps = q.order_by(ProductStandard.price.desc()).paginate(page, pagesize)
            else:
                ps = q.order_by(Product.orders.desc()).paginate(page, pagesize)
        else:
            if orderby == 'orders':
                ps = q.order_by(Product.orders).paginate(page, pagesize)
            elif orderby == 'views':
                ps = q.order_by(Product.views).paginate(page, pagesize)
            elif orderby == 'price':
                ps = q.order_by(ProductStandard.price).paginate(page, pagesize)
            else:
                ps = q.order_by(Product.orders).paginate(page, pagesize)
        child = CategoryFront.select(CategoryFront.name,CategoryFront.code).where((db.fn.Length(CategoryFront.code) == 4)
                    & CategoryFront.code % child_cid).group_by(CategoryFront.name,CategoryFront.code).order_by(CategoryFront.code)

        p = ProductStandard.select(ProductStandard, Product).join(Product,
                                                                  on=(ProductStandard.id == Product.defaultstandard) & (Product.status == 1 ) & (Product.is_score == 1))
        hot = p.order_by(Product.orders.desc()).limit(5)

        self.render('site/huangou.html', standards=enumerate(ps), total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, keyword=(keyword if keyword else ''), orderby=orderby, desc=desc,child=child,
                    hot=hot,c_cid=c_cid)

@route(r'/store', name='store')  # 门店
class StoreHandler(BaseWithCityHandler):
    def get(self):
        client_store = self.get_secure_cookie('store', None)
        if client_store:
            # sid = simplejson.loads(client_store)
            # s = Store.get(Store.id == sid)
            self.redirect("/store/" + client_store)
        else:
            page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
            pagesize = self.settings['admin_pagesize']
            keyword = self.get_argument("keyword", None)
            orderby = self.get_argument("orderby", None)
            desc = int(self.get_argument("desc", 1))
            region = self.get_argument("region", None)
            c_cid= ''

            city_code = self.get_secure_cookie("city_code")
            code = city_code + '%'

            ft = (Store.check_state == 1)   # & (Store.store_type == 0)
            if city_code:
                ft = ft & (Store.area_code % code)
            if region:
                ft = ft & (Store.area_code == region)
            q = Store.select().join(User, on=(User.store==Store.id)).where(ft & (User.grade == 1))
            total = q.count()
            if total % pagesize > 0:
                totalpage = total / pagesize + 1
            else:
                totalpage = total / pagesize

            ps = q.paginate(page, pagesize)
            child = Store.select().join(User, on=(User.store==Store.id)).where((Store.check_state == 1)&(User.grade == 1)).group_by(Store.area_code)

            p = ProductStandard.select(ProductStandard, Product).join(Product,
                                                                      on=(ProductStandard.id == Product.defaultstandard))
            hot = p.order_by(Product.orders.desc()).limit(5)

            self.render('site/store/stores.html', stores=enumerate(ps), total=total, page=page, pagesize=pagesize,
                        totalpage=totalpage, keyword=(keyword if keyword else ''), orderby=orderby, desc=desc,child=child,
                        hot=hot,c_cid=c_cid)

@route(r'/store/(\d+)', name='store_index')  # 门店首页
class StoreIndexHandler(BaseWithCityHandler):
    def get(self, sid):
        if sid == '0':
            self.redirect("/store")
        else:
            ft = (Product.status == 1) & (Product.store == sid)
            ft_near = (Product.status == 1) & (Product.store != sid)
            fts = (Store.check_state == 1) & (Store.id != sid)
            s = Store.get(Store.id == sid)
            sintro = filter_tags(s.intro).replace('\n','<br>')
            products = ProductStandard.select(ProductStandard).join(Product,on=(Product.id==ProductStandard.product)).where(ft).limit(8)
            products_count = products.count()
            near_products = ProductStandard.select().join(Product,on=(Product.id==ProductStandard.product)).where(ft_near).limit(5) # Product.select().where(ft_near).limit(5)
            near_products_count = near_products.count()
            near_stores = Store.select().join(User, on=(User.store == Store.id)).where(fts&(User.grade == 1)).order_by(Store.is_recommend.desc(),Store.credit_score.desc()).limit(5)
            near_stores_count = near_products.count()
            fav_store = False
            if self.current_user:
                q = FavStore.select().where((FavStore.store == sid) & (FavStore.user == self.current_user.id))
                if q.count() > 0:
                    fav_store = True

            categoryfronts = CategoryFront.select().join(Product,on=(CategoryFront.id==Product.categoryfront))\
                .where((Product.store==sid) & (Product.status == 1)).distinct()
            self.render('site/store/store.html', s=s, sid=sid, sintro=sintro, products=products, near_stores=near_stores, near_products=near_products,
                        products_count=products_count, near_products_count=near_products_count, near_stores_count=near_stores_count,
                        categoryfronts=categoryfronts, fav_store=fav_store)

@route(r'/store_news/(\d+)/(\d+)', name='store_news')  # 门店信息列表
class StoreNewsHandler(BaseWithCityHandler):
    def get(self, sid, cid):
        if sid == '0' or cid == '0':
            self.redirect("/store")
        else:
            ft = (Product.status == 1) & (Product.store == sid)
            fts = (StoreNews.status == 1) & (StoreNews.check_state == 1) & (StoreNews.store == sid) & (StoreNews.category == cid)
            s = Store.get(Store.id == sid)
            c = StoreNewsCategory.get(StoreNewsCategory.id == cid)
            products = ProductStandard.select(ProductStandard).join(Product,on=(Product.id==ProductStandard.product)).where(ft).limit(8)
            products_count = products.count()
            news = StoreNews.select().where(fts)
            news_count = news.count()
            self.render('site/store/news.html', s=s, c=c, sid=sid, cid=cid, products=products, news=news,
                        products_count=products_count, news_count=news_count)

@route(r'/store_news_detail/(\d+)', name='store_news_detail')  # 门店信息详细
class StoreNewsDetailHandler(BaseWithCityHandler):
    def get(self, news_id):
        if news_id == '0':
            self.redirect("/store")
        else:
            n = StoreNews.get(StoreNews.id == news_id)
            n.clicks = n.clicks + 1
            n.save()
            ft = (Product.status == 1) & (Product.store == n.store)
            s = Store.get(Store.id == n.store)
            c = StoreNewsCategory.get(StoreNewsCategory.id == n.category)
            products = ProductStandard.select(ProductStandard).join(Product,on=(Product.id==ProductStandard.product)).where(ft).limit(8)
            products_count = products.count()
            self.render('site/store/news_detail.html', s=s, c=c, products=products, n=n,
                        products_count=products_count)

@route(r'/store/map/(\d+)', name='store_map')  # 门店地图页
class StoreMapIndexHandler(BaseWithCityHandler):
    def get(self, sid):
        if sid == '0':
            self.redirect("/store")
        else:
            s = Store.get(Store.id == sid)
            self.render('site/store/map.html', s=s, sid=sid)

@route(r'/store_products/(\d+)', name='store_products')  # 店铺商品列表
class StoreListHandler(BaseWithCityHandler):
    def get(self, sid):
        if sid == '0':
            self.clear_cookie('store')
            self.redirect("/store")
        else:
            page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
            pagesize = self.settings['admin_pagesize']
            keyword = self.get_argument("keyword", None)
            orderby = self.get_argument("orderby", None)
            desc = int(self.get_argument("desc", 1))
            type = self.get_argument("type", None)
            is_bargain = self.get_argument("is_bargain", None)
            ft = (Product.status == 1) & (Product.store == sid)
            if type:
                ft = ft & (Product.category_store == type)
                cid = type + '%'
                cid = cid.replace('%%', '%')
            if keyword:
                key = '%' + keyword + '%'
                ft = ft & (Product.name % key)
            if is_bargain:
                ft = ft & (Product.is_bargain == is_bargain)
            qq = ProductStandard.select(ProductStandard.id.alias('psid'),Product.id.alias('pid'),Product.sku,Product.cover,Product.name,
                                        ProductStandard.name.alias('psname'), Product.prompt,ProductStandard.weight,ProductStandard.price,
                                        Product.orders, Product.views).join(Product,
                                on=(ProductStandard.id == Product.defaultstandard)).where(ft).dicts()
            total = qq.count()

            if total % pagesize > 0:
                totalpage = total / pagesize + 1
            else:
                totalpage = total / pagesize

            if not orderby:
                orderby = 'orders'

            if desc == 1:
                if orderby == 'orders':
                    ps = qq.order_by(Product.orders.desc()).paginate(page, pagesize)
                elif orderby == 'views':
                    ps = qq.order_by(Product.views.desc()).paginate(page, pagesize)
                elif orderby == 'price':
                    ps = qq.order_by(ProductStandard.price.desc()).paginate(page, pagesize)
                else:
                    ps = qq.order_by(Product.orders.desc()).paginate(page, pagesize)
            else:
                if orderby == 'orders':
                    ps = qq.order_by(Product.orders).paginate(page, pagesize)
                elif orderby == 'views':
                    ps = qq.order_by(Product.views).paginate(page, pagesize)
                elif orderby == 'price':
                    ps = qq.order_by(ProductStandard.price).paginate(page, pagesize)
                else:
                    ps = qq.order_by(Product.orders).paginate(page, pagesize)

            list = []
            for n in ps:
                list.append({'psid':n['psid'],'price': n['price'], 'name': n['name'],'cover': n['cover'],'prompt':n['prompt'],
                             'sku': n['sku'],'pid': n['pid'],'orders': n['orders'],'barcode':'0', 'views':n['views'],'psname':n['psname'], 'type':0})

            child = Category_Store.select().where((Category_Store.status == 1) &(Category_Store.store == sid))

            p = ProductStandard.select(ProductStandard, Product).join(Product,
                                                                  on=(ProductStandard.id == Product.defaultstandard) & (Product.status == 1 ))
            hot = p.order_by(Product.orders.desc()).limit(5)

            s = Store.get(Store.id == sid)

            self.render('site/store/store_products.html', standards=enumerate(list), total=total, page=page, pagesize=pagesize,
                        totalpage=totalpage, keyword=(keyword if keyword else ''), orderby=orderby, desc=desc,child=child,
                        hot=hot,s=s,sid=sid)

@route(r'/duanwu', name='duanwu')  # 端午节活动页面
class DuanWuHandler(BaseWithCityHandler):
    def get(self):
        self.render('/activity/duanwu.html')

@route(r'/d', name='d')  # 下载页面
class DHandler(BaseHandler):
    def get(self):
        self.render('/activity/d.html')


@route(r'/store_product/(\d+)', name='store_product_detail')  # 店铺产品详情
class StoreProductHandler(BaseWithCityHandler):
    def get(self, pid):
        client_store = self.get_secure_cookie('store', None)
        ps = ProductStandard.select().where(ProductStandard.product == pid)
        if ps.count() == 0:
            self.set_status(404)
            return self.render('site/404.html')
        else:
            ps = ps[0]
            price = StorePrice.select().where(StorePrice.product_standard == ps.id)
            ps.ourprice = round((price[0].price / 2), 2)
            p = ps.product
            pics2 = p.pics
            ca = p.sku[0:2] + '%'

            list = ProductOffline.select().where((ProductOffline.product == pid) & (ProductOffline.store == int(client_store))
                & (ProductOffline.status == 2)).limit(10)
            standards = []
            for n in list:
                standards.append(n)

            populars = Product.select().where((Product.sku % ca) & (Product.id != p.id ) & (Product.status == 1 )). \
            order_by(Product.orders.desc()).paginate(1, 5).aggregate_rows()
            pics = [ProductPic(path=p.cover)] + [n for n in pics2 if not n.path == p.cover]
            fav = False
            if self.current_user:
                q = Fav.select().where((Fav.product == p.id) & (Fav.user == self.current_user.id))
                if q.count() > 0:
                    fav = True
            comments = Comment.select().where((Comment.product == n.product.id) & ((Comment.status == 1) | (Comment.status == 2)))
            page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
            pagesize = self.settings['admin_pagesize']
            total = comments.count()
            if total % pagesize > 0:
                totalpage = total / pagesize + 1
            else:
                totalpage = total / pagesize
            cs = comments.order_by(Comment.created.desc()).paginate(page, pagesize)

            self.render('site/store/store_product.html', p=p, pics=pics, populars=populars, standards=standards, ps=ps, fav=fav,
                        comments=cs, total=total, page=page, pagesize=pagesize,totalpage=totalpage)

@route(r'/m', name='mobile_index')  # 手机端首页
class MobileIndexHandler(BaseWithCityHandler):
    def get(self):
        self.render('mobile/index.html')

@route(r'/activity/store', name='activity_store')  # 店铺活动页
class ActivityStoreHandler(BaseWithCityHandler):
    def get(self):
        self.render('activity/store.html')

@route(r'/page/(\S+)', name='page')  # 网站单页
class ActivityPageHandler(BaseWithCityHandler):
    def get(self, pid):
        p = Page.select().where(Page.slug == pid)
        if p.count() == 0:
            self.set_status(404)
            return self.render('site/404.html')
        else:
            p = p[0]
        self.render('site/help/page.html', p=p)

@route(r'/news/(\d+)', name='news')  # 新闻详情
class ActivityNewsHandler(BaseWithCityHandler):
    def get(self, nid):
        news = MediaNews.select().where(MediaNews.id == nid)
        if news.count() == 0:
            self.set_status(404)
            return self.render('site/404.html')
        else:
            news = news[0]
        self.render('site/help/news.html', news=news)

@route(r'/youhao', name='car_youhao')  # 汽车油耗
class MobileIndexHandler(BaseWithCityHandler):
    def get(self):
        self.render('site/car_youhao.html')

@route(r'/chedai', name='car_loans')  # 汽车贷款计算
class MobileIndexHandler(BaseWithCityHandler):
    def get(self):
        self.render('site/car_loans.html')