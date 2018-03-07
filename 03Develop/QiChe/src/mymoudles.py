#!/usr/bin/env python
#coding=utf8

from tornado.web import UIModule
from model import PageBlock,Cart,Product,ProductStandard,Hot_Search,Gift,Store,Product_Reserve,CategoryFront
import simplejson
import copy
import time
from handler.activity import check_activity
from bootloader import db

class ShowMenu(UIModule):
    def render(self):
        categories1 = CategoryFront.select().where((CategoryFront.isactive == 1) & (db.fn.Length(CategoryFront.code) == 4))
        categories2 = CategoryFront.select().where((CategoryFront.isactive == 1) & (db.fn.Length(CategoryFront.code) == 8))
        categories3 = CategoryFront.select().where((CategoryFront.isactive == 1) & (db.fn.Length(CategoryFront.code) == 12))

        text1 = ''
        for n in categories1:
            if len(n.code) == 4:
                text1 += '<dt class="top-category tyre-label"><a href="/category/'+n.code+'">'+n.name+' </a><s></s></dt>'
                text1 += '<dd class="list-all grid-15"><dl class="option-list">'
                for c in categories2:
                    if (len(c.code) == 8) & (c.code[0:4] == n.code):
                        text1 += '<dt>'+c.name+'</dt>'
                        text1 += '<dd>'
                        for cc in categories3:
                            if (len(cc.code) == 12) & (cc.code[0:8] == c.code):
                                text1 += '<a href="/category/'+cc.code+'">'+ cc.name +'</a> '
                        text1 += '<div class="clear"></div></dd>'
                text1 += '</dl></dd>'

        return text1

class KeyWords(UIModule):
    def render(self):
        hot_search = Hot_Search.select().where(Hot_Search.status == 1).order_by(Hot_Search.quantity.desc(),Hot_Search.last_time.desc()).limit(10)
        return hot_search

class MyCart(UIModule):
    def render(self):
        user = self.current_user
        client_car = self.handler.get_secure_cookie('car',None)
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
                    c1.save()
            cartitems =  Cart.select().where((Cart.user == self.current_user.id)) # & (Cart.type != 2)
            self.handler.clear_cookie('car')
            for i in cartitems:
                c = copy.deepcopy(carproduct)
                c['name'] = i.product.name
                pa = check_activity(i.product.id)
                if pa:
                    c['price'] = pa["price"]
                    c['quantity'] = 1
                    c['is_activity'] = 1
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
                c['psid'] = i.product_standard.id
                c['imgurl'] = i.product.cover
                c['pid'] = i.product.id
                c['sku'] = i.product.sku
                c['psid'] = i.product_standard.id
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
                pa = check_activity(i['pid'])
                if pa:
                    c['price'] = pa["price"]
                    c['quantity'] = 1
                    c['is_activity'] = 1
                else:
                    c['price'] = ps.price
                    c['quantity'] = i['quantity']
                c['oprice'] = ps.orginalprice
                c['standardname'] = ps.name
                c['psid'] = ps.id
                c['imgurl'] = p.cover
                c['pid'] = i['pid']
                c['sku'] = p.sku
                c['psid'] = i['psid']
                totalprice += float(ps.price) * float(i['quantity'])
                count += int(i['quantity'])
                list.append(c)
        return self.render_string("layout/mycart.html", cartitems=list,count=count, gift_items=giftItems, totalprice=totalprice)

class StoreName(UIModule):
    def render(self):
        client_store = self.handler.get_secure_cookie('store', None)
        if client_store:
            sid = simplejson.loads(client_store)
            s = Store.get(Store.id == sid)
            name = s.name
        else:
            name = u'实体店'
        return name