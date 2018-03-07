#!/usr/bin/env python
# coding=utf8

import os
import time
import random
import simplejson
from PIL import Image, ImageFont, ImageDraw
import StringIO
import logging
from lib.mqhelper import create_msg
from lib.util import exportcsv, createpdf, calpriceajax, exportbizcsv, exportorders, exportsku, exportcomment,\
    export_user_csv, export_product_csv, export_price_csv,exportskulist,exportinventoryorders
from handler import BaseHandler, UserBaseHandler
from lib.route import route
from model import UserVcode, Cart, UserAddr, Product, ProductPic, CategoryFront, Order, User, Fav, AdminLog, Invoicing, \
    Coupon, \
    CouponTotal, Balance, Coupon, ProductStandard, DeliveryNumbers, OrderItem, GroupOrder, \
    Score,Inventory, PayBack, InvoicingChanged, AdminUser,UserLevel,\
    User_Raffle_Log,Comment, CouponRealTotal, CouponReal, Gift,Product_Activity,Product_Reserve,Inventory_Store,\
    ProductOffline,Store, Brand, Area, StorePic, Delivery, FavStore, Feedback, Question, CircleTopic, CircleTopicPic, CircleTopicReply, \
    CircleTopicPraise, Settlement, Withdraw
from bootloader import db
from suds.client import Client
import datetime
import urllib
import urllib2
from lib.alipay_return import AlipayReturn
from activity import new_year_send_logic
from activity import new_user_order_coupon
from activity import old_new_user_balance,check_buy_quantity
from lib.imgHelper import GenerateMobileImg
from activity import check_activity
from activity import create_coupon
import tornado.gen
from tornado.concurrent import run_on_executor
# 这个并发库在python3自带在python2需要安装sudo pip install futures
from concurrent.futures import ThreadPoolExecutor
import tornado.web
import jsonpickle
from map import getMinDistanceStore


@route(r'/ajax/upload', name='ajax_upload')  # 上传文件，用于产品内容
class UploadHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def post(self):
        if self.request.files:
            ext = self.request.files["filedata"][0]["filename"].rsplit('.')[-1].lower()

            if ext in ['jpg', 'gif', 'png']:
                # p = Product.get(id=pid)
                filename = '%d%d.%s' % (int(time.time()), random.randint(1000, 9999), ext)
                size = len(self.request.files["filedata"][0]["body"])
                if size<=2*1024*1024:
                    try:
                        user = self.current_user
                        path_dir = 'upload/'  + str(user.id/10000) + '/' + str(user.id)
                        if not os.path.exists('upload/'  + str(user.id/10000)):
                            os.mkdir('upload/'  + str(user.id/10000))
                        if not os.path.exists(path_dir):
                            os.mkdir(path_dir)
                        with open(path_dir + '/' + filename, "wb") as f:
                            f.write(self.request.files["filedata"][0]["body"])

                        # pic = ProductPic.create(product=p, path=filename, isactive=1)
                        msg = '{"err":"","msg":"/' + path_dir + '/' + filename + '"}'
                        homedir = os.getcwd()
                        # oldImgPath = os.path.join(homedir + '/' + path_dir, filename)
                        # GenerateMobileImg(oldImgPath)
                        # if self.settings['syncimg']:
                        #     urls = []
                        #     imgArrr = os.path.splitext(filename)
                        #     outfile = imgArrr[0] + ".mobile.jpg"
                        #     urls.append('http://admin.eofan.com'+'/' + path_dir + '/' + filename)
                        #     urls.append('http://admin.eofan.com'+'/' + path_dir + '/' + outfile)
                        #     create_msg(simplejson.dumps(urls), 'img')
                    except Exception, e:
                        logging.error(e)
                        msg = '{"err":0,"msg":"上传失败"}'
                else:
                    msg = '{"err":0,"msg":"上传图片大小不能超过2M！"}'
            else:
                msg = '{"err":0,"msg":"请上传.jpg,.gif,.png格式图片！"}'
            self.write(msg)

@route(r'/ajax/upload/del', name='ajax_upload_dal')  # 删除上传的文件
class UploadHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def post(self):
        file_path = self.get_argument('file_path', '')
        if file_path:
            try:
                homedir = os.getcwd()
                oldImgPath = os.path.join(homedir +file_path)
                if os.path.exists(oldImgPath):
                    os.remove(oldImgPath)
                msg = '{"err":"","msg":"删除成功！"}'
            except Exception, e:
                logging.error(e)
                msg = '{"err":0,"msg":"上传失败"}'
            self.write(msg)

@route(r'/ajax/product/pic/(\d+)', name='ajax_product_pic')  # 上传产品图片文件
class UploadHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def post(self, pid):
        if self.request.files:
            ext = self.request.files["filedata"][0]["filename"].rsplit('.')[-1].lower()

            if ext in ['jpg', 'gif', 'png']:
                p = Product.get(id=pid)
                filename = '%d%d.%s' % (int(time.time()), random.randint(1000, 9999), ext)
                try:
                    user = self.current_user
                    path_dir = 'upload/'  + str(user.id/10000) + '/' + str(user.id)
                    if not os.path.exists('upload/' + str(user.id/10000)):
                        os.mkdir('upload/'  + str(user.id/10000))
                    if not os.path.exists(path_dir):
                        os.mkdir(path_dir)
                    with open(path_dir + '/' + filename, "wb") as f:
                        f.write(self.request.files["filedata"][0]["body"])

                    pic = ProductPic.create(product=p, path = '/' + path_dir + '/' + filename, isactive=1)
                    msg = '{"id":' + str(pic.id) + ',"path":"/'+ path_dir + '/' + filename + '"}'
                    homedir = os.getcwd()
                    oldImgPath = os.path.join(homedir + '/' + path_dir, filename)
                    GenerateMobileImg(oldImgPath)
                    # if self.settings['syncimg']:
                    #     urls = []
                    #     imgArrr = os.path.splitext(filename)
                    #     outfile = imgArrr[0] + ".mobile.jpg"
                    #     urls.append('http://admin.eofan.com'+'/' + path_dir + '/' + filename)
                    #     urls.append('http://admin.eofan.com'+'/' + path_dir + '/' + outfile)
                    #     create_msg(simplejson.dumps(urls), 'img')
                except Exception, e:
                    logging.error(e)
                    msg = '{"id":0,"path":"上传失败"}'
            self.write(msg)


@route(r'/ajax/circle_topic/pic/(\d+)', name='ajax_circle_topic_pic')  # 上传圈子主题图片文件
class UploadHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def post(self, pid):
        if self.request.files:
            ext = self.request.files["filedata"][0]["filename"].rsplit('.')[-1].lower()

            if ext in ['jpg', 'gif', 'png']:
                p = CircleTopic.get(id=pid)
                filename = '%d%d.%s' % (int(time.time()), random.randint(1000, 9999), ext)
                try:
                    user = self.current_user
                    if p.topic_pics.count() < 9:
                        path_dir = 'upload/'  + str(user.id/10000) + '/' + str(user.id)
                        if not os.path.exists('upload/' + str(user.id/10000)):
                            os.mkdir('upload/'  + str(user.id/10000))
                        if not os.path.exists(path_dir):
                            os.mkdir(path_dir)
                        with open(path_dir + '/' + filename, "wb") as f:
                            f.write(self.request.files["filedata"][0]["body"])

                        pic = CircleTopicPic.create(user=user, topic=p, path = '/' + path_dir + '/' + filename, created=int(time.time()))
                        msg = '{"id":' + str(pic.id) + ',"path":"/'+ path_dir + '/' + filename + '"}'
                        homedir = os.getcwd()
                        oldImgPath = os.path.join(homedir + '/' + path_dir, filename)
                        GenerateMobileImg(oldImgPath)
                        # if self.settings['syncimg']:
                        #     urls = []
                        #     imgArrr = os.path.splitext(filename)
                        #     outfile = imgArrr[0] + ".mobile.jpg"
                        #     urls.append('http://admin.eofan.com'+'/' + path_dir + '/' + filename)
                        #     urls.append('http://admin.eofan.com'+'/' + path_dir + '/' + outfile)
                        #     create_msg(simplejson.dumps(urls), 'img')
                    else:
                        msg = '{"id":0,"path":"晒图最多只能上传9张！"}'
                except Exception, e:
                    logging.error(e)
                    msg = '{"id":0,"path":"上传失败"}'
            self.write(msg)

@route(r'/ajax/store/pic', name='ajax_store_pic')  # 上传门店图片文件
class UploadStorePicHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def post(self):
        if self.request.files:
            ext = self.request.files["filedata"][0]["filename"].rsplit('.')[-1].lower()

            if ext in ['jpg', 'gif', 'png']:
                filename = '%d%d.%s' % (int(time.time()), random.randint(1000, 9999), ext)
                size = len(self.request.files["filedata"][0]["body"])
                if size<=2*1024*1024:
                    try:
                        user = self.current_user
                        store = user.store
                        if store.store_pics.count() < 5:
                            path_dir = 'upload/'  + str(user.id/10000) + '/' + str(user.id)
                            if not os.path.exists('upload/' + str(user.id/10000)):
                                os.mkdir('upload/'  + str(user.id/10000))
                            if not os.path.exists(path_dir):
                                os.mkdir(path_dir)
                            with open(path_dir + '/' + filename, "wb") as f:
                                f.write(self.request.files["filedata"][0]["body"])

                            pic = StorePic.create(store=store, path='/' + path_dir + '/' + filename, check_state=0, is_cover=0, is_active=1)
                            msg = '{"id":' + str(pic.id) + ',"path":"/'+ path_dir + '/' + filename + '"}'
                            homedir = os.getcwd()
                            oldImgPath = os.path.join(homedir + '/' + path_dir, filename)
                            GenerateMobileImg(oldImgPath)
                            # if self.settings['syncimg']:
                            #     urls = []
                            #     imgArrr = os.path.splitext(filename)
                            #     outfile = imgArrr[0] + ".mobile.jpg"
                            #     urls.append('http://admin.eofan.com'+'/' + path_dir + '/' + filename)
                            #     urls.append('http://admin.eofan.com'+'/' + path_dir + '/' + outfile)
                            #     create_msg(simplejson.dumps(urls), 'img')
                        else:
                            msg = '{"id":0,"path":"企业展示图片暂时最多只能上传5张！"}'
                    except Exception, e:
                        logging.error(e)
                        msg = '{"id":0,"path":"上传失败"}'
                else:
                    msg = '{"id":0,"path":"上传图片大小不能超过2M！"}'
            else:
                msg = '{"id":0,"path":"企业展示图片目前只能上传jpg,png,gif图片！"}'
            self.write(msg)

@route(r'/ajax/checkuser', name='ajax_checkuser')  # 检查用户
class CheckuserHandler(BaseHandler):
    def get(self):
        result = {'status': False, 'msg': ''}
        mobile = self.get_argument("mobile")
        try:
            user = User.select().where((User.username == mobile) | (User.mobile == mobile))
            if user.count() > 0:
                result['msg'] = 503  # 已存在
            else:
                UserVcode.delete().where(UserVcode.created < (int(time.time()) - 30 * 60)).execute()
                uservcode = UserVcode()
                uservcode.mobile = mobile
                uservcode.vcode = random.randint(100000, 999999)
                uservcode.created = int(time.time())
                uservcode.flag = 0
                try:
                    uservcode.validate()

                    if UserVcode.select().where(UserVcode.mobile == mobile).count() > 3:
                        result['msg'] = 502  # 连续发三次以上
                    else:
                        try:
                            uservcode.save()
                            result['status'] = True
                            result['msg'] = 0
                            sms = {'mobile': mobile, 'body': u"您登录车装甲的验证码为：" + str(uservcode.vcode), 'isyzm': '1'}
                            create_msg(simplejson.dumps(sms), 'sms')
                        except Exception, ex:
                            logging.error(ex)
                            result['msg'] = 501  # 发送短信异常

                except Exception, ex:
                    logging.error(ex)
                    result['msg'] = 504  # 手机号码无效

        except Exception, e:
            result['msg'] = 505  # 系统异常

        self.write(simplejson.dumps(result))

@route(r'/ajax/bind_alipay/vcode', name='ajax_bind_alipay_vcode')  # 绑定支付宝账号验证码
class BindAlipayVcodeHandler(BaseHandler):
    def post(self):
        result = {'status': False, 'msg': ''}
        u = self.current_user
        if u:
            mobile = u.mobile
            UserVcode.delete().where(UserVcode.created < (int(time.time()) - 30 * 60)).execute()

            uservcode = UserVcode()
            uservcode.mobile = mobile
            uservcode.vcode = random.randint(100000, 999999)
            uservcode.created = int(time.time())
            uservcode.flag = 0
            try:
                uservcode.validate()

                if UserVcode.select().where((UserVcode.mobile == mobile) & (UserVcode.flag == 0)).count() > 3:
                    result['msg'] = "您发送短信过于频繁，请稍后再试"
                else:
                    try:
                        uservcode.save()
                        logging.info("sendmsg:%s - %d" % (mobile, uservcode.vcode))
                        result['status'] = True
                        result['msg'] = '验证码已发送'
                        sms = {'mobile': mobile, 'body': u"您的验证码为：" + str(uservcode.vcode), 'signtype': '1', 'isyzm': '1'}
                        create_msg(simplejson.dumps(sms), 'sms')
                    except Exception, ex:
                        logging.error(ex)
                        result['msg'] = ex.message

            except Exception, ex:
                logging.error(ex)
                result['msg'] = ex.message

        self.write(simplejson.dumps(result))

@route(r'/ajax/bind_alipay', name='ajax_bind_alipay')  # 绑定支付宝账号
class BindAlipayHandler(BaseHandler):
    def post(self):
        result = {'status': False, 'msg': ''}
        u = self.current_user
        alipay_truename = self.get_argument("alipay_truename")
        alipay_account = self.get_argument("alipay_account")
        vcode = self.get_argument("vcode")
        if not alipay_truename:
            result['msg'] = '请输入支付宝账号对应的真实姓名！'
        elif not alipay_account:
            result['msg'] = '请输入支付宝账号！'
        elif u:
            mobile = u.mobile
            try:
                qUserVcode=UserVcode.select().where((UserVcode.mobile == mobile) & (UserVcode.vcode == vcode) & (
                                    UserVcode.flag == 0))
                if qUserVcode.count() > 0:
                    for code in qUserVcode:
                        code.flag = 1
                        code.save()
                    u.alipay_truename = alipay_truename
                    u.alipay_account = alipay_account
                    u.save()
                    #更新用户Session
                    self.session['user'] = u
                    self.session.save()
                    result['status'] = True
                    result['msg'] = '绑定成功！'
                else:
                    result['msg'] = '验证码错误！'
            except Exception, ex:
                logging.error(ex)
                result['msg'] = ex.message
        else:
            result['msg'] = '登录已过期！'
        self.write(simplejson.dumps(result))

@route(r'/ajax/bind_bank', name='ajax_bind_bank')  # 绑定银行卡号
class BindBankHandler(BaseHandler):
    def post(self):
        result = {'status': False, 'msg': ''}
        u = self.current_user
        bank_truename = self.get_argument("bank_truename")
        bank_name = self.get_argument("bank_name")
        bank_branchname = self.get_argument("bank_branchname")
        bank_account = self.get_argument("bank_account")
        vcode = self.get_argument("vcode")
        if not bank_truename:
            result['msg'] = '请输入银行卡对应的真实姓名！'
        elif not bank_name:
            result['msg'] = '请选择银行！'
        elif not bank_branchname:
            result['msg'] = '请输入分支银行！'
        elif not bank_account:
            result['msg'] = '请输入银行卡号！'
        elif u:
            mobile = u.mobile
            try:
                qUserVcode=UserVcode.select().where((UserVcode.mobile == mobile) & (UserVcode.vcode == vcode) & (
                                    UserVcode.flag == 0))
                if qUserVcode.count() > 0:
                    for code in qUserVcode:
                        code.flag = 1
                        code.save()
                    u.bank_truename = bank_truename
                    u.bank_name = bank_name
                    u.bank_branchname = bank_branchname
                    u.bank_account = bank_account
                    u.save()
                    #更新用户Session
                    self.session['user'] = u
                    self.session.save()
                    result['status'] = True
                    result['msg'] = '绑定成功！'
                else:
                    result['msg'] = '验证码错误！'
            except Exception, ex:
                logging.error(ex)
                result['msg'] = ex.message
        else:
            result['msg'] = '登录已过期！'
        self.write(simplejson.dumps(result))

@route(r'/ajax/withdraw', name='ajax_withdraw')  # 提现到支付宝
class WithdrawHandler(BaseHandler):
    def post(self):
        result = {'status': False, 'msg': ''}
        u = self.current_user
        account_type = int(self.get_argument("account_type"))
        sum_money = float(self.get_argument("sum_money"))
        vcode = self.get_argument("vcode")
        if (account_type == 0) and( not u.bank_truename or not u.bank_name or not u.bank_branchname or not u.bank_account):
            result['msg'] = '请先绑定银行卡！'
        elif (account_type == 1) and( not u.alipay_truename or not u.alipay_account):
            result['msg'] = '请先绑定支付宝！'
        elif not sum_money:
            result['msg'] = '请输入要提现的金额！'
        elif sum_money<100 or sum_money>u.cashed_money:
            result['msg'] = '提现金额必须大于100且少于可提现金额！'
        elif u:
            mobile = u.mobile
            try:
                qUserVcode=UserVcode.select().where((UserVcode.mobile == mobile) & (UserVcode.vcode == vcode) & (
                                    UserVcode.flag == 0))
                if qUserVcode.count() > 0:
                    for code in qUserVcode:
                        code.flag = 1
                        code.save()
                    w = Withdraw()
                    w.user = u
                    w.account_type = account_type
                    if account_type == 0:
                        w.account_truename = u.bank_truename
                        w.account_name = u.bank_name
                        w.account_branchname = u.bank_branchname
                        w.account_account = u.bank_account
                    elif account_type == 1:
                        w.account_truename = u.alipay_truename
                        w.account_name = ''
                        w.account_branchname = ""
                        w.account_account = u.alipay_account
                    w.sum_money = sum_money
                    w.status = 0
                    w.apply_time = int(time.time())
                    w.save()
                    u.cashed_money = u.cashed_money - sum_money
                    u.save()
                    #更新用户Session
                    self.session['user'] = u
                    self.session.save()
                    result['status'] = True
                    result['msg'] = '申请提现成功！'
                else:
                    result['msg'] = '验证码错误！'
            except Exception, ex:
                logging.error(ex)
                result['msg'] = ex.message
        else:
            result['msg'] = '登录已过期！'
        self.write(simplejson.dumps(result))

@route(r'/ajax/forget/vcode', name='ajax_forget_vcode')  # 忘记密码手机验证码
class VcodeHandler(BaseHandler):
    def post(self):
        result = {'status': False, 'msg': ''}
        mobile = self.get_argument("mobile", None)
        user = User.select().where(User.username == mobile)
        if user.count() == 0:
            result['msg'] = '您输入的手机号还没有注册'
            self.write(simplejson.dumps(result))
            return

        UserVcode.delete().where(UserVcode.created < (int(time.time()) - 30 * 60)).execute()

        uservcode = UserVcode()
        uservcode.mobile = mobile
        uservcode.vcode = random.randint(100000, 999999)
        uservcode.created = int(time.time())
        uservcode.flag = 1
        try:
            uservcode.validate()

            if UserVcode.select().where((UserVcode.mobile == mobile) & (UserVcode.flag == 1)).count() > 3:
                result['msg'] = 503
            else:
                try:
                    uservcode.save()
                    logging.info("sendmsg:%s - %d" % (mobile, uservcode.vcode))
                    result['status'] = True
                    result['msg'] = '验证码已发送'
                    sms = {'mobile': mobile, 'body': u"您的验证码为：" + str(uservcode.vcode), 'signtype': '1', 'isyzm': '1'}
                    create_msg(simplejson.dumps(sms), 'sms')
                    # client = Client('http://115.29.206.137:8081/MyService.svc?wsdl')
                    #result = client.service.SendSMSYZM('18189279827', u'测试内容123321','1','1')
                except Exception, ex:
                    logging.error(ex)
                    result['msg'] = 500

        except Exception, ex:
            logging.error(ex)
            result['msg'] = 400

        self.write(simplejson.dumps(result))


@route(r'/ajax/captcha', name='ajax_captcha')
class CaptchaHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def get(self):
        img = Image.new('RGB', size=(40, 16), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        captcha = str(random.randint(1000, 9999))
        self.set_cookie("captcha", captcha)

        font = ImageFont.truetype(os.path.join(os.path.dirname(__file__).replace('handler', 'upload'), 'Arial.ttf'), 12)
        for i, s in enumerate(captcha):
            position = (i * 10, 2)
            draw.text(position, s, fill=(0, 0, 0), font=font)

        del draw
        strIO = StringIO.StringIO()
        img.save(strIO, 'png')
        strIO.seek(0)
        self.set_header("Content-Type", "image/png")
        self.write(strIO.read())


@route(r'/ajax/AddAddress', name='ajax_addaddress')  # 添加/修改收货地址
class AddAddressHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def get(self):
        result = {'status': 0, 'msg': 0, 'addAddress': ''}
        user = self.current_user

        addressID = self.get_argument('address_id')
        province = self.get_argument('recipient_province')
        city = self.get_argument('recipient_city')
        region = self.get_argument('recipient_dist')
        street = self.get_argument('street_code')
        address = self.get_argument('recipient_address')
        name = self.get_argument('recipient_name')
        mobile = self.get_argument('recipient_hp')
        tel_area = self.get_argument('recipient_tel_area')
        tel_number = self.get_argument('recipient_tel_number')
        tel_ext = self.get_argument('recipient_tel_ext')

        try:
            if addressID == '0':
                ad = UserAddr()
            else:
                ad = UserAddr.get(UserAddr.id == addressID)
            ad.province = province
            ad.city = city
            ad.region = region
            ad.street = street
            ad.address = address
            ad.name = name
            ad.mobile = mobile
            if (tel_area != '' and tel_number != ''):
                if ( tel_ext != ''):
                    ad.tel = tel_area + '-' + tel_number + '-' + tel_ext
                else:
                    ad.tel = tel_area + '-' + tel_number
            listUserAddrs = UserAddr.select().where((UserAddr.user == user.id) & (UserAddr.isdefault == 1))
            for listUserAddr in listUserAddrs:
                listUserAddr.isdefault = 0
                listUserAddr.save()
            ad.isdefault = 1
            ad.user = user.id
            try:
                ad.save()
                ad.id = ad.id
                adda = jsonpickle.encode(ad)
                result['addAddress'] = adda
                result['status'] = 1
                result['msg'] = 200
            except Exception, ex:
                logging.error(ex)
                result['msg'] = 500
        except:
            result['msg'] = 404
        self.write(simplejson.dumps(result))


@route(r'/ajax/SetAddress', name='ajax_setaddress')  # 添加/修改收货地址
class SetAddressHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def get(self):
        result = 0
        user = self.current_user
        addressID = self.get_argument('addrid')

        if addressID == '':
            pass
        else:
            if user:
                listUserAddrs = UserAddr.select().where((UserAddr.user == user.id) & (UserAddr.isdefault == 1))
                for listUserAddr in listUserAddrs:
                    listUserAddr.isdefault = 0
                    listUserAddr.save()
            ad = UserAddr.get(UserAddr.id == addressID)
            if ad:
                ad.isdefault = 1
                ad.save()
                result = 1
        self.write(simplejson.dumps(result))


@route(r'/ajax/RemoveAddress', name='ajax_removeaddress')  # 删除收货地址
class RemoveAddressHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def post(self):
        result = {'status': 0, 'msg': 0, 'count': 0, 'type': ''}
        user = self.current_user
        addressID = self.get_argument('address_id')
        try:
            isd = False  # 用于标记当前删除数据是否为默认收货地址
            ua = UserAddr.get(UserAddr.id == addressID)
            if ua.isdefault == 1:
                isd = True
            # UserAddr.delete().where(UserAddr.id == addressID).execute()
            userAddr = UserAddr.get(UserAddr.id == addressID)
            userAddr.isactive = 0
            userAddr.save()

            addrs = UserAddr.select().where((UserAddr.user == user.id) and UserAddr.isactive == 1)
            addrCount = len(list(addrs))
            if (addrCount == 0):
                result['type'] = 'unknow_address'
            if isd and addrCount > 0:  # 如果默认收货地址被删除 并且 此用户还有其他收货地址，自动将最后一个添加的地址设为默认
                listUserAddr = UserAddr.select().where((UserAddr.user == user.id) & (UserAddr.isactive == 1))
                for addritem in listUserAddr.order_by(UserAddr.id.desc()):
                    addritem.isdefault = 1
                    addritem.save()
                    break
            result['count'] = addrCount
            result['status'] = 1
            result['msg'] = 200
        except Exception, ex:
            logging.error(ex)
            result['msg'] = 404
        # print result
        self.write(simplejson.dumps(result))


@route(r'/ajax/GetOneAddress', name='ajax_getoneaddress')  # 获取一条收货地址
class GetOneAddressHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def post(self):
        result = {'status': 0, 'msg': 0, 'addAddress': ''}
        user = self.current_user
        addressID = self.get_argument('address_id')
        try:
            addr = UserAddr.get(UserAddr.id == addressID)
            ad = UserAddr()
            ad.province = addr.province
            ad.city = addr.city
            ad.region = addr.region
            ad.street = addr.street
            ad.address = addr.address
            ad.name = addr.name
            ad.mobile = addr.mobile
            ad.tel = addr.tel
            ad.isdefault = addr.isdefault
            ad.user = addr.user
            ad.id = addr.id
            adda = jsonpickle.encode(ad)
            result['addAddress'] = adda
            result['status'] = 1
            result['msg'] = 200
        except Exception, ex:
            logging.error(ex)
            result['msg'] = 404
        print result
        self.write(simplejson.dumps(result))


@route(r'/ajax/category', name='ajax_category')  # post读取产品列表
class CategoryHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def post(self):
        result = {'total': 0, 'pages': 0, 'data': []}
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        cid = int(self.get_argument("cid", 1))
        pagesize = self.settings['admin_pagesize']
        # pagesize = 1
        ft = (Product.status > 0)

        if cid > 0:
            ft = ft & (Product.categoryfront == cid)

        q = Product.select().where(ft)
        total = q.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        result['total'] = total
        result['pages'] = totalpage
        pps = [n for n in q.paginate(page, pagesize).dicts()]
        result['data'] = pps
        # for item in q.paginate(page, pagesize):
        #    result['data'].append(jsonpickle.encode(item))
        self.write(simplejson.dumps(result))


@route(r'/ajax/allcategory', name='ajax_allcategory')  # 获取所有分类
class AllcategoryHandler(BaseHandler):
    def get(self):
        q = [ca for ca in CategoryFront.select().where(CategoryFront.isactive == 1).dicts()]
        self.write(simplejson.dumps(q))


@route(r'/ajax/addCart', name='addCart')  # 将产品加入购物车
class AddCartHandler(BaseHandler):
    def get(self):
        result = 0
        try:
            pid = int(self.get_argument("pid", 1))
            quantity = int(self.get_argument("quantity", 0))
            psid = int(self.get_argument("psid", 1))
            type = int(self.get_argument("type", 0))    # 2表示预售商品
            if quantity > 0:
                if self.current_user:
                    if type == 2:
                        c = {'flag': 0, 'quantity': 0}
                    else:
                        c = check_buy_quantity(pid, self.current_user.id, quantity, 0)
                    if c['flag'] == 0:
                        cart = Cart.select().where((Cart.user == self.current_user.id) & (Cart.product == pid) & (Cart.type != 3))
                        if cart.count() > 0:
                            if type == 2:
                                Cart.delete().where((Cart.user == self.current_user.id) & (Cart.product == pid)).execute()
                                c = Cart()
                                c.user = self.current_user.id
                                c.product = pid
                                c.product_standard = psid
                                c.quantity = quantity
                                c.type = type
                                c.save()
                            else:
                                pa_quantity = self.application.session_store.get_session('psid_'+ str(psid),'')
                                if pa_quantity > 0:
                                    pa = check_activity(pid)
                                else:
                                    pa = None

                                if pa:
                                    cart[0].quantity == 1
                                else:
                                    cart[0].quantity += quantity
                                cart[0].save()
                        else:
                            c = Cart()
                            c.user = self.current_user.id
                            c.product = pid
                            c.product_standard = psid
                            c.quantity = quantity
                            c.type = type
                            c.save()
                    else:
                        result = -2
                else:
                    client_car = self.get_secure_cookie('car', None)
                    carItems = []
                    item = {'pid': pid, 'psid': psid, 'quantity': quantity, 'type': type}
                    if client_car:
                        carItems = simplejson.loads(client_car)
                        products = [n for n in carItems if int(n['pid']) == pid]
                        if len(products) == 1:
                            products[0]['quantity'] = int(products[0]['quantity']) + quantity
                        else:
                            carItems.append(item)
                    else:
                        carItems.append(item)
                    json = simplejson.dumps(carItems)
                    self.set_secure_cookie('car', json, expires_days=100)
                # result = quantity
            else:
                result = -1
        except Exception, ex:
            logging.error(ex)
            result = 0
        self.write(simplejson.dumps(result))


@route(r'/ajax/SaveCookieForCart', name='SaveCookieForCart')  # 将cookie中的信息加入购物车
class SaveCookieForCartHandler(BaseHandler):
    def post(self):
        result = {'pid': False, 'msg': 0}
        try:
            pro = simplejson.loads(self.get_argument("products", '[]'))[0]
            user = self.current_user

            cart = Cart.select().where((Cart.user == user.id) & (Cart.product == pro['PId']))
            if cart.count() > 0:
                cart[0].quantity += int(pro['PAmount'])
                cart[0].save()
            else:
                c = Cart()
                c.user = user.id
                c.product = pro['PId']
                c.product_standard = pro['psid']
                c.quantity = pro['PAmount']
                c.save()
            result['msg'] = 0
            result['pid'] = pro['PId']
            self.current_user.emailactived = 1
            self.session['user'] = self.current_user
            self.session.save()
        except Exception, ex:
            logging.error(ex)
            result['msg'] = 1
        self.write(simplejson.dumps(result))


def OrderChangeStatus(id, status, refund,_self):
    with db.handle.transaction():
        order = Order.get(id=id)
        old_status = order.status
        order.change_status(status)
        if status == 5 and order.payment < 9:  # 需要取消订单，并且不是取消系统补单
            if 5 > old_status > -1:  # 订单原始状态为有效状态，含未支付
                order_item = OrderItem.select().where(OrderItem.order == id)
                for i in order_item:
                    if (i.item_type == 9) or (i.item_type == 3) or (i.item_type == 4) or (i.item_type == 2):
                        gift = Gift.select().where((Gift.status == 1) & (Gift.product == i.product) & (Gift.user == order.user.id)).order_by(Gift.used_time.desc()).limit(1)
                        gift[0].status = 0
                        gift[0].save()
                    if(i.item_type == 1):
                        key = 'psid_' + str(i.product_standard.id)
                        mscount = _self.application.session_store.get_session(key, '')
                        quantity = mscount if mscount else 0
                        _self.application.session_store.set_session(key, quantity+1, None, expiry=24*60*60*5)
                    if(i.item_type == 5) & (old_status == 1):   #订单状态为1 并且属于预定商品，需要减去预定份数
                        pr = Product_Reserve.get(Product_Reserve.product == i.product)
                        pr.quantity -= i.quantity
                        pr.save()
                    if i.product_offline:
                        po = ProductOffline.select().where(ProductOffline.id == i.product_offline.id)
                        if po.count() > 0:
                            po[0].status = 2
                            po[0].save()
                #返还优惠卷
                if order.coupon and old_status != 5:
                    coupon = Coupon.get(id=order.coupon)
                    coupon.status = 1
                    coupon.save()
                if order.pay_balance > 0:  # 货到付款，用余额支付了部分
                    balance = Balance()
                    balance.user = order.user.id
                    balance.balance = order.pay_balance
                    balance.stype = 0
                    balance.log = u'订单取消，返还用户支付费用-订单编号：' + str(order.ordernum)
                    balance.created = int(time.time())
                    balance.save()
                if order.payment == 1 or order.payment == 2 or order.payment == 3:
                    if old_status > 0:  # 原先支付成功的
                        if refund == 1:  # 退到余额
                            balance = Balance()
                            balance.user = order.user.id
                            balance.balance = round(order.currentprice - order.pay_balance, 2)
                            balance.stype = 0
                            balance.log = u'订单取消，返还用户支付费用-订单编号：' + str(order.ordernum)
                            balance.created = int(time.time())
                            if balance.balance > 0:
                                balance.save()
                        elif refund == 0:  # 原路退回
                            if order.payment == 2:  # 使用余额支付
                                balance = Balance()
                                balance.user = order.user.id
                                balance.balance = round(order.currentprice - order.pay_balance, 2)
                                balance.stype = 0
                                balance.log = u'订单取消，返还用户支付费用-订单编号：' + str(order.ordernum)
                                balance.created = int(time.time())
                                if balance.balance > 0:
                                    balance.save()
                            elif order.payment == 1 or order.payment == 3:  # 使用在线支付，创建退款记录

                                paybackprice = float(
                                    order.currentprice - (order.pay_balance if order.pay_balance else 0))
                                pb = PayBack()
                                pb.order = order
                                pb.user = order.user
                                pb.price = paybackprice
                                pb.batch_no = ''
                                pb.trade_no = order.trade_no
                                pb.reason = ''
                                pb.pay_account = order.pay_account
                                pb.back_by = 2
                                pb.status = 0
                                pb.save()
                                admins = AdminUser.select(db.fn.Distinct(AdminUser.email)).where(
                                    (AdminUser.roles % '%F%') | (AdminUser.roles % '%D%')).dicts()
                                receivers = [n['email'] for n in admins if len(n['email']) > 0]
                                msg = u'订单号：' + order.ordernum + u', 需退款' + str(paybackprice) + u'元； 请核实并尽快处理'
                                email = {u'receiver': receivers, u'subject': u'产生取消订单，退款请求', u'body': msg}
                                try:
                                    create_msg(simplejson.dumps(email), 'email')
                                except:
                                    pass
        order.save()
        if status == 4:
            sign_time = int(time.mktime(time.strptime('2015-02-19', "%Y-%m-%d")))
            if order.user.signuped < sign_time:
                start_time = int(time.mktime(time.strptime('2015-03-01', "%Y-%m-%d")))
                end_time = int(time.mktime(time.strptime('2015-03-08', "%Y-%m-%d")))
                if (order.ordered > start_time) & (order.ordered < end_time):
                    b = Balance()
                    b.user = order.user
                    b.balance = round((order.currentprice * 0.1), 2)
                    b.stype = 0
                    b.log = u'老用户返利10%活动，返利金额：' + order.ordernum
                    b.created = int(time.time())
                    b.save()

            if order.payment != 9:
                try:
                    ul=UserLevel.get(levelid=order.user.userlevel)
                    if ul:
                        stype = 0
                        jftype = 0
                        scorenum = int(int(order.price)*ul.xfonescore/100)
                        log = u'订单完成 - 订单编号：%s' % order.ordernum
                        order.user.updatescore(stype, jftype, scorenum, log)
                        if(ul.jlperscore > 0):
                            jftype = 1
                            scorenum = int(scorenum*ul.jlperscore/100)
                            log = u'订单完成奖励积分 - 订单编号：%s' % order.ordernum
                            order.user.updatescore(stype, jftype, scorenum, log)
                except Exception, ex:
                    logging.error(ex)

        # if old_status < 2 and status == 2:  # 改变为正在处理，关联活动
        #     new_year_send_logic(order)
            # 活动结束
            # new_user_order_coupon(order)
        if old_status == 3 and status == 4: #老推新活动，订单标记为已完成时返利
            old_new_user_balance(order)

def OrderChangeStatusStore(id, status, refund, _self):
    with db.handle.transaction():
        order = Order.get(id=id)
        old_status = order.status
        order.status = status
        if status == 5 and order.payment < 9:  # 需要取消订单，并且不是取消系统补单
            if 5 > old_status > -1:  # 订单原始状态为有效状态，含未支付
                order_item = OrderItem.select().where(OrderItem.order == id)
                for i in order_item:
                    if (i.item_type == 9) or (i.item_type == 3) or (i.item_type == 4) or (i.item_type == 2):
                        gift = Gift.select().where((Gift.status == 1) & (Gift.product == i.product) & (Gift.user == order.user.id)).order_by(Gift.used_time.desc()).limit(1)
                        gift[0].status = 0
                        gift[0].save()
                    if(i.item_type == 1):
                        key = 'psid_' + str(i.product_standard.id)
                        mscount = _self.application.session_store.get_session(key, '')
                        quantity = mscount if mscount else 0
                        _self.application.session_store.set_session(key, quantity+1, None, expiry=24*60*60*5)
                    if(i.item_type == 5) & (old_status == 1):   #订单状态为1 并且属于预定商品，需要减去预定份数
                        pr = Product_Reserve.get(Product_Reserve.product == i.product)
                        pr.quantity -= i.quantity
                        pr.save()
                #返还优惠卷
                if order.coupon and old_status != 5:
                    coupon = Coupon.get(id=order.coupon)
                    coupon.status = 1
                    coupon.save()
                if order.pay_balance > 0:  # 货到付款，用余额支付了部分
                    balance = Balance()
                    balance.user = order.user.id
                    balance.balance = order.pay_balance
                    balance.stype = 0
                    balance.log = u'订单取消，返还用户支付费用-订单编号：' + str(order.ordernum)
                    balance.created = int(time.time())
                    balance.save()
                if order.payment == 1 or order.payment == 2 or order.payment == 3:
                    if old_status > 0:  # 原先支付成功的
                        if refund == 1:  # 退到余额
                            balance = Balance()
                            balance.user = order.user.id
                            balance.balance = round(order.currentprice - order.pay_balance, 2)
                            balance.stype = 0
                            balance.log = u'订单取消，返还用户支付费用-订单编号：' + str(order.ordernum)
                            balance.created = int(time.time())
                            if balance.balance > 0:
                                balance.save()
                        elif refund == 0:  # 原路退回
                            if order.payment == 2:  # 使用余额支付
                                balance = Balance()
                                balance.user = order.user.id
                                balance.balance = round(order.currentprice - order.pay_balance, 2)
                                balance.stype = 0
                                balance.log = u'订单取消，返还用户支付费用-订单编号：' + str(order.ordernum)
                                balance.created = int(time.time())
                                if balance.balance > 0:
                                    balance.save()
                            elif order.payment == 1 or order.payment == 3:  # 使用在线支付，创建退款记录

                                paybackprice = float(
                                    order.currentprice - (order.pay_balance if order.pay_balance else 0))
                                pb = PayBack()
                                pb.order = order
                                pb.user = order.user
                                pb.price = paybackprice
                                pb.batch_no = ''
                                pb.trade_no = order.trade_no
                                pb.reason = ''
                                pb.pay_account = order.pay_account
                                pb.back_by = 2
                                pb.status = 0
                                pb.save()
                                admins = AdminUser.select(db.fn.Distinct(AdminUser.email)).where(
                                    (AdminUser.roles % '%F%') | (AdminUser.roles % '%D%')).dicts()
                                receivers = [n['email'] for n in admins if len(n['email']) > 0]
                                msg = u'订单号：' + order.ordernum + u', 需退款' + str(paybackprice) + u'元； 请核实并尽快处理'
                                email = {u'receiver': receivers, u'subject': u'产生取消订单，退款请求', u'body': msg}
                                try:
                                    create_msg(simplejson.dumps(email), 'email')
                                except:
                                    pass
        order.save()
        if status == 4:
            sign_time = int(time.mktime(time.strptime('2015-02-19', "%Y-%m-%d")))
            if order.user.signuped < sign_time:
                start_time = int(time.mktime(time.strptime('2015-03-01', "%Y-%m-%d")))
                end_time = int(time.mktime(time.strptime('2015-03-08', "%Y-%m-%d")))
                if (order.ordered > start_time) & (order.ordered < end_time):
                    b = Balance()
                    b.user = order.user
                    b.balance = round((order.currentprice * 0.1), 2)
                    b.stype = 0
                    b.log = u'老用户返利10%活动，返利金额：' + order.ordernum
                    b.created = int(time.time())
                    b.save()

            if order.payment != 9:
                try:
                    ul=UserLevel.get(levelid=order.user.userlevel)
                    if ul:
                        stype = 0
                        jftype = 0
                        scorenum = int(int(order.price)*ul.xfonescore/100)
                        log = u'订单完成 - 订单编号：%s' % order.ordernum
                        order.user.updatescore(stype, jftype, scorenum, log)
                        if(ul.jlperscore > 0):
                            jftype = 1
                            scorenum = int(scorenum*ul.jlperscore/100)
                            log = u'订单完成奖励积分 - 订单编号：%s' % order.ordernum
                            order.user.updatescore(stype, jftype, scorenum, log)
                except Exception, ex:
                    logging.error(ex)

        if old_status < 2 and status == 2:  # 改变为正在处理，关联活动
            new_year_send_logic(order)
            # 活动结束
            # new_user_order_coupon(order)
        if old_status == 3 and status == 4: #老推新活动，订单标记为已完成时返利
            old_new_user_balance(order)

@route(r'/ajax/order/changestatus', name='ajax_order_changestatus')  # 修改订单状态
class OrderHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        status = int(self.get_argument("status", -2))
        ids = simplejson.loads(self.get_argument("ids", '[]'))
        try:
            for n in ids:
                refund = 0
                OrderChangeStatus(n, status, refund, self)
                order = Order.get(id=n)
                order.lasteditedby = self.get_admin_user()
                order.lasteditedtime = int(time.time())
                order.save()

            content = {}
            content['operatetype'] = '修改订单状态'
            content['orderid'] = ids
            content['status'] = status
            # AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        except Exception, e:
            result['err'] = 1
            result['msg'] = e.message

        self.write(simplejson.dumps(result))

@route(r'/ajax/user/order/changestatus', name='ajax_user_order_changestatus')  # 修改订单状态
class UserOrderHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def options(self):
        pass

    def post(self):
        result = {'err': 0, 'msg': ''}
        status = int(self.get_argument("status", -2))
        id = self.get_argument("id", None)
        refund = int(self.get_argument("refund", 0))  # 0原路退回,1余额
        try:
            if id:
                OrderChangeStatus(id, status, refund, self)
                order = Order.get(id=id)
                usernew = User.get(id=order.user.id)
                self.session['user'] = usernew
                self.session.save()
        except Exception, e:
            result['err'] = 1
            result['msg'] = '操作失败，请稍后再试'

        self.write(simplejson.dumps(result))


@route(r'/mobile/user/order/changestatus', name='mobile_user_order_changestatus')  # 修改订单状态
class UserOrderChangeStatusHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def options(self):
        pass

    def post(self):
        result = {'err': 0, 'msg': ''}
        args = simplejson.loads(self.request.body)
        status = int(args.get("status", -2))
        id = args.get("id", None)
        refund = int(args.get("refund", 0))  # 0原路退回,1余额
        try:
            if id:
                OrderChangeStatus(id, status, refund, self)
                order = Order.get(id=id)
                usernew = User.get(id=order.user.id)
                self.session['user'] = usernew
                self.session.save()
        except Exception, e:
            result['err'] = 1
            result['msg'] = '操作失败，请稍后再试'

        self.write(simplejson.dumps(result))


@route(r'/ajax/removeCar', name='ajax_delcar')  # 删除购物车商品
class RemoveCarHandler(BaseHandler):
    def post(self):
        result = 0
        psid = self.get_argument('psid')
        poid = self.get_argument('poid')
        user = self.current_user
        try:
            if user:
                if poid:
                    Cart.delete().where((Cart.product_offline == poid) & (Cart.user == user.id)).execute()
                    po = ProductOffline.get(ProductOffline.id == poid)
                    po.status = 2
                    po.save()
                else:
                    Cart.delete().where((Cart.product_standard == psid) & (Cart.user == user.id) & (Cart.type != 3)).execute()
            else:
                client_car = self.get_secure_cookie('car', None)
                if client_car:
                    carItems = simplejson.loads(client_car)
                    list = [n for n in carItems if int(n['psid']) == int(psid)]
                    [carItems.remove(n) for n in list]
                    json = simplejson.dumps(carItems)
                    self.set_secure_cookie('car', json, expires_days=100)
            result = 1
        except Exception, ex:
            logging.error(ex)
            result = 0
        self.write(simplejson.dumps(result))


@route(r'/ajax/checkin', name='ajax_checkin')  # 签到
class CheckInHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def get(self):
        result = {'err': 0, 'msg': '', 'seriesnum': 0, 'scorenum': 0, 'totalscore':0, 'totallevel':0}

        try:
            u = self.current_user
            user = User.get(id = u.id)
            result=user.checkin()
            if result['flag'] == 1:
                u = User.get(id = user.id)
                # 签到成功，增加一次抽奖机会
                u.raffle_count  += 1
                u.save()
        except:
            result['flag'] = -1
        self.write(simplejson.dumps(result))

@route(r'/ajax/CartChange', name='ajax_cartchange')  # 更改购物车产品数量
class CartChangeHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def get(self):
        result = {'err': 0, 'msg': ''}
        user = self.current_user
        # if user:
        pid = int(self.get_argument("cid", 0))
        num = int(self.get_argument("count", 1))
        type = int(self.get_argument("type", 1))
        if (pid > 0 and num > 0):
            if type == 1:
                if user:

                    p = Product.select().where(Product.id == pid)
                    p_type = 0
                    if p.count() > 0:
                        p_type = p[0].is_reserve
                    if p_type == 1:
                        c = {'flag': 0, 'quantity': 0}
                    else:
                        c = check_buy_quantity(pid, self.current_user.id, num, 1)
                    if c['flag'] == 0:
                        try:
                            cartitem = Cart.select().where((Cart.product == pid) & (Cart.user == user.id))[0]
                            cartitem.quantity = num
                            try:
                                cartitem.save()
                            except Exception, ex:
                                logging.error(ex)

                            result['err'] = 1
                        except:
                            result['msg'] = '数量修改异常，请刷新后重试！'
                    else:
                        result['err'] = 0
                        result['msg'] = '该商品已超出当日最大可购买数量！'
                else:
                    client_car = self.get_secure_cookie('car', None)
                    if client_car:
                        carItems = simplejson.loads(client_car)
                        list = [n for n in carItems if int(n['pid']) == int(pid)]
                        list[0]['quantity'] = num
                        json = simplejson.dumps(carItems)
                        self.set_secure_cookie('car', json, expires_days=100)
                    result['err'] = 1
            else:
                try:
                    if user:
                        cartitem = Cart.select().where((Cart.product == pid) & (Cart.user == user.id))[0]
                        cartitem.quantity = num
                        try:
                            cartitem.save()
                        except Exception, ex:
                            logging.error(ex)
                    else:
                        client_car = self.get_secure_cookie('car', None)
                        if client_car:
                            carItems = simplejson.loads(client_car)
                            list = [n for n in carItems if int(n['pid']) == int(pid)]
                            list[0]['quantity'] = num
                            json = simplejson.dumps(carItems)
                            self.set_secure_cookie('car', json, expires_days=100)

                    result['err'] = 1
                except:
                    result['msg'] = '数量修改异常，请刷新后重试！'
        else:
            result['err'] = 0
            result['msg'] = '400'
        self.write(simplejson.dumps(result))


@route(r'/ajax/addfav/(\d+)', name='ajax_addfav')  # 添加收藏
class FavAddHandler(UserBaseHandler):
    def get(self, pid):
        result = {'status': False, 'msg': 0}
        q = Fav.select().where((Fav.product == pid) & (Fav.user == self.current_user.id))
        if q.count() == 0:
            Fav.create(user=self.current_user, product=pid)
        result['status'] = True
        self.write(simplejson.dumps(result))

@route(r'/ajax/addfav_store/(\d+)', name='ajax_addfav_store')  # 添加收藏 门店
class FavAddStoreHandler(BaseHandler):
    def get(self, sid):
        result = {'status': False, 'msg': '您还没登录，请先登录！'}
        if self.current_user:
            q = FavStore.select().where((FavStore.store == sid) & (FavStore.user == self.current_user.id))
            if q.count() == 0:
                FavStore.create(user=self.current_user, store=sid, favtime=int(time.time()))
            result['status'] = True
        self.write(simplejson.dumps(result))


@route(r'/ajax/ClearCartAll', name='ajax_clearcartall')  # 清空购物车
class ClearCartAllHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def get(self):
        result = 0
        user = self.current_user
        try:
            if user:
                c = Cart.select().where(Cart.type == 3)
                for n in c:
                    po = ProductOffline.select().where(ProductOffline.id == n.product_offline)
                    if po.count() > 0:
                        po[0].status = 2
                        po[0].save()
                Cart.delete().where(Cart.user == user.id).execute()
                result = 1
            else:
                self.clear_cookie('car')
                result = 1
        except:
            result = 0
        self.write(simplejson.dumps(result))


@route(r'/ajax/order/sending', name='ajax_order_sending')  # 订单发货
class OrderSendingHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        ids = simplejson.loads(self.get_argument("ids", '[]'))
        # did = self.get_argument("did", 1)
        try:
            for n in ids:
                order = Order.get(id=n)
                if order.delivery:
                    order.change_status(3)
                    # order.delivery = did
                    order.delivery_time = int(time.time())
                    order.save()
                    if order.address:
                        if order.address.mobile:
                            try:
                                if order.deliverynum:
                                    sms = {'mobile': order.address.mobile,
                                           'body': u"订单号：" + order.ordernum + u"已发出宅急送单号" + str(order.deliverynum) +
                                                   u"，登录电脑端查看详情。质量投诉请拨" + self.settings['com_tel'],
                                           'signtype': '1', 'isyzm': '1'}
                                else:
                                    sms = {'mobile': order.address.mobile,
                                           'body': u"订单号：" + order.ordernum + u"商品已发出，登录电脑端查看详情。质量投诉请拨" + self.settings[
                                               'com_tel'],
                                           'signtype': '1', 'isyzm': '1'}
                                create_msg(simplejson.dumps(sms), 'sms')
                            except Exception, e:
                                pass
                    '''orderItems = OrderItem.select().where(OrderItem.order == n)
                    for orderItem in orderItems:
                        i = Invoicing()
                        i.type = 1 #0入库，1出库
                        i.product = orderItem.product.id
                        i.quantity = (orderItem.product_standard.weight * orderItem.quantity) / 500
                        i.price = orderItem.product_standard.price * orderItem.quantity
                        i.unitprice =orderItem.product_standard.price
                        i.args = order.ordernum
                        i.addtime = int(time.mktime(time.strptime(time.strftime('%Y-%m-%d',time.localtime(time.time())),"%Y-%m-%d")))
                        i.save()

                        pro = Product.get(id = orderItem.product.id)
                        ps = ProductStandard.get(id=pro.defaultstandard)
                        list = simplejson.loads(ps.relations)
                        pslist = ProductStandard.select().where(ProductStandard.id << list)
                        for n in pslist:
                            p = Product.get(id=n.product.id)
                            p.quantity -= (orderItem.product_standard.weight * orderItem.quantity) / 500
                            p.save()'''
                else:
                    result['err'] = 2
                    result['msg'] = '需要发货的订单中存在未设置物流公司的订单，请检查。'
        except Exception, e:
            result['err'] = 1
            result['msg'] = e.message
        self.write(simplejson.dumps(result))

@route(r'/ajax/order/send', name='ajax_order_send')  # 订单发货
class OrderSendingHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        id = self.get_argument("id", '0')
        num = self.get_argument("num", '')
        did = self.get_argument("did", '1')
        status = int(self.get_argument("status", -2))
        try:
            OrderChangeStatus(id, status, 0, self)
            order = Order.get(id=id)
            order.change_status(3)
            order.delivery = did
            order.deliverynum = num
            order.delivery_time = int(time.time())
            # order.lasteditedby = self.get_admin_user()
            order.lasteditedtime = int(time.time())
            order.save()
            d = Delivery.get(id=did)
            if order.address:
                if order.address.mobile:
                    try:
                        if order.deliverynum:
                            sms = {'mobile': order.address.mobile,
                                   'body': u"订单：" + order.ordernum + u"已由" + d.name + u"发出,单号" + str(order.deliverynum) +
                                           u"，登录电脑端查看详情。质量投诉请拨" + self.settings['com_tel'],
                                   'signtype': '1', 'isyzm': '1'}
                        else:
                            sms = {'mobile': order.address.mobile,
                                   'body': u"订单号：" + order.ordernum + u"商品已发出，登录电脑端查看详情。质量投诉请拨" + self.settings[
                                       'com_tel'],
                                   'signtype': '1', 'isyzm': '1'}
                        create_msg(simplejson.dumps(sms), 'sms')
                    except Exception, e:
                        pass
        except Exception, e:
            result['err'] = 1
            result['msg'] = e.message
        self.write(simplejson.dumps(result))

@route(r'/ajax/pdf/orders', name='ajax_order_pdf')  # 生成order的pdf
class PDFOrderHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        ids = simplejson.loads(self.get_argument("ids", '[]'))
        if len(ids) == 0:
            result['err'] = 1
            result['msg'] = '请至少选择一个订单'
        else:
            try:
                fname = 'orders' + str(time.time()) + '.pdf'
                q = Order.select().where(Order.id << ids)
                count = q.count()
                createpdf(q, fname, count)
                result['msg'] = fname
                for n in q:
                    n.exportpdf = 1
                    n.save()
            except Exception, e:
                result['err'] = 1
                result['msg'] = e.message

        self.write(simplejson.dumps(result))


@route(r'/ajax/library', name='addlibrary')  # 入库管理
class AddLibraryHandler(BaseHandler):
    def get(self):
        result = ''
        purchase = float(self.get_argument("purchase", 0))
        price = float(self.get_argument("price", 0))
        actual = float(self.get_argument("actual", 0))
        kg = self.get_argument("kg", 0)
        id = self.get_argument("id", 0)
        name = self.get_argument("name", 0)
        try:
            invoicing = Invoicing()
            invoicing.actual = actual
            invoicing.price = price
            invoicing.purchase = purchase
            invoicing.unit = kg
            invoicing.created = int(time.time())
            invoicing.categroyid = id
            invoicing.createdby = self.get_admin_user().username
            invoicing.categroyname = name
            invoicing.save()
            result = "添加成功"
        except Exception, ex:
            logging.error(ex)
            result = "添加失败"
        self.write(simplejson.dumps(result))


@route(r'/ajax/editlibrary', name='editlibrary')  # 入库管理--编辑
class EidtLibraryHandler(BaseHandler):
    def get(self):
        result = ''
        purchase = float(self.get_argument("purchase", 0))
        price = float(self.get_argument("price", 0))
        actual = float(self.get_argument("actual", 0))
        kg = self.get_argument("kg", 0)
        cid = self.get_argument("id", 0)
        try:
            invoicing = Invoicing.get(Invoicing.id == cid)
            invoicing.actual = actual
            invoicing.price = price
            invoicing.purchase = purchase
            invoicing.unit = kg
            invoicing.created = int(time.time())
            invoicing.createdby = self.get_admin_user().username
            invoicing.save()
            result = "保存成功"
        except Exception, ex:
            logging.error(ex)
            result = "保存失败"
        self.write(simplejson.dumps(result))


@route(r'/ajax/add_coupon', name='ajax_add_coupon')  # 使用优惠卷
class AddCouponsHandler(BaseHandler):
    def post(self):
        result = {'error': '', 'msg': 'success', 'price': '', 'min': ''}
        code = self.get_argument("code", None)
        try:
            if code:
                p = Coupon.get(Coupon.code == code)
                # p.status = 2
                # p.save()
                result['msg'] = "success"
                result['price'] = p.coupontotal.price
                result['min'] = p.coupontotal.minprice
        except Exception, e:
            result['error'] = e
            result['msg'] = e.message

        self.write(simplejson.dumps(result))


@route(r'/ajax/check_pay', name='ajax_check_pay')  # 检查支付是否成功
class CheckPayHandler(BaseHandler):
    def post(self):
        result = {'result': '', 'ordernum': '', 'orderid': ''}
        user = self.current_user
        oid = self.get_argument("id", '')
        try:
            if oid:
                order = Order.get(id=oid)
            else:
                orders = Order.select().where(Order.user == user.id).order_by(Order.id.desc()).limit(1)
                if orders.count() > 0:
                    order = orders[0]
                else:
                    result['result'] = "failure"
            if order:
                if (order.status == 0):
                    result['result'] = "failure"
                else:
                    result['result'] = "success"
                result['ordernum'] = order.ordernum
                result['orderid'] = order.id
        except Exception, e:
            result['result'] = e.message

        self.write(simplejson.dumps(result))


@route(r'/ajax/analyze', name='ajax_analyze')  # 重新计算价格
class AjaxAnalyzeHandler(BaseHandler):
    def post(self):
        result = {'pid': False, 'msg': 0}
        try:
            f = self.get_argument("f", '')
            cost = eval(self.get_argument("cost", ''))
            weight = float(self.get_argument("weight", '0'))
            price = calpriceajax(cost, f)
            msg = {}
            msg['price'] = str(price) if price else '0'
            msg['preprice'] = str((price / 500.0) * weight) if price else '0'
            result['msg'] = msg
            result['pid'] = True
        except Exception, ex:
            logging.error(ex)
            result['msg'] = 1
        self.write(simplejson.dumps(result))


@route(r'/ajax/changeprice', name='ajax_changeprice')  # 立即改价
class AjaxAnalyzeHandler(BaseHandler):
    def post(self):
        try:
            pid = int(self.get_argument("pid", '0'))
            sid = int(self.get_argument("sid", '0'))
            price = float(self.get_argument("price", '0'))
            preprice = float(self.get_argument("preprice", '0'))
            # marketprice = float(self.get_argument("marketprice", '0'))
            f = self.get_argument("f", '')
            p = Product.get(id=pid)
            now = datetime.datetime.now()

            s = ProductStandard.get(id=sid)
            s.price = preprice
            s.ourprice = price
            #s.orginalprice = marketprice
            s.pricefunction = f
            s.save()
            try:
                InvoicingChanged.delete().where(InvoicingChanged.product == pid).execute()
            except:
                pass
            self.write('修改成功')
        except:
            self.write('修改失败')


@route(r'/ajax/export/orders', name='ajax_export_orders')  # 生成待打印订单数据csv文件
class CSVOrderHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        ids = simplejson.loads(self.get_argument("ids", '[]'))
        company = int(self.get_argument("company", -2))

        if len(ids) == 0:
            result['err'] = 1
            result['msg'] = '请至少选择一个订单'
        else:
            ordernumbers = DeliveryNumbers.select().where((DeliveryNumbers.status == 0) &
                                                          (DeliveryNumbers.delivery == company)).paginate(1, len(ids))
            if (ordernumbers.count() < len(ids)) & (company == 1):
                result['err'] = 1
                result['msg'] = '该物流公司的可用订单号不足，请立即联系物流公司'
            elif (ordernumbers.count() > len(ids)) & (company == 1):
                result['err'] = 1
                result['msg'] = '所选订单号与物流单号对应错误，请联系技术人员'
            else:
                try:
                    fname = 'orders.csv'
                    q = Order.select().where(Order.id << ids)
                    idx = 0
                    dvnum = {}
                    with db.handle.transaction():
                        for o in q:
                            if not o.delivery:
                                if company == 1:
                                    if o.group_orders.count() > 0:
                                        name = o.group_orders[0].name
                                        if dvnum.has_key(name):
                                            o.deliverynum = dvnum[name]
                                        else:
                                            dvnum[name] = ordernumbers[idx].num
                                            o.deliverynum = dvnum[name]
                                            ordernumbers[idx].status = 1
                                            ordernumbers[idx].save()
                                            idx += 1
                                    else:
                                        o.deliverynum = ordernumbers[idx].num
                                        ordernumbers[idx].status = 1
                                        ordernumbers[idx].save()
                                        idx += 1
                                o.delivery = company
                                o.save()

                    exportcsv(q, fname, self.settings['com_tel'])
                    result['msg'] = fname
                except Exception, e:
                    result['err'] = 1
                    result['msg'] = e.message

        self.write(simplejson.dumps(result))


@route(r'/ajax/export/bisorder', name='ajax_export_bisorder')  # 生成业务对接数据csv文件
class BIZCSVOrderHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        ids = simplejson.loads(self.get_argument("ids", '[]'))

        if len(ids) == 0:
            result['err'] = 1
            result['msg'] = '请至少选择一个订单'
        else:
            try:
                fname = 'biz_orders.csv'
                q = Order.select().where(Order.id << ids)
                exportbizcsv(q, fname, self.settings['com_tel'])
                result['msg'] = fname
            except Exception, e:
                result['err'] = 1
                result['msg'] = e.message

        self.write(simplejson.dumps(result))


@route(r'/ajax/checkvcode', name='ajax_checkvcode')  # 检查验证码是否正确
class CheckVcodeHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        user = self.current_user
        vcode = self.get_argument("vcode", None)  # 余额支付验证码
        if vcode:
            if UserVcode.select().where((UserVcode.mobile == user.mobile) & (UserVcode.vcode == vcode) & (
                        UserVcode.flag == 1)).count() > 0:
                self.set_secure_cookie('mobile', user.mobile, expires_days=1)
            else:
                result['err'] = 1
                result['msg'] = '请输入正确的验证码'

        self.write(simplejson.dumps(result))


@route(r'/ajax/getwlinfo', name='ajax_getwlinfo')  # 根据物流单号获取物流信息
class GetWLInfoandler(BaseHandler):

    executor = ThreadPoolExecutor(50)
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        yield self.execGetWLInfo(self)

    @run_on_executor
    def execGetWLInfo(self, handler):
        wlnum = handler.get_argument('deliverynum', None)
        s = ''
        try:
            s = urllib2.urlopen("http://www.kuaidi100.com/query?type=zhaijisong&postid=" + wlnum).read()
        except:
            pass

        handler.write(simplejson.dumps(s))


@route(r'/ajax/grouporder/(\d+)', name='ajax_grouporder')  # 合并、解耦订单
class GroupOrderHandler(BaseHandler):
    def post(self, flag):
        ids = simplejson.loads(self.get_argument("ids", '[]'))
        try:
            if flag == '0':  # 解耦
                ##############Modify by Tan in 20150526 拆分订单 重新计算运费 begin#######################################
                qorders=Order.select().where(Order.id<<ids)
                for n in qorders:
                    shippingprice = 5
                    if n.price < 29:
                        n.currentprice=n.currentprice + shippingprice
                        n.shippingprice=shippingprice
                        if n.payment!=0:#非货到付款的订单，要扣除余额
                            b = Balance()
                            b.user = n.user
                            b.balance =shippingprice
                            b.stype = 1
                            b.log = u'后台拆分订单，扣除运费：'+ n.ordernum
                            b.remark = u'后台拆分订单，扣除运费：'+ n.ordernum
                            b.created = int(time.time())
                            b.save()
                        n.save()
                ##############Modify by Tan in 20150526 拆分订单 重新计算运费 end#######################################
                for id in ids:
                    q = GroupOrder.delete().where(GroupOrder.order == id)
                    q.execute()
            elif flag == '1':  # 合并
                ##############Modify by Tan in 20150526 合并订单 取消运费 begin#######################################
                qorders=Order.select().where(Order.id<<ids).order_by(Order.payment.desc())#有运费的话，保留第一个订单
                summoney=0
                for n in qorders:
                    summoney=summoney+n.price
                iCount = 0
                # if summoney < 29: #合并后订单金额少于29，保留一个运费
                for n in qorders:
                    iCount=iCount+1
                    if iCount==1 and summoney < 29:
                        continue
                    shippingprice = 0
                    if n.shippingprice > 0:
                        shippingprice=n.shippingprice
                        n.currentprice=n.currentprice-shippingprice
                        n.shippingprice=0
                        if n.payment!=0:#非货到付款的订单，要返还余额
                            b = Balance()
                            b.user = n.user
                            b.balance =shippingprice
                            b.stype = 0
                            b.log = u'后台合并订单，取消运费：'+ n.ordernum
                            b.remark = u'后台合并订单，取消运费：'+ n.ordernum
                            b.created = int(time.time())
                            b.save()
                        n.save()
                ##############Modify by Tan in 20150526 合并订单 取消运费 end#######################################
                q = GroupOrder.select().where(GroupOrder.order << ids)

                if q.count() == 0:
                    name = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    for id in ids:
                        GroupOrder.create(name=name, order=id)
                else:
                    name = q[0].name
                    for id in ids:
                        c = GroupOrder.select().where(GroupOrder.order == id).count()
                        if c == 0:
                            GroupOrder.create(name=name, order=id)
            else:
                pass
            msg = '操作完成'
        except Exception, e:
            msg = e.message

        self.write(msg)


@route(r'/ajax/update_inventory', name='ajax_update_inventory')  # 库存盘点
class UpdateInventoryHandler(BaseHandler):
    def post(self):
        result = ''
        try:
            pid = int(self.get_argument("pid", 0))  # 产品ID
            quantity = float(self.get_argument("quantity", 0))  # 库存数量
            oq = float(self.get_argument("oq", 0))  # 系统库存数量

            pro = Product.get(id=pid)
            ps = ProductStandard.get(id=pro.defaultstandard)
            list = simplejson.loads(ps.relations)
            pslist = ProductStandard.select().where(ProductStandard.id << list)
            q_old = 0
            c = pslist.count()
            total_loss = 0
            for n in pslist:
                p = Product.get(id=n.product.id)
                last_time = p.updatedtime  # 上次盘点时间
                q_old += p.quantity
                if p.total_loss:
                    p.total_loss = p.total_loss + (p.quantity - quantity)
                else:
                    p.total_loss = p.quantity - quantity
                p.quantity = quantity
                total_loss += p.total_loss
                p.updatedtime = int(time.time())
                p.save()
            '''product = Product.get(id = pid)
            product.quantity = quantity
            product.updatedtime = int(time.time())
            if product.total_loss:
                product.total_loss = product.total_loss + (oq - quantity)
            else:
                product.total_loss = oq - quantity
            product.save()'''

            invoicint = Invoicing.select().where((Invoicing.product == pid) & (Invoicing.type == 0))
            total_weight = sum(n['quantity'] for n in invoicint.dicts())
            i = Inventory()
            i.product = pid
            i.original_weight = q_old / c
            i.weight = quantity
            i.current_total_weight = total_weight
            if total_weight != 0:
                i.loss = round((total_loss / c / total_weight * 100), 2)
            else:
                i.loss = 0
            i.updatedtime = int(time.time())
            i.updatedby = self.get_admin_user()
            i.save()
            result = 'success'
        except Exception, e:
            result = u'修改失败' + e.message
        self.write(result)


@route(r'/ajax/getproduct', name='ajax_getproduct')  # 后台补单添加产品
class GetProductHandler(BaseHandler):
    def get(self):
        result = {'sku': '', 'cover': '', 'price': '0', 'err': ''}
        try:
            pid = int(self.get_argument("pid", 0))  # 产品ID
            product = Product.get(id=pid)
            result['sku'] = product.sku
            result['cover'] = product.cover
            if product.defaultstandard:
                ps = ProductStandard.get(id=product.defaultstandard)
                result['price'] = ps.price
        except Exception, e:
            result['err'] = u'获取失败' + e.message
        self.write(simplejson.dumps(result))



@route(r'/ajax/check_user', name='ajax_check_user')  # 检查用户 存在则返回用户信息
class CheckUserHandler(BaseHandler):
    def get(self):
        result = {'take_name': '', 'take_tel': '', 'take_address': '', 'msg': '', 'user_id': '', 'region': '',
                  'addr_id': '', 'street': ''}
        mobile = self.get_argument("mobile")
        try:
            user = User.get((User.username == mobile) | (User.mobile == mobile))
            if user:
                userAddrs = UserAddr.select().where((UserAddr.user == user.id) & (UserAddr.isactive == 1)).order_by(
                    UserAddr.id.desc()).limit(1)
                for ua in userAddrs:
                    result['take_name'] = ua.name
                    result['take_tel'] = ua.mobile
                    result['take_address'] = ua.address
                    result['region'] = ua.region
                    result['addr_id'] = ua.id
                    result['street'] = ua.street
                result['user_id'] = user.id
                result['msg'] = '503'
            else:
                result['msg'] = '504'
        except Exception, e:
            result['msg'] = '505'  # 系统异常

        self.write(simplejson.dumps(result))


@route(r'/ajax/orders/export', name='ajax_order_export')  # 生成order的csv
class OrdersExportHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        sql = simplejson.loads(self.get_argument("sql", None))
        if sql:
            try:
                fname = 'orders_export.csv'
                status = sql["status"]
                keyword = sql["keyword"]
                begindate = sql["begindate"]
                enddate = sql["enddate"]
                phone = sql["phone"]
                delivery = sql["delivery"]
                ft = (Order.status > -1)
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
                if delivery:
                    ft = ft & (Order.delivery == delivery)
                if begindate and enddate:
                    begin = time.strptime(begindate, "%Y-%m-%d")
                    end = time.strptime((enddate + " 23:59:59"), "%Y-%m-%d %H:%M:%S")
                    ft = ft & (Order.ordered > time.mktime(begin)) & (Order.ordered < time.mktime(end))

                q = Order.select().where(ft).order_by(Order.ordered.desc())
                for o in q:
                    oCount = Order.select().where((Order.id<o.id) & (Order.status>0) & (Order.status<5) & (Order.user==o.user)).count()
                    o.trade_no = str(oCount + 1)
                exportorders(q, fname)
                result['msg'] = fname
            except Exception, e:
                result['err'] = 1
                result['msg'] = e.message
        else:
            result['err'] = 1
            result['msg'] = '没有产生数据的逻辑'
        self.write(simplejson.dumps(result))


@route(r'/ajax/orders/exportsku', name='ajax_order_exportsku')  # 生成sku的csv文件
class OrdersExportSKUHandler(BaseHandler):
    def get(self):
        result = {'err': 0, 'msg': ''}
        try:
            status = int(self.get_argument("status", -1))
            category = self.get_argument("category", '01')
            begindate = self.get_argument("begindate", '')
            enddate = self.get_argument("enddate", '')
            title = '线上'
            ft = (Order.status > -1)&(Order.order_type==0)
            if status != -1:
                if status == 0:  # 待付款
                    ft = ft & ((Order.status == 0) & (Order.payment == 1))
                elif status == 1:  # 待处理
                    ft = ft & ((Order.status == 1) | ((Order.payment == 0) & (Order.status == 0)))
                else:
                    ft = ft & (Order.status == status)

            if begindate and enddate:
                title = begindate + u'至' + enddate + u'时间段'
                begindate1 = time.strptime(begindate, "%Y-%m-%d %H:%M:%S")
                enddate1 = time.strptime(enddate, "%Y-%m-%d %H:%M:%S")
                ft = ft & (Order.ordered > time.mktime(begindate1)) & (Order.ordered < time.mktime(enddate1))

            if category == '01':
                title=title+'水果'
                ft = ft & (Product.sku % '01%')
            elif category == '02':
                title=title+'蔬菜'
                ft = ft & (Product.sku % '02%')
            elif category == '03':
                title=title+'礼盒'
                ft = ft & (Product.sku % '03%')
            else:
                title=title+'全部'

            skus = Product.select(Product, db.fn.SUM(OrderItem.quantity).alias('quantity'),
                                  Product.quantity.alias('quantity1')). \
                join(OrderItem, on=(Product.id == OrderItem.product)). \
                join(Order, on=(Order.id == OrderItem.order)). \
                group_by(Product).where(ft).order_by(db.fn.SUM(OrderItem.quantity).desc(), Product.sku).aggregate_rows()

            fname = 'sku_export'+str(int(time.time()))+'.csv'
            exportsku(skus, fname, title)
            result['msg'] = fname
        except Exception, e:
            result['err'] = 1
            result['msg'] = e.message

        self.write(simplejson.dumps(result))

@route(r'/ajax/return_pay', name='admin_return_pay')  # 原路退款
class ReturnPayHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        ids = simplejson.loads(self.get_argument("ids", '[]'))
        if len(ids) == 0:
            result['err'] = 1
            result['msg'] = '请至少选择一个退款订单'
        else:
            try:
                q = PayBack.select().where(PayBack.id << ids)
                for pb in q:
                    pb.batch_no = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + str(pb.order.id)
                    pb.paybackby = self.get_admin_user().username
                    pb.paybacktime = int(time.time())
                    pb.save()
                    alipay = AlipayReturn(**self.settings)
                    result['msg'] = alipay.request_payback(pb.trade_no, pb.batch_no, pb.price)
            except Exception, e:
                result['err'] = 1
                result['msg'] = e.message

        self.write(simplejson.dumps(result))


@route(r'/ajax/cancel_return_pay', name='admin_cancel_return_pay')  # 取消退款申请
class CancelReturnPayHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        ids = simplejson.loads(self.get_argument("ids", '[]'))
        if len(ids) == 0:
            result['err'] = 1
            result['msg'] = '请至少选择一个退款申请'
        else:
            try:
                q = PayBack.select().where(PayBack.id << ids)
                for pb in q:
                    pb.status = -1
                    pb.save()
            except Exception, e:
                result['err'] = 1
                result['msg'] = e.message

        self.write(simplejson.dumps(result))


@route(r'/ajax/upd_orderitem', name='ajax_upd_orderitem')  # 更新订单项
class UpdateOrderItemHandler(BaseHandler):
    def get(self):
        result = 0
        iid = int(self.get_argument("iid", 0))
        oid = int(self.get_argument("oid", 0))
        quantity = int(self.get_argument("quantity", 1))
        try:
            if iid != 0 and oid != 0:
                item = OrderItem.get(id=iid)
                old_quantity = item.quantity
                item.quantity = quantity
                o = Order.get(id=oid)
                o.price -= old_quantity * item.price
                o.price += quantity * item.price
                o.currentprice -= old_quantity * item.price
                o.currentprice += quantity * item.price
                if o.currentprice >= 0 and o.price >= 0:
                    o.save()
                    item.save()
                else:
                    result = -2
        except Exception, e:
            result = -1

        self.write(simplejson.dumps(result))


@route(r'/ajax/user_update_gift', name='ajax_user_update_gift')  # 更新用户礼品获取信息
class UserUpdateGiftHandler(BaseHandler):
    def post(self):
        result = 0
        uid = int(self.get_argument("uid", 0))
        type = int(self.get_argument("type", 0))
        try:
            if uid != 0 and type != 0:
                user = User.get(id=uid)
                if type == 1:
                    old_gift = user.gift[1]
                    if user.gift[0] == '0':
                        user.gift = '1' + old_gift
                        result = 1
                    else:
                        user.gift = '0' + old_gift
                        result = 2
                else:
                    old_gift = user.gift[0]
                    if user.gift[1] == '0':
                        user.gift = old_gift + '1'
                        result = 1
                    else:
                        user.gift = old_gift + '0'
                        result = 2
                user.save()
        except Exception, e:
            result = -1

        self.write(simplejson.dumps(result))

@route(r'/ajax/user_singup_gift', name='ajax_user_singup_gift')  # 更新用户注册礼信息，如果管理员后台点击注册礼，则扣除用户注册赠送的10元余额，反之增加10元余额
class UserSingupGiftHandler(BaseHandler):
    def post(self):
        result = ''
        result = {'err': 0, 'msg': ''}
        uid = int(self.get_argument("uid", 0))
        try:
            if uid != 0:
                user = User.get(id=uid)
                old_gift = user.gift[1]

                balance = Balance()
                balance.user = uid
                balance.balance = 10
                balance.created = int(time.time())
                if user.gift[0] == '0':
                    if user.balance >= 10:  #先判断用户账户余额中是否有10元余额
                        user.gift = '1' + old_gift  # 1 表示获取实物礼品，扣除10元新用户赠送余额
                        user.save()
                        balance.stype = 1
                        balance.log = u'用户选择线下实物礼品，扣除10元账户余额。'
                        balance.save()
                        result['msg'] = u'操作成功，用户获取线下实物礼品，扣除10元账户余额。'
                        result['err'] = 1
                    else:
                        result['msg'] = u'用户账户余额不足10元，无法获取线下实物礼。'
                        result['err'] = -1
                else:
                    user.gift = '0' + old_gift  # 0 表示取消实物礼品，返还10元新用户赠送余额
                    user.save()
                    balance.stype = 0
                    balance.log = u'管理员取消线下实物礼品，返还10元账户余额。'
                    balance.save()
                    result['msg'] = u'操作成功，管理员取消线下实物礼品，返还10元账户余额。'
                    result['err'] = 2
        except Exception, e:
            result['msg'] = u'操作失败，错误信息：'+ e.message
            result['err'] = -1

        self.write(simplejson.dumps(result))

@route(r'/ajax/change_event', name='ajax_change_event')  # 更新产品是否活动状态
class UserChangeEventHandler(BaseHandler):
    def post(self):
        result = 0
        pid = int(self.get_argument("pid", 0))
        try:
            if pid != 0:
                product = Product.get(id=pid)
                if product.is_index == 0:
                    product.is_index = 1
                    result = 1
                else:
                    product.is_index = 0
                    result = 2
                product.save()
        except Exception, e:
            result = -1

        self.write(simplejson.dumps(result))

@route(r'/ajax/product_change_pass', name='ajax_product_change_pass')  # 更新产品的审核状态
class ProductChangePassHandler(BaseHandler):
    def post(self):
        result = 0
        pid = int(self.get_argument("pid", 0))
        try:
            if pid != 0:
                product = Product.get(id=pid)
                product.is_pass = product.is_pass + 1
                if product.is_pass >2:
                    product.is_pass = 1
                result = product.is_pass
                product.save()
        except Exception, e:
            result = -1

        self.write(simplejson.dumps(result))

@route(r'/ajax/product_change_bargain', name='ajax_product_change_bargain')  # 更新产品的状态:正常，免费，特价
class ProductChangeBargainHandler(BaseHandler):
    def post(self):
        result = 0
        pid = int(self.get_argument("pid", 0))
        try:
            if pid != 0:
                product = Product.get(id=pid)
                product.is_bargain = product.is_bargain + 1
                if product.is_bargain >2:
                    product.is_bargain = 0
                result = product.is_bargain
                product.save()
        except Exception, e:
            result = -1

        self.write(simplejson.dumps(result))

@route(r'/ajax/change_balance', name='ajax_change_balance')  # 修改账户余额
class UserChangeBalanceHandler(BaseHandler):
    def post(self):
        result = 0
        content = {}
        uid = int(self.get_argument("uid", 0))
        type = int(self.get_argument("type", -1))
        price = float(self.get_argument("price", 0))
        remark = self.get_argument("remark", '')
        try:
            if uid != 0 and price > 0 and type > -1:
                user = User.get(id=uid)
                content['userid'] = user.id
                content['username'] = user.username
                balance = Balance()
                balance.user = uid
                balance.balance = price
                balance.created = int(time.time())
                if type == 0:  # 0增加；1减少
                    balance.stype = 0
                    balance.log = u'系统后台赠送余额。'
                    result = 1
                    content['content'] = u'为用户 ' + user.username + u' 增加余额' + str(price) + u'元'
                    sms = {'mobile': user.username,
                           'body': u"尊敬的客户您好，系统为您充值的 " + str(price) + u" 元账户余额已到账，请查收。",
                           'signtype': '1', 'isyzm': '1'}
                    create_msg(simplejson.dumps(sms), 'sms')
                elif type == 1:
                    balance.stype = 1
                    balance.log = u'系统后台扣除余额。'
                    result = 1
                    content['content'] = u'为用户 ' + user.username + u' 扣除余额' + str(price) + u'元'
                balance.remark = remark
                balance.save()
                AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        except Exception, e:
            result = -1
        self.write(simplejson.dumps(result))

@route(r'/ajax/change_score', name='ajax_change_score')  # 修改用户积分
class UserChangeBalanceHandler(BaseHandler):
    def post(self):
        result = 0
        content = {}
        uid = int(self.get_argument("uid", 0))
        type = int(self.get_argument("type", -1))
        price = float(self.get_argument("price", 0))
        remark = self.get_argument("remark", '')
        try:
            if uid != 0 and price > 0 and type > -1:
                user = User.get(id=uid)
                content['userid'] = user.id
                content['username'] = user.username
                s = Score()
                s.user = uid
                s.score = price
                s.created = int(time.time())
                if type == 0:  # 0增加；1减少
                    s.stype = 0
                    s.log = u'系统后台赠送积分。'
                    result = 1
                    content['content'] = u'为用户 ' + user.username + u' 增加积分' + str(price) + u'元'
                elif type == 1:
                    s.stype = 1
                    s.log = u'系统后台扣除积分。'
                    result = 1
                    content['content'] = u'为用户 ' + user.username + u' 扣除积分' + str(price) + u'元'
                s.remark = remark
                s.save()
                AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        except Exception, e:
            result = -1
        self.write(simplejson.dumps(result))

@route(r'/ajax/sms_send', name='ajax_sms_send')  # 给指定用户发送消息
class UserSmsSendHandler(BaseHandler):
    def post(self):
        result = 0
        content = {}
        phone = self.get_argument("phone", '')
        sms_content = self.get_argument("content", '')
        type = int(self.get_argument("type", 0))
        try:
            if phone != '' and sms_content != '':
                if type == 0:  # 0增加；1减少
                    content['content'] = u'为用户 ' + str(phone) + u' 推送极光消息，消息内容：' + sms_content

                    ausers = AdminUser.select().where((AdminUser.mobile != '') & (AdminUser.isactive == 1) & (AdminUser.roles % '%B%'))
                    sms = {'apptype': 1, 'body': sms_content, 'receiver': [phone]}
                    create_msg(simplejson.dumps(sms), 'jpush')
                    result = 1
                elif type == 1:
                    content['content'] = u'为用户 ' + phone + u' 发送短信，短信内容：' + sms_content
                    sms = {'mobile': phone,
                           'body': sms_content,
                           'signtype': '1', 'isyzm': ''}
                    create_msg(simplejson.dumps(sms), 'sms')
                    result = 1
                AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        except Exception, e:
            result = -1
        self.write(simplejson.dumps(result))


@route(r'/ajax/draw', name='ajax_draw')  # 转盘抽奖
class ActTestHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def get(self):
        try:
            user = User.get(User.id == self.current_user.id)
        except:
            user = None
        # if user:
        # result["err"]=0
        try:
            result = {'index': 0,'name': '抽奖次数已用完，请明天再来！', 'angle':0,'msg':'' ,'count': 0}#id 奖项名称,角度
            if user.raffle_count > 0:
                try:
                    user.raffle_count -= 1
                    user.save()
                    prize=[[1,"92","115","200元果蔬礼包",0],
                           [2,"62","80","20元果蔬礼包",1],
                           [3,"212","230","10元账户余额",2],
                           [4,"302","328","10元优惠券",200],
                           [5,"182","200","5元账户余额",4],
                           [6,"272","298","5元优惠券",200],
                           [7,"152","170","1份小台芒",1],    # psid=166
                           [8,"122","140","1份洛川富士",1],  # psid=1
                           [9,"242","260","1份哈密瓜",0],    # psid=93
                           [10,"32","55","50积分",100],
                           [11,"1","28","20积分",220],
                           [12,"332","358","10积分",270]]
                    #id,奖项对应的最小角度,最大角度,奖项名称,概率
                    arrv=[s[4] for s in prize]
                    # for i in range(len(prize)):
                    #     arrv.append(prize[i][4])
                    iIndex=self.getrand(arrv)
                    arrmin=prize[iIndex][1].split(',')
                    arrmax=prize[iIndex][2].split(',')
                    iangle=random.randint(0,len(arrmin)-1)
                    minangle=int(arrmin[iangle])
                    maxangle=int(arrmax[iangle])
                    result['index']=prize[iIndex][0]
                    result['name']=prize[iIndex][3]
                    result['angle']=random.randint(minangle,maxangle)
                    result['count'] = user.raffle_count
                    level = prize[iIndex][0]
                    self.draw(level,prize[iIndex][3])
                    if level == 10 or level == 11 or level == 12:
                        self.score(level)
                    elif level == 3 or level == 5:
                        self.balance(level)
                    elif level == 4 or level == 6:
                        self.coupon(level)
                    elif level == 7 or level == 8 or level == 9:
                        self.gift(level, user)
                    user = User.get(id = self.current_user.id)
                    self.session['user']=user
                    self.session.save()
                except Exception, ex:
                    result['index']=-1
                    result['name']= u'谢谢参与'
                    result['angle']=0
                    result['msg']=ex
        except:
            result['index']=-1
            result['name'] = u'您尚未登陆，请先登录！'
            result['angle']=0
            result['msg'] = ''
        self.write(simplejson.dumps(result))

    def getrand(self,arrv):
        arrall=[]
        iIndex=0;
        for i in range(len(arrv)):
            for j in range(arrv[i]):
                arrall.append(i)
                iIndex=iIndex+1
        irnd=random.randint(0,iIndex)
        iresult=arrall[irnd]
        return iresult
    def score(self,level):
        user = User.get(User.id == self.current_user.id)
        s = Score()
        s.user = user
        s.stype = 0
        if level == 10:
            s.score = 50
        elif level == 11:
            s.score = 20
        elif level == 12:
            s.score = 10
        s.log = u'幸运转盘抽奖活动赠送积分'
        s.created = int(time.time())
        s.save()
    def draw(self,level,name):
        user = User.get(User.id == self.current_user.id)
        ud = User_Raffle_Log()
        ud.user = user
        ud.draw_level = level
        ud.draw_name = name
        ud.created = int(time.time())
        ud.save()
    def balance(self,level):
        user = User.get(User.id == self.current_user.id)
        b = Balance()
        b.user = user.id
        b.stype = 0
        if level == 3:
            b.balance = 10
        elif level == 5:
            b.balance = 5
        b.log = u'幸运转盘抽奖活动赠送余额'
        b.created = int(time.time())
        b.isactive = 1
        b.save()
    def coupon(self, level):
        log = u'幸运转盘抽奖活动赠送'
        user = User.get(User.id == self.current_user.id)
        cps5 = CouponTotal.select().where((CouponTotal.name == '满50减5元') & (CouponTotal.status == 0)).limit(1)
        cps10 = CouponTotal.select().where((CouponTotal.name == '满100减10元') & (CouponTotal.status == 0)).limit(1)
        if level == 6:
            if cps5.count() < 1:
                msg = u'幸运转盘抽奖返卷失败，请检查“满50减5元”优惠券是否存在或已被禁用，用户'+user.username +u"未获得返卷，请手动补充优惠券后手动补发。"
                admins = AdminUser.select()
                receivers = [n.email for n in admins if len(n.email)>0]
                email = {u'receiver': receivers, u'subject':u'幸运转盘抽奖返卷失败',u'body': msg}
                create_msg(simplejson.dumps(email), 'email')
            else:
                create_coupon(user, cps5[0].id, log)
        elif level == 4:
            if cps10.count() < 1:
                msg = u'幸运转盘抽奖返卷失败，请检查“满100减10元”优惠券是否存在或已被禁用，用户'+user.username +u"未获得返卷，请手动补充优惠券后手动补发。"
                admins = AdminUser.select()
                receivers = [n.email for n in admins if len(n.email)>0]
                email = {u'receiver': receivers, u'subject':u'幸运转盘抽奖返卷失败',u'body': msg}
                create_msg(simplejson.dumps(email), 'email')
            else:
                create_coupon(user, cps10[0].id, log)
    def gift(self, level, user):
        psid = 0
        if level == 7:
            psid = 166
        elif level == 8:
            psid = 1
        elif level == 9:
            psid = 93
        if psid != 0:
            ps = ProductStandard.get(id = psid)
            gift = Gift()
            gift.user = user.id
            gift.product = ps.product
            gift.product_standard = ps.id
            gift.quantity = 1
            gift.created = int(time.time())
            gift.created_by = 12    # 数据库中是 temp
            gift.status = 0
            gift.type = 4   # 4转盘抽奖
            gift.end_time = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 0:0:0", time.localtime(time.time()+ 86400 * 30)), "%Y-%m-%d 0:0:0")))
            gift.save()


@route(r'/ajax/comment/export', name='ajax_comment_export')  # 生成评论的csv
class CommentExportHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        sql = simplejson.loads(self.get_argument("sql", None))
        if sql:
            try:
                fname = 'comment_export.csv'
                status = sql["status"]
                pid = sql["pid"]
                begindate = sql["begindate"]
                enddate = sql["enddate"]
                uid = sql["uid"]
                ft = (Comment.id > 0)
                if status != -1:
                    ft = ft & (Comment.status == status)
                if pid and pid != 'None':
                    ft = ft & (Comment.product == pid)
                if uid and uid != 'None':
                    ft = ft & (Comment.user == uid)
                if begindate and enddate:
                    begin = time.strptime(begindate, "%Y-%m-%d")
                    end = time.strptime((enddate + " 23:59:59"), "%Y-%m-%d %H:%M:%S")
                    ft = ft & (Comment.created > time.mktime(begin)) & (Comment.created < time.mktime(end))

                q = Comment.select().where(ft).order_by(Comment.created.desc())
                exportcomment(q, fname)
                result['msg'] = fname
            except Exception, e:
                result['err'] = 1
                result['msg'] = e.message
        else:
            result['err'] = 1
            result['msg'] = '没有产生数据的逻辑'
        self.write(simplejson.dumps(result))


@route(r'/ajax/used_coupon_real', name='used_coupon_real')  # 使用实物卷，将商品添加至购物车
class UsedCouponRealHandler(BaseHandler):
    def get(self):
        result = 0
        try:
            cid = int(self.get_argument("cid", 0))
            if self.current_user:
                if cid > 0:
                    cr = CouponReal.select().where((CouponReal.id == cid) & (CouponReal.status == 1) & (CouponReal.user == self.current_user.id))
                    if cr.count() > 0:
                        c = Cart()
                        c.user = cr[0].user
                        c.product = cr[0].coupon_real_total.product
                        c.product_standard = cr[0].coupon_real_total.product_standard
                        c.quantity = 1
                        c.type = 1  # 1代表实物卷商品，赠品，抽奖，换购
                        c.save()

                        cr[0].status = 2
                        cr[0].save()

                        cr[0].coupon_real_total.used += 1
                        cr[0].coupon_real_total.save()
                        result = 1
                    else:
                        result = -1
                else:
                    result = -2
            else:
                result = -3
        except Exception, ex:
            logging.error(ex)
            result = -4
        self.write(simplejson.dumps(result))

@route(r'/ajax/used_gift', name='used_gift')  # 使用礼品
class UsedGiftHandler(BaseHandler):
    def get(self):
        result = 0
        try:
            cid = int(self.get_argument("cid", 0))
            if self.current_user:
                if cid > 0:
                    cr = Gift.select().where((Gift.id == cid) & (Gift.status == 0) & (Gift.user == self.current_user.id))
                    if cr.count() > 0:
                        cr[0].status = 0    # 0准备使用
                        cr[0].used_time = int(time.time())
                        cr[0].save()
                        result = 1
                    else:
                        result = -1
                else:
                    result = -2
            else:
                result = -3
        except Exception, ex:
            logging.error(ex)
            result = -4
        self.write(simplejson.dumps(result))

@route(r'/ajax/remove_gift', name='ajax_remove_gift')  # 删除购物车商品
class RemoveGiftHandler(BaseHandler):
    def post(self):
        result = 0
        id = self.get_argument('id')
        try:
            if id:
                Gift.delete().where(Gift.id == id).execute()
                result = 1
        except Exception, ex:
            logging.error(ex)
            result = 0
        self.write(simplejson.dumps(result))

@route(r'/ajax/delivery/order_status', name='delivery_order_status')  # 物流公司标记为已送达
class DeliveryOrderStatusHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        try:
            id = int(self.get_argument("id", 0))
            status = int(self.get_argument("status", 4))
            OrderChangeStatus(id, status, 0, self)
        except Exception, ex:
            result['err'] = 1
            result['msg'] = ex.message
        self.write(simplejson.dumps(result))

@route(r'/ajax/export/users', name='ajax_export_users')  # 生成用户列表数据csv文件
class CSVUserHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        begindate = self.get_argument("begin", '')
        enddate = self.get_argument("end", '')
        order_sign = self.get_argument("order_sign", '')

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

        try:
            fname = 'users.csv'
            q = User.select(User,db.fn.COUNT(Order.user).alias('order_count')).join(Order, db.JOIN_LEFT_OUTER,
                                    on=((User.id==Order.user) &
                                    (((Order.status>-1) & (Order.payment==0)) | ((Order.payment>0) &
                                    (Order.status>0))) & (Order.payment<9) &
                                    (Order.status<5))).where(ft).group_by(User.id).order_by(order_str)

            export_user_csv(q, fname)
            result['msg'] = fname
        except Exception, e:
            result['err'] = 1
            result['msg'] = e.message

        self.write(simplejson.dumps(result))

@route(r'/ajax/score_buy', name='ajax_score_buy')  # 积分兑换
class CSVUserHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': '', 'score': 0}
        quantity = int(self.get_argument("quantity", '0'))
        score = int(self.get_argument("score", '0'))
        pid = self.get_argument("pid", '')
        psid = self.get_argument("psid", '')
        try:
            user = User.get(User.id == self.current_user.id)
        except:
            user = None
        try:
            if user:
                score_num = score * quantity
                if user.score > score_num:
                    if quantity and score:
                        p = Product.get(Product.id == pid)
                        s = Score()
                        s.user = user
                        s.stype = 1
                        s.score = score * quantity
                        s.log = u'积分换购商品 '+ p.name
                        s.created = int(time.time())
                        s.save()

                        gift = Gift()
                        gift.user = user.id
                        gift.product = pid
                        gift.product_standard = psid
                        gift.quantity = quantity
                        gift.created = int(time.time())
                        gift.created_by = 12    # 数据库中是 temp
                        gift.status = 0
                        gift.type = 2   # 2积分兑换
                        gift.end_time = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 0:0:0", time.localtime(time.time()+ 86400 * 30)), "%Y-%m-%d 0:0:0")))
                        gift.save()

                        # c = Cart()
                        # c.user = user.id
                        # c.product = pid
                        # c.product_standard = psid
                        # c.quantity = 1
                        # c.type = 1  # 1代表实物卷商品，赠品，抽奖，换购
                        # c.save()
                        user = User.get(id = self.current_user.id)
                        self.session['user']=user
                        self.session.save()
                        result['score'] = user.score
                    else:
                        result['err'] = 1
                        result['msg'] = '兑换失败，请刷新后重试！'
                else:
                    result['err'] = 1
                    result['msg'] = '兑换失败，可用积分不足！'
            else:
                result['err'] = 1
                result['msg'] = '您尚未登录车装甲，请先登录！'
        except:
            result['err'] = 1
            result['msg'] = '兑换失败，请稍后重试！'
        self.write(simplejson.dumps(result))

@route(r'/ajax/check_store', name='ajax_check_store')  # 根据用户收货地址检查是否有可以当日送达的店铺
class CheckStoreHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': '', 'store': 0, 'product': []}
        aid = int(self.get_argument("aid", ''))
        pids = self.get_argument("pids", '')
        opids = self.get_argument("opids", '')
        try:
            if aid:
                ua = UserAddr.get(UserAddr.id == aid)
                address = ua.province + ua.city + ua.address
                s = getMinDistanceStore(address.replace(' ', ''))
                if s['flag'] == 1:
                    result['store'] = s['data']
            if pids:
                pids = pids.split(',')
                products = Product.select().where(Product.id << pids)
                for p in products:
                    if p.store:
                        result['product'].append({'pid': p.id, 'name': p.name, 'psid': p.defaultstandard, 'store_id': p.store.id, 'store_name': p.store.name})
            if opids:
                opids = opids.split(',')
                op = ProductOffline.select().where(ProductOffline.id << opids)
                for p in op:
                    result['product'].append({'pid': p.product.id, 'name': p.product.name, 'psid': p.product.defaultstandard, 'store_id': p.store.id, 'store_name': p.store.name, 'poid': p.id})


        except Exception, e:
            result['err'] = 1
            result['msg'] = e.message

        self.write(simplejson.dumps(result))

@route(r'/ajax/orderUpdateStore', name='orderUpdateStore')  # 将产品加入批发购物车
class OrderUpdateStoreHandler(BaseHandler):
    def get(self):
        result = {'flag':'0','msg':''}
        try:
            orderid = int(self.get_argument("orderid", 0))
            storeid = int(self.get_argument("storeid", 0))

            order = Order.get(Order.id==orderid)
            storeid_old=order.store
            if not storeid_old:
                storeid_old=0
            if storeid==storeid_old:
                result["flag"] = 0
                result["msg"]="订单所属经销商未改变，不需要操作！"
            else:
                if storeid>0:
                    order.store=storeid
                else:
                    order.store=None
                order.save()
                for oi in order.items:
                    if storeid>0:#订单移到经销商，需要减目标经销商的库存
                        si=Inventory_Store.select().where((Inventory_Store.product==oi.product.id)&Inventory_Store.store==storeid)
                        if si.count()>0:
                            si[0].quantity=si[0].quantity-oi.quantity
                            si[0].save()
                    else:#订单移出经销商，需要增加原经销商的库存
                        si=Inventory_Store.select().where((Inventory_Store.product==oi.product.id)&Inventory_Store.store==storeid_old)
                        if si.count()>0:
                            si[0].quantity=si[0].quantity+oi.quantity
                            si[0].save()
                result["flag"] = 1
                result["msg"]=""
        except:
            # logging.error(ex)
            result["flag"] = 0
            result["msg"]="程序错误"
        self.write(simplejson.dumps(result))

@route(r'/ajax/remove_store_cart', name='ajax_remove_store_cart')  # 移除购物车中不能配送的商品
class CheckStoreHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': '', 'items': []}
        pids = self.get_argument("pids", '')
        opids = self.get_argument("opids", '')
        sid = int(self.get_argument("sid", '0'))
        try:
            if pids:
                pids = pids.split(',')
                products = Product.select().where(Product.id << pids)
                for p in products:
                    if p.store:
                        if p.store.id == sid:
                            result['items'].append(p.id)
                    else:
                        result['items'].append(p.id)
            if opids:
                opids = opids.split(',')
                op = ProductOffline.select().where(ProductOffline.id << opids)
                for p in op:
                    result['items'].remove(p.product.id)
        except Exception, e:
            result['err'] = 1
            result['msg'] = e.message

        self.write(simplejson.dumps(result))

@route(r'/ajax/export/products', name='ajax_export_products')  # 生成用户列表数据csv文件
class CSVProductHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        status = self.get_argument("status", '-1')
        sku = self.get_argument("sku", '-1')

        fn = (Product.status > 0) & (Product.is_store != 1)
        if status != '-1' and status != '0':
            fn = fn & (Product.status == status)
        skus = '' + sku + '%'
        if sku != '-1' and sku != '00':
            fn = fn & (Product.sku % skus)
        try:
            fname = 'products.csv'
            q = Product.select().where(fn).order_by(Product.id)
            for n in q:
                ps = ProductStandard.get(id = n.defaultstandard)
                n.total_loss = ps.weight

            export_product_csv(q, fname)
            result['msg'] = fname
        except Exception, e:
            result['err'] = 1
            result['msg'] = e.message

        self.write(simplejson.dumps(result))

@route(r'/ajax/cancel_order', name='ajax_cancel_order')  # 根据订单ID取消订单
class CancelOrderHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        id = self.get_argument("id", '-1')
        status = int(self.get_argument("status", '-1'))
        cause = self.get_argument("cause", '')
        content = {}
        try:
            OrderChangeStatusStore(id, status, 1, self)
            o = Order.get(Order.id == id)
            o.cancelreason = cause + u'；操作人：' +self.get_admin_user().username  #订单取消原因
            o.save()
            content['cancel_cause'] = cause
            content['order_id'] = id
            AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        except Exception, e:
            result['err'] = 1
            result['msg'] = e.message

        self.write(simplejson.dumps(result))

@route(r'/ajax/export/price', name='ajax_export_price')  # 生成价格数据csv
class CSVPriceHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        now = datetime.datetime.now()
        n_days = now + datetime.timedelta(days=1)
        date = n_days.strftime('%Y-%m-%d')

        ft = (Product.status == 1) & (Product.is_store == 0)  # 只查询上架商品
        try:
            fname = 'price.csv'
            products = Product.select(Product.id, Product.status, Product.sku, Product.name,
                                  ProductStandard.name.alias('standard'), Product.args,
                                  ProductStandard.ourprice.alias('currentprice'),
                                  ProductStandard.price.alias('currentpreprice'),
                                  ProductStandard.pricefunction, ProductStandard.weight,
                                  InvoicingChanged.last_unitprice.alias('last_unitprice'),
                                  InvoicingChanged.current_unitprice.alias('current_unitprice'),
                                  (InvoicingChanged.current_unitprice - ProductStandard.ourprice).alias('differprice'),
                                  ProductStandard.id.alias('sid')). \
            join(ProductStandard, on=(ProductStandard.id == Product.defaultstandard)).\
            join(InvoicingChanged, db.JOIN_LEFT_OUTER, on=(InvoicingChanged.product == Product.id)). \
            where(ft).order_by((InvoicingChanged.current_unitprice - ProductStandard.ourprice).desc()).dicts()

            export_price_csv(products, fname)
            result['msg'] = fname
        except Exception, e:
            result['err'] = 1
            result['msg'] = e.message

        self.write(simplejson.dumps(result))

@route(r'/ajax/add_cart_store', name='add_cart_store')  # 将店铺商品加入购物车
class AddCartStoreHandler(BaseHandler):
    def get(self):
        result = 0
        try:
            sid = self.get_argument("sid", '')
            if sid:
                id_list = [int(n) for n in sid.split(',')]
                fn = ((ProductOffline.status == 2) & (ProductOffline.id << id_list))
                items = ProductOffline.select().where(fn)
                if items.count() > 0:
                    carItems = []
                    for n in items:
                        if self.current_user:
                            c = Cart()
                            c.user = self.current_user.id
                            c.product = n.product.id
                            c.product_standard = n.product.defaultstandard
                            c.quantity = 1
                            c.type = 3      # 3表示线下商品
                            c.product_offline = n.id
                            c.created = int(time.time())
                            c.save()
                            n.status = 6    # 加入购物车后锁定该商品
                            n.save()
                        else:
                            result = -2
                else:
                    result = -3
        except Exception, ex:
            logging.error(ex)
            result = -1
        self.write(simplejson.dumps(result))

@route(r'/ajax/auto_delivery', name='ajax_auto_delivery')  # 自动选择物流公司
class AutoDeliveryHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': '', 'data': []}
        ids = simplejson.loads(self.get_argument("ids", '[]'))
        if len(ids) == 0:
            result['err'] = 1
            result['msg'] = '请至少选择一个订单'
        else:
            try:
                q = Order.select().where((Order.id << ids) & (Order.delivery == None))
                for n in q:
                    # s = getMinDistanceStore(n.take_address.replace(' ', ''))
                    # if s['flag'] == 1:
                    #     result['store'] = s['data']   #莲湖区 雁塔区 新城区
                    if n.store != None:
                        result['data'].append({
                            'id': n.id,
                            'delivery': 3
                        })
                    elif u'莲湖区' in n.take_address or u'雁塔区' in n.take_address or u'新城区' in n.take_address:
                        result['data'].append({
                            'id': n.id,
                            'delivery': 2
                        })
                    else:
                        result['data'].append({
                            'id': n.id,
                            'delivery': 1
                        })


            except Exception, e:
                result['err'] = 1
                result['msg'] = e.message

        self.write(simplejson.dumps(result))

@route(r'/ajax/save_delivery', name='ajax_save_delivery')  # 自动选择物流公司
class SaveDeliveryHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        ids = simplejson.loads(self.get_argument("ids", '[]'))
        try:
            idx = 0
            dvnum = {}
            for n in ids:
                id = n['id']
                did = n['did']
                q = Order.select().where((Order.id == id) & (Order.delivery == None))
                if q.count() > 0:
                    if did == '1':
                        ordernumbers = DeliveryNumbers.select().where((DeliveryNumbers.status == 0) &
                                                              (DeliveryNumbers.delivery == 1)).paginate(1, len(ids))
                        if ordernumbers.count() < len(ids):
                            result['err'] = 1
                            result['msg'] = '该物流公司的可用订单号不足，请立即联系物流公司'
                        elif ordernumbers.count() > len(ids):
                            result['err'] = 1
                            result['msg'] = '所选订单号与物流单号对应错误，请联系技术人员'
                        else:
                            try:
                                with db.handle.transaction():
                                    o = q[0]
                                    if not o.delivery:
                                        if o.group_orders.count() > 0:
                                            name = o.group_orders[0].name
                                            if dvnum.has_key(name):
                                                o.deliverynum = dvnum[name]
                                            else:
                                                dvnum[name] = ordernumbers[idx].num
                                                o.deliverynum = dvnum[name]
                                                ordernumbers[idx].status = 1
                                                ordernumbers[idx].save()
                                                idx += 1
                                        else:
                                            o.deliverynum = ordernumbers[idx].num
                                            ordernumbers[idx].status = 1
                                            ordernumbers[idx].save()
                                            idx += 1
                            except Exception, e:
                                result['err'] = 1
                                result['msg'] = e.message
                    if did:
                        q[0].delivery = did
                        q[0].save()


        except Exception, e:
            result['err'] = 1
            result['msg'] = e.message

        self.write(simplejson.dumps(result))

@route(r'/ajax/GetSubBrands', name='ajax_GetSubBrands')  # 获取下级品牌
class AdminGetSubBrands(BaseHandler):
    def get(self):
        result = {'flag': 0, 'data': [], 'msg': ''}
        try:
            pcode = self.get_argument("pcode", '')
            keyword = '' + pcode + '%'
            items = Brand.select().where((Brand.code % keyword) & (Brand.is_delete == 0) & (db.fn.length(Brand.code) == len(pcode)+4)).order_by(Brand.spell,Brand.sort)
            result["flag"]=1
            result["data"]=[]
            for item in items:
                result["data"].append({
                    'id' : item.id,
                    'pid' : item.pid,
                    'code' : item.code,
                    'has_sub' : item.has_sub,
                    'name' : item.name,
                    'is_luxurious' : item.is_luxurious,
                    'spell' : item.spell,
                    'spell_abb' : item.spell_abb,
                    'sort' : item.sort,
                    'image' : item.image
                })
        except Exception, ex:
            result["flag"]=0
            result["msg"] = ex.message
        self.write(simplejson.dumps(result))

@route(r'/ajax/GetSubAreas', name='ajax_GetSubAreas')  # 获取下级区域
class AjaxGetSubAreas(BaseHandler):
    def get(self):
        result = {'flag': 0, 'data': [], 'msg': ''}
        try:
            pcode = self.get_argument("pcode", '')
            is_site = int(self.get_argument("is_site", 0))
            keyword = '' + pcode + '%'
            ft=(Area.code % keyword) & (Area.is_delete == 0) & (db.fn.length(Area.code) == len(pcode)+4)
            if is_site == 1:
                ft = ft & (Area.is_site == 1)
            items = Area.select().where(ft).order_by(Area.sort,Area.id,Area.spell)
            result["flag"]=1
            result["data"]=[]
            for item in items:
                result["data"].append({
                    'id' : item.id,
                    'pid' : item.pid,
                    'code' : item.code,
                    'has_sub' : item.has_sub,
                    'name' : item.name,
                    'is_site' : item.is_site,
                    'spell' : item.spell,
                    'spell_abb' : item.spell_abb,
                    'sort' : item.sort
                })
        except Exception, ex:
            result["flag"]=0
            result["msg"] = ex.message
        self.write(simplejson.dumps(result))


@route(r'/ajax/GetSites', name='ajax_GetSites')  # 获取站点
class AjaxGetSites(BaseHandler):
    def get(self):
        result = {'flag': 0, 'data': [], 'msg': ''}
        try:
            result["flag"]=1
            items_spell = Area.select().where((Area.is_delete == 0) & (Area.is_site == 1)).order_by(Area.code)
            list_spell=[]
            if items_spell:
                first_code = ""
                last_first_code = "_"
                spell_count=-1
                for item in items_spell:
                    first_code = item.code[0:4]
                    if first_code == last_first_code:
                        list_spell[spell_count]["citys"].append({
                            "id":item.id,
                            "code":item.code,
                            "name":item.name
                        })
                    else:
                        spell_count = spell_count + 1
                        list_spell.append({
                            "id":item.id,
                            "code":item.code,
                            "name":item.name,
                            "citys":[]
                        })
                        # list_spell[spell_count]["citys"].append({
                        #     "id":item.id,
                        #     "code":item.code,
                        #     "name":item.name
                        # })
                    last_first_code = first_code
            result["data"]=list_spell

        except Exception, ex:
            result["flag"]=0
            result["msg"] = ex.message
        self.write(simplejson.dumps(result))

@route(r'/ajax/get_sub_category', name='ajax_get_sub_category')  # 获取下级分类
class AdminGetSubCategory(BaseHandler):
    def get(self):
        result = {'flag': 0, 'data': [], 'msg': ''}
        try:
            pid = int(self.get_argument("pid", 0))
            items = CategoryFront.select().where((CategoryFront.pid == pid) & (CategoryFront.isactive == 1)).order_by(CategoryFront.slug)
            result["flag"] = 1
            result["data"] = []
            for item in items:
                result["data"].append({
                    'id': item.id,
                    'pid': item.pid,
                    'has_sub': item.has_sub,
                    'name': item.name,
                    'sort': item.slug
                })
        except Exception, ex:
            result["flag"] = 0
            result["msg"] = ex.message
        self.write(simplejson.dumps(result))

@route(r'/ajax/GetSubCategory', name='ajaxGetSubCategory')  # 获取下级分类
class AdminGetSubCategory(BaseHandler):
    def get(self):
        result = {'flag': 0, 'data': [], 'msg': ''}
        try:
            pcode = self.get_argument("pcode", "")
            keyword = '' + pcode + '%'
            subquery = Product.select(db.fn.COUNT(Product.id)).where(Product.categoryfront == CategoryFront.id)
            items = CategoryFront.select(CategoryFront, subquery.alias('p_count')). \
                join(Product, db.JOIN_LEFT_OUTER).where((CategoryFront.code % keyword) & (CategoryFront.isactive == 1) & (db.fn.length(CategoryFront.code) == len(pcode)+4)). \
                group_by(CategoryFront).order_by(CategoryFront.code)
            # items = CategoryFront.select().where((CategoryFront.pid == pid) & (CategoryFront.isactive == 1)).order_by(CategoryFront.slug)
            result["flag"] = 1
            result["data"] = []
            for item in items:
                result["data"].append({
                    'id': item.id,
                    'name': item.name,
                    'code': item.code,
                    'type': item.type,
                    'pid': item.pid,
                    'has_sub': item.has_sub,
                    'p_count': item.p_count,
                    'slug': item.slug
                })
        except Exception, ex:
            result["flag"] = 0
            result["msg"] = ex.message
        self.write(simplejson.dumps(result))

@route(r'/ajax/store_update_state', name='ajax_store_update_state')  # 更新门店状态
class StoreUpdateStateHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        id = int(self.get_argument("id", 0))
        state_type =int( self.get_argument("state_type", -1))
        try:
            if id:
                store = Store.get(Store.id == id)
                if state_type == 0:  # 更新审核状态
                    store.check_state = (store.check_state + 1)
                    if store.check_state > 2:
                        store.check_state = 1
                    if store.check_state ==1: # 审核通过 修改用户类型
                        user = User.get(User.store == id)
                        user.grade = 1
                        user.save()
                        store.credit_score = 80

                    result['msg'] = store.check_state
                elif state_type == 1:  # 更新推荐状态
                    store.is_recommend = (1 - store.is_recommend)
                    result['msg'] = store.is_recommend
                elif state_type == 2:  # 更新账户状态
                    user = User.get(User.store == id)
                    user.isactive = (1-user.isactive)
                    user.save()
                    result['msg'] = user.isactive
                store.save()
                result['err'] = 0

        except Exception, e:
            result['err'] = 1
            result['msg'] = e.message

        self.write(simplejson.dumps(result))


@route(r'/ajax/GetStoreComments', name='ajax_GetStoreComments')  # 获取门店评论
class AjaxGetStoreComments(BaseHandler):
    def get(self):
        result = {'flag': 0, 'data': [], 'msg': '', 'total': 0 , 'total_page': 0 }
        try:
            result["flag"]=1
            page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
            sid = int(self.get_argument("sid", 0))
            pagesize = 5
            ft = (Comment.status == 2)&(Comment.store == sid)
            q = Comment.select(Comment).join(User).where(ft)
            total = q.count()
            if total % pagesize > 0:
                totalpage = total / pagesize + 1
            else:
                totalpage = total / pagesize
            result["total_page"] = totalpage
            result["total"] = total
            comments = q.order_by(Comment.created.desc()).paginate(page, pagesize)
            lists = []
            for n in comments:
                username = ""
                if n.user.nickname and len(n.user.nickname) >= 3:
                    username = n.user.nickname[0:3]+"***"+n.user.nickname[-3:-1]
                else:
                    username = n.user.username[0:3]+"***"+n.user.username[-4:]
                lists.append({
                    "id": n.id,
                    "username": username,
                    "qualityscore": n.qualityscore,
                    "speedscore": n.speedscore,
                    "pricescore": n.pricescore,
                    "servicescore": n.servicescore,
                    "comment": n.comment,
                    "created": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(n.created)),
                    "reply_content": n.reply_content,
                    "reply_time": n.reply_time
                })
            result["data"] = lists

        except Exception, ex:
            result["flag"]=0
            result["msg"] = ex.message
        self.write(simplejson.dumps(result))

@route(r'/ajax/feedback_change_read', name='ajax_feedback_change_read')  # 更新意见反馈的阅读状态
class FeedbackChangeReadHandler(BaseHandler):
    def post(self):
        result = 0
        fid = int(self.get_argument("fid", 0))
        try:
            if fid != 0:
                p = Feedback.get(Feedback.id == fid)
                p.has_read = 1 - p.has_read
                p.save()
                result = p.has_read
        except Exception, e:
            result = -1

        self.write(simplejson.dumps(result))

@route(r'/ajax/question_update_state', name='ajax_question_update_state')  # 更新问题状态
class QuestionUpdateStateHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        id = int(self.get_argument("id", 0))
        state_type =int( self.get_argument("state_type", -1))
        try:
            if id:
                question = Question.get(Question.id == id)
                if state_type == 0:  # 更新审核状态
                    question.check_status = (question.check_status + 1)
                    if question.check_status > 2:
                        question.check_status = 1

                    result['msg'] = question.check_status
                elif state_type == 1:  # 更新推荐状态
                    question.is_recommend = (1 - question.is_recommend)
                    result['msg'] = question.is_recommend
                question.save()
                result['err'] = 0

        except Exception, e:
            result['err'] = 1
            result['msg'] = e.message

        self.write(simplejson.dumps(result))

@route(r'/ajax/circle_update_state', name='ajax_circle_update_state')  # 更新圈子状态
class CircleUpdateStateHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        id = int(self.get_argument("id", 0))
        state_type =int( self.get_argument("state_type", -1))
        try:
            if id:
                question = CircleTopic.get(CircleTopic.id == id)
                if state_type == 0:  # 更新审核状态
                    question.check_status = (question.check_status + 1)
                    if question.check_status > 2:
                        question.check_status = 1

                    result['msg'] = question.check_status
                # elif state_type == 1:  # 更新推荐状态
                #     question.is_recommend = (1 - question.is_recommend)
                #     result['msg'] = question.is_recommend
                question.save()
                result['err'] = 0

        except Exception, e:
            result['err'] = 1
            result['msg'] = e.message

        self.write(simplejson.dumps(result))


@route(r'/ajax/user/order/settlement', name='ajax_user_order_settlement')  # 用户订单结算
class OrderHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        ids = simplejson.loads(self.get_argument("ids", '[]'))
        try:
            u = self.current_user
            if u and len(ids) > 0:
                s = Settlement()
                s.user = self.current_user
                s.sum_money = 0
                s.created = int(time.time())
                s.save()
                sum_money = 0
                for n in ids:
                    order = Order.get(id=n)
                    if not order.settlement:
                        order.settlement = s
                        sum_money = sum_money + order.price
                        order.save()
                s.sum_money = sum_money
                s.save()
                u.cashed_money = u.cashed_money + sum_money
                u.save()
                self.session['user'] = u
            else:
                result['err'] = 1
                result['msg'] = "请登录后至少选择一个订单！"
            # content = {}
            # content['operatetype'] = '修改订单状态'
            # content['orderid'] = ids
            # AdminLog.create(user=self.get_admin_user(), dotime=int(time.time()), content=content)
        except Exception, e:
            result['err'] = 1
            result['msg'] = e.message

        self.write(simplejson.dumps(result))

@route(r'/ajax/withdraw_change_status', name='ajax_withdraw_change_status')  # 更新意见反馈的阅读状态
class WithdrawChangeStatusHandler(BaseHandler):
    def post(self):
        result = 0
        fid = int(self.get_argument("fid", 0))
        try:
            if fid != 0:
                p = Withdraw.get(Withdraw.id == fid)
                p.status = p.status + 1
                if p.status > 2:
                    p.status = 2
                p.processing_time = int(time.time())
                p.processing_by = self.get_admin_user()
                p.save()
                result = p.status
        except Exception, e:
            result = -1

        self.write(simplejson.dumps(result))

@route(r'/ajax/order/agent', name='ajax_order_agent')  # 指派代理商
class OrderAgentHandler(BaseHandler):
    def post(self):
        result = {'err': 0, 'msg': ''}
        id = self.get_argument("id", '0')
        agent_id = self.get_argument("agent_id", '1')
        try:
            order = Order.get(id=id)
            order.agent = agent_id
            order.lasteditedtime = int(time.time())
            order.save()
        except Exception, e:
            result['err'] = 1
            result['msg'] = e.message
        self.write(simplejson.dumps(result))

@route(r'/ajax/user/pic/(\d+)', name='ajax_user_pic')  # 上传用户图片文件
class UploadUserPicHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def post(self, pid):
        if self.request.files:
            ext = self.request.files["filedata"][0]["filename"].rsplit('.')[-1].lower()
            if ext in ['jpg', 'gif', 'png']:
                filename = '%d%d.%s' % (int(time.time()), random.randint(1000, 9999), ext)
                size = len(self.request.files["filedata"][0]["body"])
                if size<=2*1024*1024:
                    try:
                        user = self.current_user
                        path_dir = 'upload/users'
                        if not os.path.exists(path_dir):
                            os.mkdir(path_dir)
                        with open(path_dir + '/' + filename, "wb") as f:
                            f.write(self.request.files["filedata"][0]["body"])

                        user.portraiturl = '/' + path_dir + '/' + filename
                        user.save()
                        msg = '{"err":"","msg":"/' + path_dir + '/' + filename + '"}'
                        homedir = os.getcwd()
                        oldImgPath = os.path.join(homedir + '/' + path_dir, filename)
                        GenerateMobileImg(oldImgPath)
                    except Exception, e:
                        logging.error(e)
                        msg = '{"err":0,"path":"上传失败"}'
                else:
                    msg = '{"err":0,"msg":"上传图片大小不能超过2M！"}'
            else:
                msg = '{"err":0,"msg":"请上传.jpg,.gif,.png格式图片！"}'
            self.write(msg)
