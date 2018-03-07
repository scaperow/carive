#!/usr/bin/env python
# coding=utf8
import simplejson
from lib.route import route
from model import ProductStandard,Product,CategoryFront,ProductOffline,StorePrice,Store
from tornado.web import RequestHandler
from handler import OfflineHandler
from bootloader import db
import time

@route(r'/offline/login', name='offline_login')  # 手机端登录
class OfflineLoginHandler(OfflineHandler):
    def check_xsrf_cookie(self):
        pass

    def options(self):
        pass

    def post(self):
        result = self.get_offline_user()
        self.write(simplejson.dumps(result))


@route(r'/offline/products', name='offline_products')  # 商品列表
class OfflineProductsHandler(RequestHandler):
    def check_xsrf_cookie(self):
        pass

    def options(self):
        pass

    def get(self):
        sid = int(self.get_argument("sid", '1'))
        result = []

        # ft = (Product.is_store == 0)
        # qq = ProductStandard.select(ProductStandard, Product).join(Product,
        #                                                           on=(ProductStandard.id == Product.defaultstandard)). \
        #     join(CategoryFront, on=(Product.categoryfront == CategoryFront.id)).where(ft)
        q = StorePrice.select(StorePrice,ProductStandard,Product).join(ProductStandard, on=(ProductStandard.id == StorePrice.product_standard)).\
            join(Product, on=(Product.id == StorePrice.product)).where(StorePrice.store == sid)
        for n in q:
            result.append({
                'ID': n.product.id,
                'SKU': n.product.sku,
                'FullName': n.product.name,
                'ShotName': '',
                'ShotKey': '',
                'Price': n.price,
                'StoreID': sid,
                'PY': n.product.tags,
                'Standard': n.product_standard.name,
                'Status': n.product.status
            })
        self.write(simplejson.dumps(result))


@route(r'/offline/add_product', name='offline_add_product')  # 添加线下商品
class OfflineAddProductHandler(OfflineHandler):
    def check_xsrf_cookie(self):
        pass

    def options(self):
        pass

    def post(self):
        result = '0'
        # args = simplejson.loads(self.request.body)
        try:
            pid = self.get_argument("pid")
            store = self.get_argument("store", None)
            barcode = self.get_argument("barcode")
            status = int(self.get_argument("status", '0'))
            weight = float(self.get_argument("weight", '0.0'))
            price = float(self.get_argument("price", '0.0'))
            out_time = self.get_argument("out_time", '0')
            in_time = self.get_argument("in_time", '0')
            sale_time = 0
            if store and store == '0':
                store = None
            if status  <= 1:
                store=None

            q=ProductOffline.select().where(ProductOffline.barcode==barcode)
            if q.count()<=0:
                ProductOffline.create(product=int(pid), store=store, barcode=barcode, status=status, weight=weight,
                                       price=price, out_time=out_time, in_time=in_time, sale_time=sale_time, cancel_reason='',cancel_time=0)
            else:
                q[0].product=int(pid)
                q[0].weight=weight
                q[0].price=price
                q[0].save()
            result = '1'
        except Exception, e:
            result = '0'
        self.write(result)


@route(r'/offline/get_product', name='offline_get_product')  # 根据条形码获取产品信息
class OfflineGetProductHandler(RequestHandler):
    def check_xsrf_cookie(self):
        pass

    def options(self):
        pass

    def get(self):
        result = {'flag': '0', 'msg': '', 'data': ''}
        barcode = self.get_argument("barcode")
        storeid = int(self.get_argument("storeid", '0') if len(self.get_argument("storeid", '0')) > 0 else '0')
        q = ProductOffline.select().where(ProductOffline.barcode == barcode)
        if q.count() > 0:
            qSP=StorePrice.select().where((StorePrice.store==1)&(StorePrice.product==q[0].product.id))
            if qSP.count()>0:
                PrePrice=qSP[0].price
                result['flag'] = 1
                result['data'] = {
                    'id': q[0].id,
                    'sku': q[0].product.sku,
                    'name': q[0].product.name,
                    'weight': q[0].weight,
                    'price': q[0].price,
                    'PrePrice': PrePrice,
                    'status': q[0].status
                }
            else:
                result['flag'] = 0
                result['msg'] = '根据店铺ID'+str(storeid)+'和产品ID'+str(q[0].product.id)+'未获取到价格。'
        else:
            result['flag'] = 0
            result['msg'] = '没有查询到任何信息。'
        self.write(simplejson.dumps(result))

@route(r'/offline/set_product_status', name='offline_set_product_status')  # 设置线下产品状态
class OfflineGetProductHandler(RequestHandler):
    def check_xsrf_cookie(self):
        pass

    def options(self):
        pass

    def post(self):
        result = {'msg': '', 'flag': 0, 'data': 0}
        barcode = self.get_argument("barcode")
        status = self.get_argument("status")
        storeid = int(self.get_argument("storeid", '0') if len(self.get_argument("storeid", '0')) > 0 else '0')
        price = self.get_argument("price")
        weight = self.get_argument("weight")
        product = self.get_argument("product")
        msg = self.get_argument("msg")
        q = ProductOffline.select().where(ProductOffline.barcode == barcode)

        if q.count() > 0:
            qSP=StorePrice.select().where((StorePrice.store==1)&(StorePrice.product==q[0].product.id))
            if qSP.count()>0:
                PrePrice=qSP[0].price
                if product and product != '0':
                    q[0].product = product
                if price and price != '0':
                    q[0].price = price
                if weight and weight != '0':
                    q[0].weight = weight
                if int(status) >= 0:
                    q[0].status = status
                if storeid and storeid != 0:
                    q[0].store = storeid
                if status == '4' or status == '5':
                    q[0].cancel_reason = msg
                    q[0].cancel_time = int(time.time()) # 取消时间
                elif status == '3':
                    q[0].sale_time = int(time.time())   # 售出时间
                elif status == '2':
                    q[0].in_time = int(time.time())     # 入门店时间
                elif status == '1':
                    q[0].out_time = int(time.time())    # 出仓库时间
                q[0].save()
                result['flag'] = 1
                result['data'] = {
                    'id': q[0].id,
                    'sku': q[0].product.sku,
                    'name': q[0].product.name,
                    'weight': q[0].weight,
                    'price': q[0].price,
                    'PrePrice': PrePrice,
                    'status': q[0].status
                }
            else:
                result['flag'] = 0
                result['msg'] = '根据店铺ID'+storeid+'和产品ID'+str(q[0].product.id)+'未获取到价格。'
        else:
            result['msg'] = '没有查询到任何信息，请重试！'
        self.write(simplejson.dumps(result))

@route(r'/offline/stores', name='offline_stores')  # 线下店铺列表
class OfflineStoresHandler(RequestHandler):
    def check_xsrf_cookie(self):
        pass

    def options(self):
        pass

    def get(self):
        result = []
        q = Store.select().where(Store.status == 1)
        for n in q:
            result.append({
                'ID': n.id,
                'Name': n.name
            })
        self.write(simplejson.dumps(result))

@route(r'/offline/max_barcode', name='offline_max_barcode')  # 线下店铺列表
class GetMaxBarcodeHandler(RequestHandler):
    def check_xsrf_cookie(self):
        pass

    def options(self):
        pass

    def get(self):
        barcode = self.get_argument("barcode")
        code = barcode[0:4] + '%'
        q = ProductOffline.select(db.fn.Max(ProductOffline.barcode).alias('barcode')).where(ProductOffline.barcode % code)
        if q.count() > 0:
            self.write(q[0].barcode[4:12])
        else:
            self.write(barcode[4:12])