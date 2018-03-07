#!/usr/bin/env python
# coding=utf8

from handler import StoreBaseHandler,BaseHandler,RequestHandler
from lib.route import route
from model import AdminUser,Product,Category_Store,ProductStandard,AdminLog,Store,User,Inventory_Store,ProductPic,\
    Order,OrderItem,StorePrice,ProductOffline
from bootloader import db
from activity import check_activity
from ajax2 import OrderChangeStatusStore,OrderChangeStatus
import time
import os
import simplejson
import sys
import logging
reload(sys)
sys.setdefaultencoding('utf8')

@route(r'/mobile/store_login', name='mobile_store_login')  # 经销商手机端登录
class MobileStoreLoginHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass
    def options(self):
        pass
    def vrole(self, role,roles):
        userrole = list(roles)
        for n in userrole:
            if role.count(n) > 0:
                return True
        return False
    def post(self):
        result = {"flag":0,"msg":"","data":""}
        try:
            args = simplejson.loads(self.request.body)
            username = args["username"]
            password = args["password"]
            if username and password:
                    quser = AdminUser.select().where(AdminUser.username == username)
                    if quser.count()>0 and quser[0].check_password(password):
                        user=quser[0]
                        if user.isactive == 1:
                            if self.vrole("J",user.roles):
                                if not user.store:
                                    storeid=0
                                else:
                                    storeid=user.store
                                if not user.front_user:
                                    frontuserid=0
                                else:
                                    frontuserid=user.front_user
                                qstore=Store.select().where(Store.id==storeid)
                                qfront_user=User.select().where(User.id==frontuserid)
                                if qstore.count()>0 and qfront_user.count()>0:
                                    user.updatesignin()
                                    result["flag"]=1
                                    result["data"]={
                                        'adminid':user.id,
                                        'storeid':qstore[0].id,
                                        'front_user':user.front_user,
                                        'storename':qstore[0].name,
                                    }
                                else:
                                    result["flag"]=0
                                    result["msg"]="此帐户未关联经销商或经销商未绑定前台用户。"
                            else:
                                result["flag"]=0
                                result["msg"]="此账户没有经销商的登录权限。"
                        else:
                            result["flag"]=0
                            result["msg"]="此账户被禁止登录，请联系管理员。"
                    else:
                        if quser.count()>0:
                            result["flag"]=0
                            result["msg"]="密码错误。"
                        else:
                            result["flag"]=0
                            result["msg"]="此用户不存在"
            else:
                result["flag"]=0
                result["msg"]="请输入用户名或者密码"
        except Exception, e:
            result["flag"]=0
            result["msg"]=e
        self.write(simplejson.dumps(result))

@route(r'/mobile/store_products', name='mobile_store_products')  # app管理下单产品列表
class MobileStoreProductHandler(RequestHandler):
    def check_xsrf_cookie(self):
        pass

    def options(self):
        pass

    def get(self):
        storeid =0 #= self.get_argument("storeid", '0')
        if self.get_argument("storeid", ''):
            storeid=int(self.get_argument("storeid", ''))

        result = {"flag":0,"msg":"","data":""}
        data = []
        try:
            ft = (Product.status >= 1)
            ft = ft & (Product.is_store == 0)
            ft = ft & (Inventory_Store.store == storeid)
            q = Inventory_Store.select(Inventory_Store,ProductStandard, Product).join(Product,
                                                                      on=(
                                                                          Inventory_Store.product == Product.id)).join(ProductStandard,
                                                                      on=(
                                                                          Inventory_Store.product_standard == ProductStandard.id)).where(ft)
            for n in q:
                data.append({
                    'id': n.product.id,
                    'name': n.product.name,
                    'price': n.price,
                    'kc': n.quantity,
                    'unit': '份',
                    'sku': n.product.sku,
                    'standard': n.product_standard.name,
                    'psid': n.product_standard.id,
                    'tags': n.product.tags,
                })
            result["flag"]=1
            result["data"]=data

        except Exception, e:
            result["flag"]=0
            result["msg"]=e
        self.write(simplejson.dumps(result))

@route(r'/mobile/store_version/(\S+)', name='mobile_store_verison')  # 手机端程序更新
class MobileStoreVersionHandler(RequestHandler):
    def check_xsrf_cookie(self):
        pass

    def options(self):
        pass

    def get(self, v):
        lastversion = '0.0.1'
        result = {'version': lastversion, 'baseUrl': ''}
        if not v == lastversion:
            result['baseUrl'] = "http://192.168.1.100:8890/upload/mobile/storeorder" + lastversion + '.zip?r=' + str(
                time.time())
        self.write(simplejson.dumps(result))

@route(r'/store/login', name='store_login')  # 登录
class LoginHandler(BaseHandler):
    def get(self):
        self.render('/store/login.html')
    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)

        if username and password:
            try:
                user = AdminUser.get(AdminUser.username == username)
                if user.check_password(password):
                    if user.isactive == 1:
                        if not user.store:
                            storeid=0
                        else:
                            storeid=user.store
                        if not user.front_user:
                            frontuserid=0
                        else:
                            frontuserid=user.front_user
                        qstore=Store.select().where(Store.id==storeid)
                        qfront_user=User.select().where(User.id==frontuserid)
                        if qstore.count()>0 and qfront_user.count()>0:
                            user.updatesignin()
                            self.session['store'] = user
                            self.session.save()
                            self.redirect("/store/index")
                            return
                        else:
                            self.flash("此帐户未关联经销商或经销商未绑定前台用户。")
                    else:
                        self.flash("此账户被禁止登录，请联系管理员。")
                else:
                    self.flash("密码错误")
            except Exception, e:
                print e
                self.flash("此用户不存在")
        else:
            self.flash("请输入用户名或者密码")

        self.render("/store/login.html", next=self.next_url)

@route(r'/store/logout', name='store_logout')  # 退出
class LogoutHandler(StoreBaseHandler):
    def get(self):
        if "store" in self.session:
            del self.session["store"]
            self.session.save()
        self.render('/store/login.html')

@route(r'/store/index', name='store_index')  # 首页
class IndexHandler(StoreBaseHandler):
    def get(self):
        self.render('/store/index.html')

@route(r'/store/category', name='store_category')  # 分类管理
class CategoryHandler(StoreBaseHandler):
    def get(self):
        store_user = self.get_store_user()
        subquery = Product.select(db.fn.COUNT(Product.id)).where(Product.category_store == Category_Store.id)
        categorys = Category_Store.select(Category_Store, subquery.alias('p_count')).where(Category_Store.store == store_user.store.id).order_by(Category_Store.name)
        if categorys.count() == 0:
            categorys = None
        self.render('store/category/category.html', categorys=categorys, active='categorys')

@route(r'/store/category/(\d+)', name='store_eidt_category')   # 分类管理编辑
class EditCategoryHandler(StoreBaseHandler):
    def get(self, cid):
        if str(cid) == '0':
            c = None
        else:
            c = Category_Store.get(Category_Store.id == cid)

        self.render('store/category/category_edit.html', c=c, active='categorys')

    def post(self, cid):
        store_user = self.get_store_user()
        name = self.get_argument("name", '')
        code = self.get_argument("code", '')
        if cid == '0':
            c = Category_Store()
            self.flash(u"商品分类添加成功")
        else:
            c = Category_Store.get(id=cid)
            self.flash(u"商品分类编辑成功")

        c.name = name
        c.code = code
        c.store = store_user.store.id
        c.save()
        self.redirect("/store/category")

@route(r'/store/products', name='store_products')  # 商品管理
class ProductHandler(StoreBaseHandler):
    def get(self):
        store_user = self.get_store_user()
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        cid = int(self.get_argument("pcategory", 0))
        pagesize = self.settings['admin_pagesize']
        keyword = self.get_argument("keyword", None)
        defaultstandard = self.get_argument("defaultstandard", None)
        status = int(self.get_argument("status", 1))
        ft = (Product.status > 0) & (Product.store == store_user.store.id)

        if cid > 0:
            ft = ft & (Product.category_store == cid)
        if keyword:
            keyw = '%' + keyword + '%'
            ft = ft & (Product.name % keyw)
        if defaultstandard:
            ft = ft & (Product.defaultstandard % defaultstandard)
        ft = ft & (Product.status == status)
        q = Product.select(Product, Category_Store).join(Category_Store).where(ft)
        total = q.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        products = q.order_by(Product.created.desc()).paginate(page, pagesize).aggregate_rows()

        categorys = Category_Store.select().where(Category_Store.store == store_user.store.id)
        print categorys.count()
        self.render('store/product/products.html', products=products, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, categorys=categorys, cid=cid, active='ps', status=status, keyword=keyword,
                    dp=defaultstandard)

@route(r'/store/product/(\d+)', name='store_edit_product')  # 修改产品页
class EditProductHandler(StoreBaseHandler):
    def get(self, pid):
        if pid == '0':
            p = None
            ps = None
        else:
            p = Product.get(Product.id == pid)
            ps = ProductStandard.get(ProductStandard.id == p.defaultstandard)
        categorys = Category_Store.select().where(Category_Store.store == self.get_store_user().store.id)
        self.render('store/product/product_edit.html', p=p, ps=ps, categorys=categorys, active='ps')

    def post(self, pid):
        store_user = self.get_store_user()
        resume = self.get_argument("presume", '')
        name = self.get_argument("pname", '')
        tags = self.get_argument("tags", '')
        intro = self.get_argument("pintro", '')
        quantity = float(self.get_argument("quantity", '0'))
        producer = self.get_argument("pproducer", '')
        metakeywords = self.get_argument("pmetakeywords", '')
        metadescription = self.get_argument("pmetadescription", '')
        metatitle = self.get_argument("pmetatitle", '')
        category = int(self.get_argument("pcategory", '1'))
        quality = self.get_argument("quality", '')
        standard = self.get_argument("standard", '')
        status = self.get_argument("standard", '1')
        prompt = self.get_argument("prompt", '')

        psname = self.get_argument("sname", '')
        psprice = float(self.get_argument("sprice", '0'))
        content = {}
        sku = int(time.time())
        try:
            if pid == '0':
                p = Product()
                p.sku = str(sku)
                if not os.path.exists('upload/' + p.sku):
                    os.mkdir('upload/' + p.sku)
                p.created = int(time.time())
                p.categoryback = 1
                content['operatetype'] = '创建产品'
            else:
                p = Product.get(Product.id == pid)
                content['operatetype'] = '修改产品'
                content['oldproduct'] = simplejson.dumps(str(p))
            p.args = 'C'
            p.categoryfront = 166   #数据库内置分类   经销商
            p.updatedtime = int(time.time())
            p.updatedby = self.get_store_user()
            p.resume = resume
            p.name = name
            p.tags = tags
            p.intro = intro
            p.producer = producer
            p.metakeywords = metakeywords
            p.metadescription = metadescription
            p.metatitle = metatitle
            p.marketprice = 0
            p.quantity = quantity
            p.quality = quality
            p.standard = standard
            p.xgperusernum = 50
            p.xgtotalnum = 99999
            p.status = int(status)  # 默认上架
            p.store = store_user.store.id
            p.is_store = 1
            p.category_store = category
            p.prompt = prompt
            p.validate()
            p.save()
            if pid == '0':
                s = ProductStandard()
            else:
                s = ProductStandard.get(ProductStandard.id == p.defaultstandard)
            s.name = psname
            s.tags = ''
            s.price = psprice
            s.orginalprice = psprice
            s.weight = 0
            s.ourprice = psprice
            s.relations = []
            s.product = p
            s.save()
            s.relations = '[' + str(s.id) + ']'
            s.save()
            p.defaultstandard = s.id
            p.save()
            self.flash("保存成功")
            content['pid'] = p.id
            AdminLog.create(user=self.get_store_user(), dotime=int(time.time()), content=content)
            self.redirect('/store/product/' + str(p.id))
        except Exception, e:
            self.flash("保存失败，请联系管理员" + e.message)
            self.redirect('/store/product/0')
            
@route(r'/store/primarypic/(\d+)', name='store_primarypic')  # 设置产品图片
class DelPicHandler(StoreBaseHandler):
    def get(self, pcid):
        p = ProductPic.get(ProductPic.id == pcid)
        content = {}
        content['operatetype'] = '设置主图'
        content['pcid'] = pcid
        content['old_path'] = p.product.cover
        content['current_path'] = p.path
        p.product.cover = p.path
        p.product.updatedtime = int(time.time())
        p.product.updatedby = self.get_store_user()
        p.product.save()
        AdminLog.create(user=self.get_store_user(), dotime=int(time.time()), content=content)
        self.redirect('/store/product/' + str(p.product.id))

@route(r'/store/delpic/(\d+)', name='store_delpic')  # 删除产品图片
class DelPicHandler(StoreBaseHandler):
    def get(self, pcid):
        p = ProductPic.get(ProductPic.id == pcid)
        content = {}
        content['operatetype'] = '删除产品图片'
        content['pcid'] = pcid
        content['path'] = p.path
        pid = p.product.id
        p.delete_instance()
        AdminLog.create(user=self.get_store_user(), dotime=int(time.time()), content=content)
        self.redirect('/store/product/' + str(pid))

@route(r'/store/changeproduct/(\d+)/(\d+)', name='store_changeproduct')  # 修改产品状态
class StatusProductHandler(StoreBaseHandler):
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
        p.updatedtime = int(time.time())
        p.updatedby = self.get_store_user()
        p.save()
        AdminLog.create(user=self.get_store_user(), dotime=int(time.time()), content=content)
        self.redirect('/store/products?page=' + str(page) + '&pcategory=' + str(cid) + '&keyword='+ keyword +
                      '&defaultstandard=' + str(ds) + '&status=' + str(s))

@route(r'/store/password', name='store_password')  # 密码管理
class PasswordHandler(StoreBaseHandler):
    def get(self):
        self.render('/store/password.html', active='password')

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
                user = self.get_store_user()
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
        self.redirect('/store/password')

@route(r'/store/orders', name='store_orders')  # 订单管理
class OrderHandler(StoreBaseHandler):
    def get(self):
        store_user = self.get_store_user()
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        status = int(self.get_argument("status", -1))
        pagesize = self.settings['admin_pagesize']
        ft = (Order.status > -1)
        keyword = self.get_argument("keyword", '')
        begindate = self.get_argument("begindate", '')
        enddate = self.get_argument("enddate", '')
        statuscheck = int(self.get_argument("statuscheck", '-1') if len(self.get_argument("statuscheck", '1')) > 0 else '-1')
        phone = self.get_argument("phone", '')

        ft = ft & (Order.store == store_user.store.id)
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
        self.render('/store/order/orders.html', orders=orders, total=total, page=page, pagesize=pagesize,
        totalpage=totalpage, status=status, active='orders',begindate=begindate,enddate=enddate,keyword=keyword,
        phone=phone)

@route(r'/store/order/(\d+)', name='store_order_detail')  # 订单详情
class OrderDetailHandler(StoreBaseHandler):
    def get(self, oid):
        o = Order.get(id=oid)
        self.render('/store/order/order_detail.html', o=o, active='orders')

@route(r'/store/category/list/(\d+)', name='store_categorys_list')  # 分类产品列表管理
class CategoryListHandler(StoreBaseHandler):
    def get(self, cid):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']

        category = Category_Store.get(id=cid)

        ft = ((Product.status > 0) & (Product.category_store == category))
        q = Product.select().where(ft)
        total = q.count()

        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        products = q.paginate(page, pagesize)

        self.render('/store/category/category_product.html', products=products, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, category=category, active='categorys')

@route(r'/store/inventory', name='store_inventory')  # 库存管理
class StoreInventoryHandler(StoreBaseHandler):
    def get(self):
        keyword=self.get_argument("keyword","").strip()
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']
        ft = (Product.status >= 1)
        ft = ft & (Product.is_store == 0)
        ft = ft & (ProductOffline.status == 2)
        ft = ft & (ProductOffline.store == self.get_store_user().store)
        if keyword:
            keyw = '%' + keyword.replace("'","''") + '%'
            ft = ft & (Product.name % keyw)
        q = ProductOffline.select(Product.id,ProductOffline.store,Product.name,db.fn.COUNT(ProductOffline.product).alias('quantity')).join(Product,
                on=(
                     ProductOffline.product == Product.id)).where(ft).group_by(ProductOffline.product)
        total = q.count()

        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        inventorys = q.paginate(page, pagesize)
        store=self.get_store_user()
        self.render('store/inventory/list.html', inventorys=inventorys, total=total, page=page, pagesize=pagesize,
        totalpage=totalpage,  active='inventory',store=store,keyword=keyword)

@route(r'/store/inventory/(\d+)', name='store_inventory_offline')  # 产品库存详细
class StoreInventoryHandler(StoreBaseHandler):
    def get(self,product_id):
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        pagesize = self.settings['admin_pagesize']

        ft = (Product.status >= 1)
        ft = ft & (Product.is_store == 0)
        ft = ft & (ProductOffline.status == 2)
        ft = ft & (ProductOffline.store == self.get_store_user().store)
        ft = ft & (ProductOffline.product == product_id)
        q = ProductOffline.select(ProductOffline,Product).join(Product,
                on=(
                     ProductOffline.product == Product.id)).where(ft).order_by(ProductOffline.in_time.desc())
        total = q.count()

        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        inventorys = q.paginate(page, pagesize)
        store=self.get_store_user()
        self.render('store/inventory/list_offline.html', inventorys=inventorys, total=total, page=page, pagesize=pagesize,
        totalpage=totalpage,  active='inventory',store=store,product_id=product_id)

@route(r'/store/price', name='store_price')  # 库存价格管理
class StoreInventoryHandler(StoreBaseHandler):
    def get(self):
        keyword=self.get_argument("keyword","").strip()
        page = int(self.get_argument("page", '1') if len(self.get_argument("page", '1')) > 0 else '1')
        fillprice = int(self.get_argument("fillprice", '0') if len(self.get_argument("fillprice", '0')) > 0 else '0')
        pagesize = self.settings['admin_pagesize']

        ft = (Product.status >= 1)
        ft = ft & (Product.is_store == 0)
        ft = ft & (StorePrice.store ==1 )#self.get_store_user().store 使用枫林绿洲的价格
        ftunprice=ft
        ftunprice = ftunprice & (StorePrice.price <= 0)
        if fillprice>0:
            ft = ft & (StorePrice.price <= 0)
        if keyword:
            keyw = '%' + keyword.replace("'","''") + '%'
            ft = ft & (Product.name % keyw)
        q = StorePrice.select(StorePrice,ProductStandard,Product).join(Product,
                                                                  on=(
                                                                      StorePrice.product == Product.id)).join(ProductStandard,
                                                                  on=(
                                                                      StorePrice.product_standard == ProductStandard.id)).where(ft).order_by(Product.status)
        total = q.count()

        qunprice = StorePrice.select(StorePrice,ProductStandard,Product).join(Product,
                                                                  on=(
                                                                      StorePrice.product == Product.id)).join(ProductStandard,
                                                                  on=(
                                                                      StorePrice.product_standard == ProductStandard.id)).where(ftunprice)
        totalunprice = qunprice.count()

        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        inventorys = q.paginate(page, pagesize)
        store=self.get_store_user()
        self.render('store/inventory/price.html', inventorys=inventorys, total=total, page=page, pagesize=pagesize,
        totalpage=totalpage,  active='store_price',store=store,fillprice=fillprice,keyword=keyword,totalunprice=totalunprice)
