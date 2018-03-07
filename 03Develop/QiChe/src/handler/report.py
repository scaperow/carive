#!/usr/bin/env python
# coding=utf8

import os
import time
import simplejson
from handler import AdminBaseHandler
from lib.route import route
from model import UserVcode, Cart, UserAddr, Product, ProductPic, CategoryFront, Order, User, Fav, AdminLog, Invoicing, \
    Coupon, \
    CouponTotal, Balance, Coupon, ProductStandard, DeliveryNumbers, OrderItem, GroupOrder, \
    Score, \
    Inventory, PayBack, InvoicingChanged
from bootloader import db
import tornado.gen
from tornado.concurrent import run_on_executor
# 这个并发库在python3自带在python2需要安装sudo pip install futures
from concurrent.futures import ThreadPoolExecutor
import tornado.web


def get_cg_price(ps, timepoint):
    products = Product.select().where(Product.defaultstandard << simplejson.loads(ps.relations))
    unitprice = None
    invo = Invoicing.select(Invoicing.unitprice).where((Invoicing.product << products) & (Invoicing.status == 0) &
                                                       (Invoicing.addtime < time.mktime(timepoint) + 24*60*60) &
                                                       (Invoicing.type == 0) & (Invoicing.args=='A' | Invoicing.args=='B')).order_by(Invoicing.id.desc()).limit(1)
    if invo.count() == 0:
        invo = Invoicing.select(Invoicing.unitprice).where((Invoicing.product << products) & (Invoicing.status == 0) &
                                                       (Invoicing.addtime >= time.mktime(timepoint) + 24*60*60) &
                                                       (Invoicing.type == 0) & (Invoicing.args=='A' | Invoicing.args=='B')).order_by(Invoicing.id).limit(1)
    if invo.count() == 1:
        unitprice = invo[0].unitprice
    return unitprice


def get_sx_fee(price):
    fee = 1
    if price > 100:
        fee = round(price*0.01, 2)
    return fee

@route(r'/admin/report/summary', name='admin_report_summary')  # 报表，汇总信息
class ReportSummaryHandler(AdminBaseHandler):
    executor = ThreadPoolExecutor(2)
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        date = self.get_argument('begindate', '')
        report = yield self.getreport(date)
        self.render('admin/report/summary.html', report=report, begindate=date, active='r_summary')

    @run_on_executor
    def getreport(self, date):
        report = {}
        ft = (Invoicing.type == 0) & (Invoicing.status == 0)
        if date:
            begindate = time.strptime(date, "%Y-%m-%d")
            enddate = time.strptime((date + " 23:59:59"), "%Y-%m-%d %H:%M:%S")
            ft = ft & (Invoicing.addtime >= time.mktime(begindate)) & (Invoicing.addtime < time.mktime(enddate))
        else:
            begindate = time.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
            enddate = time.strptime(time.strftime('%Y-%m-%d 23:59:59', time.localtime(time.time())),
                                    "%Y-%m-%d %H:%M:%S")
            ft = ft & (Invoicing.addtime >= time.mktime(begindate)) & (Invoicing.addtime < time.mktime(enddate))
            # ft = ft & (Invoicing.addtime == time.mktime(begindate))
        try:
            report['day_sc_sc_price'] = round((sum([n['price'] for n in (Invoicing.select(Invoicing.price).join(Product).where(
                ft & (Invoicing.args == "A") & (Invoicing.product == Product.id) & (Product.sku % '02%')).dicts())])),2)
            report['day_sc_sg_price'] = round((sum([n['price'] for n in (Invoicing.select(Invoicing.price).join(Product).where(
                ft & (Invoicing.args == "A") & (Invoicing.product == Product.id) & (Product.sku % '01%')).dicts())])),2)
            report['day_sc_price'] = round((sum(
                [n['price'] for n in (Invoicing.select(Invoicing.price).where(ft & (Invoicing.args == "A")).dicts())])),2)
            report['day_sc_sc_weight'] = round((sum([n['quantity'] for n in (
                Invoicing.select(Invoicing.quantity).join(Product).where(
                    ft & (Invoicing.args == "A") & (Invoicing.product == Product.id) & (Product.sku % '02%')).dicts())])),2)
            report['day_sc_sg_weight'] = round((sum([n['quantity'] for n in (
                Invoicing.select(Invoicing.quantity).join(Product).where(
                    ft & (Invoicing.args == "A") & (Invoicing.product == Product.id) & (Product.sku % '01%')).dicts())])),2)
            report['day_sc_weight'] = round((sum([n['quantity'] for n in (
                Invoicing.select(Invoicing.quantity).where(ft & (Invoicing.args == "A")).dicts())])),2)

            report['day_zc_sc_price'] = round((sum([n['price'] for n in (Invoicing.select(Invoicing.price).join(Product).where(
                ft & (Invoicing.args == "B") & (Invoicing.product == Product.id) & (Product.sku % '02%')).dicts())])),2)
            report['day_zc_sg_price'] = round((sum([n['price'] for n in (Invoicing.select(Invoicing.price).join(Product).where(
                ft & (Invoicing.args == "B") & (Invoicing.product == Product.id) & (Product.sku % '01%')).dicts())])),2)
            report['day_zc_price'] = round((sum(
                [n['price'] for n in (Invoicing.select(Invoicing.price).where(ft & (Invoicing.args == "B")).dicts())])),2)
            report['day_zc_sc_weight'] = round((sum([n['quantity'] for n in (
                Invoicing.select(Invoicing.quantity).join(Product).where(
                    ft & (Invoicing.args == "B") & (Invoicing.product == Product.id) & (Product.sku % '02%')).dicts())])),2)
            report['day_zc_sg_weight'] = round((sum([n['quantity'] for n in (
                Invoicing.select(Invoicing.quantity).join(Product).where(
                    ft & (Invoicing.args == "B") & (Invoicing.product == Product.id) & (Product.sku % '01%')).dicts())])),2)
            report['day_zc_weight'] = round((sum([n['quantity'] for n in (
                Invoicing.select(Invoicing.quantity).where(ft & (Invoicing.args == "B")).dicts())])), 2)
            order_status = (Order.status < 5) & (((Order.status > -1) & (Order.payment == 0)) | ((Order.status > 0) & (Order.payment > 0)))

            order_date = (Order.ordered >= time.mktime(begindate)) & (Order.ordered <= time.mktime(enddate))

            day_orders_price = (Order.select(db.fn.Sum(Order.currentprice)).where(order_date & order_status & (Order.payment != 9))).scalar()
            report['day_orders_price'] = round((day_orders_price if day_orders_price else 0.0), 2)
            hbcount = (Order.select(db.fn.Count(db.fn.Distinct(Order.deliverynum))).where(order_date & order_status & (Order.payment != 9) & (Order.deliverynum != '') & (~(Order.deliverynum >> None))).scalar())
            singlecount = (Order.select(db.fn.Count(Order.id)).where(order_date & order_status & (Order.payment != 9) & ((Order.deliverynum == '') | (Order.deliverynum >> None))).scalar())
            report['day_orders_count'] = hbcount + singlecount

            report['day_users_count'] = Order.select(db.fn.Count(db.fn.Distinct(Order.user))).where(order_date & order_status & (Order.payment != 9)).scalar()

            day_orders_budan = Order.select().where(order_date & order_status & (Order.payment == 9))
            report['day_orders_budan_count'] = day_orders_budan.count()
            report['day_orders_budan_price'] = round((sum(n['currentprice'] for n in day_orders_budan.dicts())),2)
            day_total_weight = OrderItem.select(ProductStandard.weight, OrderItem.quantity).join(Order, on=(
                                                                                                               OrderItem.order == Order.id) & order_date & (
                                                                                                               order_status)).join(
                ProductStandard, on=(OrderItem.product_standard == ProductStandard.id))
            psWeight = round((sum(round((n['weight'] / 500 * n['quantity']), 2) for n in day_total_weight.dicts())),2)
            report['day_total_weight'] = psWeight
            sales_price = OrderItem.select().join(
                Order, on=(Order.id == OrderItem.order)).where(order_date & (order_status))
            day_sales_price = 0
            for p in sales_price:
                unitprice = get_cg_price(p.product_standard, enddate)
                if unitprice:
                    day_sales_price += ((unitprice * p.weight / 500) * p.quantity)
                else:
                    day_sales_price += (p.price * p.quantity)

            report['day_sales_price'] = round(day_sales_price, 2)
            report['day_inventory_weight'] = round((sum(round(n['quantity']) for n in Product.select(Product.quantity).dicts())),2)
            report['day_inventory_sc'] = round((sum(
                [n['quantity'] for n in Product.select(Product.quantity).where(Product.sku % '02%').dicts()])),2)
            report['day_inventory_sg'] = round((sum(
                [n['quantity'] for n in Product.select(Product.quantity).where(Product.sku % '01%').dicts()])),2)
            report['day_inventory_bc'] = 0
            report['day_total_cb'] = 0

            freight = Order.select(Order.freight).where(order_date & (order_status))
            report['day_wl_fee'] = round((sum([n['freight'] or 0 for n in freight.dicts()])),2)
            report['day_dsf_fee'] = 0
            report['day_rgf_weight'] = '0.00'
            report['day_car_fee'] = '0.00'
            report['day_xhf_weight'] = 0
            report['day_bc_fee'] = '0.00'
            report['day_total_qtcb'] = report['day_wl_fee'] + report['day_dsf_fee'] + float(report['day_rgf_weight']) + float(report[
                'day_car_fee']) + report['day_xhf_weight'] + float(report['day_bc_fee'])

        except Exception, e:
            print e
        return report


@route(r'/admin/report/user', name='admin_report_user')  # 会员报告
class ReportUserHandler(AdminBaseHandler):
    def get(self):
        begindate = self.get_argument('begindate', '')
        enddate = self.get_argument('enddate', '')
        if not begindate:
            beginvalue = time.mktime(time.strptime('2015-01-13', "%Y-%m-%d"))
        else:
            beginvalue = time.mktime(time.strptime(begindate, "%Y-%m-%d"))
        if not enddate:
            endvalue = time.time()
        else:
            endvalue = time.mktime(time.strptime(enddate, "%Y-%m-%d")) + 24*60*60

        ft = (User.isactive == 1) & (User.signuped >= beginvalue) & (User.signuped < endvalue)
        report_u = {'ordercount':[], 'fees':[], 'lv':[]}
        last30day = time.time()-30*24*60*60
        report_u['usertotal'] = (User.select(db.fn.Count(User.id)).where(ft)).scalar()
        report_u['userphone'] = (User.select(db.fn.Count(User.id)).where(ft & (User.phoneactived==1))).scalar()
        report_u['userweb'] = (User.select(db.fn.Count(User.id)).where(ft & (User.phoneactived==0))).scalar()
        report_u['unlogin'] = (User.select(db.fn.Count(User.id)).where(ft & (User.lsignined < last30day ))).scalar()
        sql = '''SELECT count(distinct a.id) FROM tb_users a
                join tb_orders b on a.id = b.user_id where ((b.status>-1 and b.payment=0) or
                (b.payment>0 and b.status>0) ) and b.payment<9 and b.status<5
                and a.signuped>=%s and a.signuped<%s'''

        q = db.handle.execute_sql(sql % (beginvalue, endvalue))
        report_u['userordered'] = q.fetchone()[0]

        sql = '''
        SELECT a.id, a.username,count(a.id) as ct FROM tb_users a
        join tb_orders b on a.id = b.user_id where ((b.status>-1 and b.payment=0) or (b.payment>0 and b.status>0) ) and b.payment<9
        and a.signuped>=%s and a.signuped<%s and b.status<5
        group by a.id,a.username order by ct desc limit 5
        '''
        q = db.handle.execute_sql(sql % (beginvalue, endvalue))
        for row in q.fetchall():
            report_u['ordercount'].append({'id':row[0], 'phone':row[1], 'count':row[2]})

        sql = '''
        SELECT a.id,a.username,sum(b.currentprice) as price FROM tb_users a
        join tb_orders b on a.id = b.user_id where ((b.status>-1 and b.payment=0) or (b.payment>0 and b.status>0) ) and b.payment<9
        and a.signuped>=%s and a.signuped<%s and b.status<5
        group by a.id,a.username order by price desc limit 5
        '''

        q = db.handle.execute_sql(sql % (beginvalue, endvalue))
        for row in q.fetchall():
            report_u['fees'].append({'id':row[0], 'phone':row[1], 'price':round(row[2],2)})

        sql = '''
        select x.lv,count(x.username) as ct from (
        SELECT a.username,a.signuped,count(a.id) as ct, ceil(((%s-a.signuped)/(24*60*60))/count(a.id)) as lv  FROM tb_users a
        join tb_orders b on a.id = b.user_id where ((b.status>-1 and b.payment=0) or (b.payment>0 and b.status>0) ) and b.payment<9
        and a.signuped>=%s and a.signuped<%s and b.status<5
        group by a.signuped,a.username  ) x group by x.lv order by x.lv
        '''
        # now = time.time()
        # q = db.handle.execute_sql(sql % (now, beginvalue, endvalue))
        # for row in q.fetchall():
        #     report_u['lv'].append({'speed':row[0], 'count':row[1], 'lv':round(row[1]*100.0/report_u['usertotal'],2)})

        self.render('admin/report/r_user.html', begindate=begindate,enddate=enddate, report_u=report_u, active='r_user')


@route(r'/admin/report/user/pop', name='admin_report_user_pop')  # 用户报表弹出页面
class ReportUserPopHandler(AdminBaseHandler):
    def get(self):
        begindate = self.get_argument('begindate', '')
        enddate = self.get_argument('enddate', '')
        type = int(self.get_argument('type', '1'))
        page = int(self.get_argument("page", 1))
        pagesize = self.settings['admin_pagesize']
        if not begindate:
            beginvalue = time.mktime(time.strptime('2015-01-13', "%Y-%m-%d"))
        else:
            beginvalue = time.mktime(time.strptime(begindate, "%Y-%m-%d"))
        if not enddate:
            endvalue = time.time()
        else:
            endvalue = time.mktime(time.strptime(enddate, "%Y-%m-%d")) + 24*60*60

        if type == 1:
            countsql = ''' select count(m.id) as ct from (
            SELECT a.id FROM tb_users a
            join tb_orders b on a.id = b.user_id where ((b.status>-1 and b.payment=0) or (b.payment>0 and b.status>0) ) and b.payment<9
            and a.signuped>=%s and a.signuped<%s and b.status<5
            group by a.id,a.username) m
            '''

            sql = '''
            SELECT a.id, a.username,count(a.id) as ct FROM tb_users a
            join tb_orders b on a.id = b.user_id where ((b.status>-1 and b.payment=0) or (b.payment>0 and b.status>0) ) and b.payment<9
            and a.signuped>=%s and a.signuped<%s and b.status<5
            group by a.id,a.username order by ct desc limit %s,%s
            '''
        else:
            countsql = ''' select count(m.id) as ct from (
            SELECT a.id FROM tb_users a
            join tb_orders b on a.id = b.user_id where ((b.status>-1 and b.payment=0) or (b.payment>0 and b.status>0) ) and b.payment<9
            and a.signuped>=%s and a.signuped<%s and b.status<5
            group by a.id,a.username) m
            '''
            sql = '''
            SELECT a.id,a.username,sum(b.currentprice) as price FROM tb_users a
            join tb_orders b on a.id = b.user_id where ((b.status>-1 and b.payment=0) or (b.payment>0 and b.status>0) ) and b.payment<9
            and a.signuped>=%s and a.signuped<%s and b.status<5
            group by a.id,a.username order by price desc limit %s,%s
            '''

        q = db.handle.execute_sql(countsql % (beginvalue, endvalue))

        total = q.fetchone()[0]
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        q = db.handle.execute_sql(sql % (beginvalue, endvalue, (page if page==0 else page-1)*pagesize, pagesize))
        list = []

        for row in q.fetchall():
            list.append({'id':row[0], 'phone':row[1], 'value':(row[2] if type==1 else round(row[2],2))})

        self.render('/admin/report/r_user_pop.html', list=list, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage,type=type,begindate=begindate,enddate=enddate)


@route(r'/admin/report/userchart', name='admin_report_user_chart')  # 用户数量曲线图
class ReportUserChartHandler(AdminBaseHandler):
    def get(self):
        begindate = self.get_argument('begindate', '')
        enddate = self.get_argument('enddate', '')
        if not begindate:
            beginvalue = time.mktime(time.strptime('2015-01-13', "%Y-%m-%d"))
        else:
            beginvalue = time.mktime(time.strptime(begindate, "%Y-%m-%d"))
        if not enddate:
            endvalue = time.time()
        else:
            endvalue = time.mktime(time.strptime(enddate, "%Y-%m-%d")) + 24*60*60

        ft = (User.isactive == 1) & (User.signuped >= beginvalue) & (User.signuped < endvalue)

        q_web = User.select(User.signupeddate, db.fn.COUNT(User.id).alias('count')). \
            where((User.phoneactived == 0) & ft).group_by(User.signupeddate).dicts()
        q_phone = User.select(User.signupeddate, db.fn.COUNT(User.id).alias('count')). \
            where((User.phoneactived == 1) & ft).group_by(User.signupeddate).dicts()
        q_all = User.select(User.signupeddate, db.fn.COUNT(User.id).alias('count')). \
            where(ft).group_by(User.signupeddate).order_by(User.signuped).order_by(User.signuped).dicts()

        list = []
        for n in q_all:
            obj = {'date': n['signupeddate'], 'allcount': n['count'], 'webcount': 0, 'phonecount': 0}
            obj['webcount'] = self.find_count_by_date(n['signupeddate'], q_web)
            obj['phonecount'] = self.find_count_by_date(n['signupeddate'], q_phone)
            list.append(obj)
        self.write(simplejson.dumps(list))

    def find_count_by_date(self, date, list):
        for n in list:
            if n['signupeddate'] == date:
                return n['count']
        return 0


@route(r'/admin/report/product', name='admin_report_product')  # 产品报告
class ReportProductHandler(AdminBaseHandler):
    def get(self):
        begindate = self.get_argument('begindate', '')
        enddate = self.get_argument('enddate', '')
        self.render('admin/report/r_product.html', active='r_product', begindate=begindate, enddate=enddate)


@route(r'/admin/report/productchart', name='admin_report_product_chart')  # 产品销量曲线图
class ReportProductChartHandler(AdminBaseHandler):
    def get(self):
        begindate = self.get_argument('begindate', '')
        enddate = self.get_argument('enddate', '')
        if not begindate:
            beginvalue = time.mktime(time.strptime('2015-01-13', "%Y-%m-%d"))
        else:
            beginvalue = time.mktime(time.strptime(begindate, "%Y-%m-%d"))
        if not enddate:
            endvalue = time.time()
        else:
            endvalue = time.mktime(time.strptime(enddate, "%Y-%m-%d")) + 24*60*60

        ft = (Order.status < 5) & (((Order.status > -1) & (Order.payment == 0)) |
             ((Order.status > 0) & (Order.payment > 0))) & (Order.ordered >= beginvalue) &\
            (Order.ordered < endvalue) & (Order.payment < 9)

        q_v = Order.select(Order.ordereddate, db.fn.Sum(OrderItem.quantity*OrderItem.weight/500).alias('count')). \
            join(OrderItem).join(Product, on=(Product.id == OrderItem.product)).\
            where(ft & (Product.sku % '02%')).group_by(Order.ordereddate).\
            order_by(Order.ordereddate).dicts()

        q_f = Order.select(Order.ordereddate, db.fn.Sum(OrderItem.quantity*OrderItem.weight/500).alias('count')). \
            join(OrderItem).join(Product, on=(Product.id == OrderItem.product)).\
            where(ft & (Product.sku % '01%')).group_by(Order.ordereddate).\
            order_by(Order.ordereddate).dicts()

        q_all = Order.select(Order.ordereddate, db.fn.Sum((OrderItem.quantity*OrderItem.weight/500)).alias('count')). \
            join(OrderItem).where(ft).group_by(Order.ordereddate).\
            order_by(Order.ordereddate).dicts()
        result = {'chart_date':[], 'chart_sale_v':[], 'chart_sale_f':[]}
        for n in q_all:
            obj = {'date': n['ordereddate'], 'allcount': round(n['count'], 2), 'vcount': 0, 'fcount': 0}
            obj['vcount'] = self.find_count_by_date(n['ordereddate'], q_v)
            obj['fcount'] = self.find_count_by_date(n['ordereddate'], q_f)
            result['chart_date'].append(obj)

        q_sale_v = Order.select(Product.id, Product.name, db.fn.Sum(OrderItem.quantity*OrderItem.weight/500).alias('count')). \
            join(OrderItem).join(Product, on=(Product.id == OrderItem.product)).\
            where(ft & (Product.sku % '02%')).group_by(Product.id, Product.name).\
            order_by(db.fn.Sum(OrderItem.quantity*OrderItem.weight).desc()).dicts()

        q_sale_f = Order.select(Product.id, Product.name, db.fn.Sum(OrderItem.quantity*OrderItem.weight/500).alias('count')). \
            join(OrderItem).join(Product, on=(Product.id == OrderItem.product)).\
            where(ft & (Product.sku % '01%')).group_by(Product.id, Product.name).\
            order_by(db.fn.Sum(OrderItem.quantity*OrderItem.weight).desc()).dicts()
        for n in q_sale_v:
            result['chart_sale_v'].append({'id': n['id'], 'name': n['name'], 'count': round(n['count'], 2)})
        for n in q_sale_f:
            result['chart_sale_f'].append({'id': n['id'], 'name': n['name'], 'count': round(n['count'], 2)})

        self.write(simplejson.dumps(result))

    def find_count_by_date(self, date, list):
        for n in list:
            if n['ordereddate'] == date:
                return round(n['count'], 2)
        return 0


@route(r'/admin/report/product/pop', name='admin_report_product_pop')  # 产品报表弹出页面
class ReportProductPopHandler(AdminBaseHandler):
    def get(self):
        begindate = self.get_argument('begindate', '')
        enddate = self.get_argument('enddate', '')
        type = int(self.get_argument('type', '1'))
        page = int(self.get_argument("page", 1))
        pagesize = self.settings['admin_pagesize']
        if not begindate:
            beginvalue = time.mktime(time.strptime('2015-01-13', "%Y-%m-%d"))
        else:
            beginvalue = time.mktime(time.strptime(begindate, "%Y-%m-%d"))
        if not enddate:
            endvalue = time.time()
        else:
            endvalue = time.mktime(time.strptime(enddate, "%Y-%m-%d")) + 24*60*60

        ft = (Order.status < 5) & (((Order.status > -1) & (Order.payment == 0)) |
             ((Order.status > 0) & (Order.payment > 0))) & (Order.ordered >= beginvalue) &\
            (Order.ordered < endvalue) & (Order.payment < 9)
        total = (Order.select(db.fn.Count(Order.id)).where(ft)).scalar()
        if type == 1:
            q = Order.select(Order.id, Order.ordernum, Order.currentprice.alias('value')).where(ft).\
                order_by(Order.currentprice.desc()).paginate(page, pagesize).dicts()
        else:
            q = Order.select(Order.id, Order.ordernum, Order.weight.alias('value')).where(ft).\
                order_by(Order.weight.desc()).paginate(page, pagesize).dicts()

        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize

        list = []

        for row in q:
            list.append({'id': row['id'], 'ordernum':row['ordernum'], 'value': round(row['value'],2)})

        self.render('/admin/report/r_order_pop.html', list=list, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage,type=type,begindate=begindate,enddate=enddate)


@route(r'/admin/report/order', name='admin_report_order')  # 订单报告
class ReportOrderHandler(AdminBaseHandler):
    def get(self):
        report_o = {'price_order':[], 'weight_order':[]}
        begindate = self.get_argument('begindate', '')
        enddate = self.get_argument('enddate', '')
        if not begindate:
            beginvalue = time.mktime(time.strptime('2015-01-13', "%Y-%m-%d"))
        else:
            beginvalue = time.mktime(time.strptime(begindate, "%Y-%m-%d"))
        if not enddate:
            endvalue = time.time()
        else:
            endvalue = time.mktime(time.strptime(enddate, "%Y-%m-%d")) + 24*60*60

        ft = (Order.status < 5) & (((Order.status > -1) & (Order.payment == 0)) |
             ((Order.status > 0) & (Order.payment > 0))) & (Order.ordered >= beginvalue) &\
            (Order.ordered < endvalue) & (Order.payment < 9)
        ftext = (Order.status > -1) & (Order.status < 5) & (Order.ordered >= beginvalue) &\
            (Order.ordered < endvalue) & (Order.payment == 9)
        ordercount = (Order.select(db.fn.Count(Order.id)).where(ft)).scalar()
        report_o['orderext'] = (Order.select(db.fn.Count(Order.id)).where(ftext)).scalar()
        report_o['ordertotal'] = ordercount
        if ordercount > 0:
            totalfee = (Order.select(db.fn.Sum(Order.currentprice)).where(ft)).scalar()
            report_o['orderprice'] = round(float(totalfee if totalfee else 0)/ordercount, 2)
            totalweight = (Order.select(db.fn.Sum(Order.weight)).where(ft)).scalar()
            report_o['orderweight'] = round(float(totalweight if totalweight else 0)/ordercount, 2)
        else:
            report_o['orderprice'] = 0
            report_o['orderweight'] = 0

        q = Order.select(Order.id, Order.ordernum, Order.currentprice).where(ft).order_by(Order.currentprice.desc()).limit(5).dicts()
        for n in q:
            report_o['price_order'].append({'id':n['id'], 'ordernum': n['ordernum'], 'price':round(n['currentprice'], 2)})
        q = Order.select(Order.id, Order.ordernum, Order.weight).where(ft).order_by(Order.weight.desc()).limit(5).dicts()
        for n in q:
            report_o['weight_order'].append({'id':n['id'], 'ordernum': n['ordernum'], 'weight':round(n['weight'], 2)})
        self.render('admin/report/r_order.html', begindate=begindate, enddate=enddate, report_o=report_o, active='r_order')


@route(r'/admin/report/orderchart', name='admin_report_order_chart')  # 订单量每日曲线图
class ReportOrderChartHandler(AdminBaseHandler):
    def get(self):
        begindate = self.get_argument('begindate', '')
        enddate = self.get_argument('enddate', '')
        if not begindate:
            beginvalue = time.mktime(time.strptime('2015-01-13', "%Y-%m-%d"))
        else:
            beginvalue = time.mktime(time.strptime(begindate, "%Y-%m-%d"))
        if not enddate:
            endvalue = time.time()
        else:
            endvalue = time.mktime(time.strptime(enddate, "%Y-%m-%d")) + 24*60*60

        ft = (Order.status < 5) & (((Order.status > -1) & (Order.payment == 0)) |
             ((Order.status > 0) & (Order.payment > 0))) & (Order.ordered >= beginvalue) &\
            (Order.ordered < endvalue) & (Order.payment < 9)

        q_web = Order.select(Order.ordereddate, db.fn.COUNT(Order.id).alias('count')). \
            where((Order.order_from == 1) & ft).group_by(Order.ordereddate).dicts()

        q_phone = Order.select(Order.ordereddate, db.fn.COUNT(Order.id).alias('count')). \
            where((Order.order_from == 2) & ft).group_by(Order.ordereddate).dicts()

        q_sys = Order.select(Order.ordereddate, db.fn.COUNT(Order.id).alias('count')). \
            where((Order.order_from == 3) & ft).group_by(Order.ordereddate).dicts()

        q_all = Order.select(Order.ordereddate, db.fn.COUNT(Order.id).alias('count')). \
            where(ft).group_by(Order.ordereddate).order_by(Order.ordered).dicts()

        q_day = Order.select(db.fn.Left(Order.orderedtime,2).alias('hour'), db.fn.COUNT(Order.id).alias('count')). \
            where(ft).group_by(db.fn.Left(Order.orderedtime,2)).order_by(db.fn.Left(Order.orderedtime,2)).dicts()

        q_payment = Order.select(Order.payment, db.fn.COUNT(Order.id).alias('count')). \
            where(ft).group_by(Order.payment).dicts()

        q_from = Order.select(Order.order_from, db.fn.COUNT(Order.id).alias('count')). \
            where(ft).group_by(Order.order_from).dicts()

        result = {'chart_all':[], 'chart_day':[], 'chart_payment':[], 'chart_from':[]}

        for n in q_all:
            obj = {'date': n['ordereddate'], 'allcount': n['count'], 'webcount': 0, 'phonecount': 0, 'syscount': 0}
            obj['webcount'] = self.find_count_by_date(n['ordereddate'], q_web)
            obj['phonecount'] = self.find_count_by_date(n['ordereddate'], q_phone)
            obj['syscount'] = self.find_count_by_date(n['ordereddate'], q_sys)
            result['chart_all'].append(obj)
        for n in q_day:
            obj = {'hour':n['hour'], 'count':n['count']}
            result['chart_day'].append(obj)
        for n in q_payment:
            payment = ''
            if n['payment'] == 0:
                payment = '货到付款'
            elif n['payment'] == 1:
                payment = '支付宝'
            elif n['payment'] == 2:
                payment = '余额支付'
            elif n['payment'] == 3:
                payment = '网银支付'
            obj = {'payment': payment, 'count': n['count']}
            result['chart_payment'].append(obj)
        for n in q_from:
            f = ''
            if n['order_from'] == 1:
                f = '网站下单'
            elif n['order_from'] == 2:
                f = '手机下单'
            elif n['order_from'] == 3:
                f = '后台下单'
            obj = {'from': f, 'count': n['count']}
            result['chart_from'].append(obj)

        self.write(simplejson.dumps(result))

    def find_count_by_date(self, date, list):
        for n in list:
            if n['ordereddate'] == date:
                return n['count']
        return 0


@route(r'/admin/report/order/pop', name='admin_report_order_pop')  # 订单报表弹出页面
class ReportOrderPopHandler(AdminBaseHandler):
    def get(self):
        begindate = self.get_argument('begindate', '')
        enddate = self.get_argument('enddate', '')
        type = int(self.get_argument('type', '1'))
        page = int(self.get_argument("page", 1))
        pagesize = self.settings['admin_pagesize']
        if not begindate:
            beginvalue = time.mktime(time.strptime('2015-01-13', "%Y-%m-%d"))
        else:
            beginvalue = time.mktime(time.strptime(begindate, "%Y-%m-%d"))
        if not enddate:
            endvalue = time.time()
        else:
            endvalue = time.mktime(time.strptime(enddate, "%Y-%m-%d")) + 24*60*60

        ft = (Order.status < 5) & (((Order.status > -1) & (Order.payment == 0)) |
             ((Order.status > 0) & (Order.payment > 0))) & (Order.ordered >= beginvalue) &\
            (Order.ordered < endvalue) & (Order.payment < 9)
        total = (Order.select(db.fn.Count(Order.id)).where(ft)).scalar()
        if type == 1:
            q = Order.select(Order.id, Order.ordernum, Order.currentprice.alias('value')).where(ft).\
                order_by(Order.currentprice.desc()).paginate(page, pagesize).dicts()
        else:
            q = Order.select(Order.id, Order.ordernum, Order.weight.alias('value')).where(ft).\
                order_by(Order.weight.desc()).paginate(page, pagesize).dicts()

        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize

        list = []

        for row in q:
            list.append({'id': row['id'], 'ordernum':row['ordernum'], 'value': round(row['value'],2)})

        self.render('/admin/report/r_order_pop.html', list=list, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage,type=type,begindate=begindate,enddate=enddate)


@route(r'/admin/report/log', name='admin_report_log')  # 操作日志
class ReportLogHandler(AdminBaseHandler):
    def get(self):
        self.render('admin/report/r_log.html', active='r_log')


@route(r'/admin/report/sale', name='admin_report_sale')  # 销售报告
class ReportSaleHandler(AdminBaseHandler):
    executor = ThreadPoolExecutor(2)
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        begindate = self.get_argument('begindate', '')
        enddate = self.get_argument('enddate', '')
        fmt = "%Y-%m-%d"
        if not enddate:
            enddate = time.strftime(fmt, time.localtime(time.time()))
        endvalue = time.mktime(time.strptime(enddate, fmt)) + 24*60*60

        if not begindate:
            begindate = time.strftime(fmt, time.localtime(endvalue - (24*30*60*60)))
        beginvalue = time.mktime(time.strptime(begindate, fmt))

        result = yield self.getresult(beginvalue, endvalue)
        json = simplejson.dumps(result)
        self.render('admin/report/r_sale.html', active='r_sale', json=json, chartdata=result, begindate=begindate,
                    enddate=enddate)

    def find_count_by_date(self, date, list):
        for n in list:
            if n['ordereddate'] == date:
                return round(n['fee'], 2)
        return 0

    @run_on_executor
    def getresult(self, beginvalue, endvalue):
        ft = (Order.status < 5) & (((Order.status > -1) & (Order.payment == 0)) |
             ((Order.status > 0) & (Order.payment > 0))) & (Order.ordered >= beginvalue) &\
            (Order.ordered < endvalue) & (Order.payment < 9)

        ft_ext = (Order.status < 5) & (((Order.status > -1) & (Order.payment == 0)) |
             ((Order.status > 0) & (Order.payment > 0))) & (Order.ordered >= beginvalue) &\
            (Order.ordered < endvalue)

        q_sales = Order.select(Order.ordereddate, db.fn.Sum(Order.currentprice).alias('saleprice')). \
            where(ft).group_by(Order.ordereddate).\
            order_by(Order.ordereddate).dicts()

        sql = '''
            SELECT b.ordereddate, sum(b.freight) as fee, sum(case when b.payment = 0 then (case when b.currentprice>100 then b.currentprice*0.01 else 1 end) else 0 end) as sxfee FROM tb_orders b
            where ((b.status>-1 and b.payment=0) or (b.payment>0 and b.status>0) )
            and b.ordered>=%s and b.ordered<%s and b.status<5
            group by b.ordereddate order by b.ordered desc
            '''
        q_wl = []
        q = db.handle.execute_sql(sql % (beginvalue, endvalue))
        for row in q.fetchall():
            q_wl.append({'ordereddate': row[0], 'fee':row[1]+row[2]})


        q_product_count = OrderItem.select(Order.ordereddate, OrderItem.product_standard.alias('psid'),
                           db.fn.Sum(OrderItem.quantity).alias('count'), OrderItem.weight, OrderItem.price). \
            join(Order).\
            where(ft_ext).group_by(Order.ordereddate, OrderItem.product_standard, OrderItem.weight, OrderItem.price).\
            order_by(Order.ordereddate).dicts()

        q_cb = {}
        for p in q_product_count:
            ps = ProductStandard.get(id=p['psid'])
            tp = time.mktime(time.strptime(p['ordereddate'], "%Y-%m-%d")) + 24*60*60
            unitprice = get_cg_price(ps, time.localtime(tp))

            if unitprice > 0:
                try:
                    subtotal = ((unitprice * p['weight'] / 500) * p['count'])
                except:
                    subtotal = 0
            else:
                subtotal =(p['price'] * p['count'])
            if q_cb.has_key(p['ordereddate']):
                q_cb[p['ordereddate']] += subtotal
            else:
                q_cb[p['ordereddate']] = subtotal

        result = {'chart_date': []}
        for n in q_sales:
            obj = {'date': n['ordereddate'], 'saleprice': round(n['saleprice'], 2)}
            obj['cgprice'] = round((q_cb[n['ordereddate']] if q_cb[n['ordereddate']] else 0), 2)
            obj['wlprice'] = self.find_count_by_date(n['ordereddate'], q_wl)
            obj['carprice'] = '0.00'
            obj['peopleprice'] = '0.00'
            obj['bcprice'] = 0
            obj['totalcb'] = round((obj['cgprice'] + obj['wlprice'] + obj['carprice'] +
                                    obj['peopleprice'] + obj['bcprice']), 2)
            obj['mlv'] = round(((obj['saleprice'] - obj['cgprice'])/obj['saleprice']) * 100, 2)
            result['chart_date'].append(obj)
        return result


@route(r'/admin/report/sale/pop', name='admin_report_sale_pop')  # 销售报表弹出页面
class ReportSalePopHandler(AdminBaseHandler):
    executor = ThreadPoolExecutor(2)
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        date = self.get_argument('date', None)
        type = self.get_argument('type', 'date')
        page = int(self.get_argument("page", 1))
        pagesize = self.settings['admin_pagesize']
        sort = self.get_argument('sort', 'totalprice')
        if not date:
            date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        beginvalue = time.mktime(time.strptime(date, "%Y-%m-%d"))
        endvalue = beginvalue + 24*60*60

        if type == 'date':
            result = yield self.get_sale_pop(type, beginvalue, endvalue, sort)
            result = sorted(result, key=lambda d: d[sort], reverse=True)
            suminfo = {}
            suminfo['count'] = sum(n['count'] for n in result)
            suminfo['weight'] = sum(n['totalweight'] for n in result)
            suminfo['sumprice'] = sum(n['totalprice'] for n in result)
            suminfo['sumcgprice'] = sum(n['totalcgprice'] for n in result)

            self.render('/admin/report/r_sale_pop_date.html', list=result, suminfo=suminfo, count=len(result), date=date, type=type)
        elif type == 'order':
            result = yield self.get_sale_pop(type, beginvalue, endvalue, sort)
            suminfo = {}
            suminfo['weight'] = sum(n['weight'] for n in result)
            suminfo['cgprice'] = sum(n['price'] for n in result)
            suminfo['saleprice'] = sum(n['currentprice'] for n in result)
            suminfo['wlprice'] = sum(n['freight'] for n in result)
            suminfo['sxprice'] = sum(n['sxprice'] for n in result)
            suminfo['couponprice'] = sum(n['couponprice'] for n in result)
            suminfo['count'] = str(len(result))

            self.render('/admin/report/r_sale_pop_order.html', list=result, suminfo=suminfo, type=type, date=date)
        elif type == 'car':
            list = ''   # CostCar.select().where(CostCar.datetext == date)
            self.render('/admin/report/r_sale_pop_car.html', list=list)
        elif type == 'people':
            list = ''  # CostPeople.select().where(CostPeople.datetext == date)
            self.render('/admin/report/r_sale_pop_people.html', list=list)

    @run_on_executor
    def get_sale_pop(self, type, beginvalue, endvalue, sort):
        ft = (Order.status < 5) & (((Order.status > -1) & (Order.payment == 0)) |
             ((Order.status > 0) & (Order.payment > 0))) & (Order.ordered >= beginvalue) &\
            (Order.ordered < endvalue) & (Order.payment < 9)
        result = []
        tp = time.strptime(time.strftime("%Y-%m-%d", time.localtime(endvalue)), "%Y-%m-%d")

        if type == 'date':
            q = Order.select(Product.id, Product.name, db.fn.SUM(OrderItem.quantity).alias('count'), ProductStandard.id.alias('psid'),
                            ProductStandard.weight, ProductStandard.name.alias('standard'), OrderItem.price). \
                join(OrderItem, on=(Order.id == OrderItem.order)). \
                join(ProductStandard, on=(ProductStandard.id == OrderItem.product_standard)). \
                join(Product, on=(Product.id == OrderItem.product)). \
                group_by(Product.id, Product.name, OrderItem.price, ProductStandard.id, ProductStandard.weight, ProductStandard.name). \
                where(ft).dicts()

            for n in q:
                obj = {'name': n['name'], 'count': n['count'], 'id': n['id'], 'weight': n['weight'],
                       'standard': n['standard'], 'saleprice': n['price']}
                obj['price'] = round(obj['saleprice'] * 500 / obj['weight'], 2)
                obj['totalprice'] = round(obj['saleprice'] * obj['count'], 2)
                obj['totalweight'] = round(obj['weight'] * obj['count'] / 500, 2)

                ps = ProductStandard.get(id=n['psid'])
                cgprice = get_cg_price(ps, tp)
                if not cgprice:
                    cgprice = obj['price']
                obj['cgprice'] = cgprice

                obj['totalcgprice'] = round(obj['totalweight'] * obj['cgprice'], 2)
                result.append(obj)
            result = sorted(result, key=lambda d: d[sort], reverse=True)

        elif type == 'order':
            q = Order.select().where(ft).order_by(Order.id)
            for n in q:
                obj = {'ordernum': n.ordernum, 'weight': n.weight, 'id': n.id, 'currentprice': n.currentprice,
                       'freight': n.freight, 'ordered': n.ordered, 'status': n.status, 'payment': n.payment}
                price = 0
                for item in n.items:
                    cgprice = get_cg_price(item.product_standard, tp)
                    if not cgprice:
                        cgprice = item.price
                    else:
                        cgprice = cgprice * item.weight / 500
                    price += cgprice * item.quantity
                obj['price'] = round(price, 2)
                obj['sxprice'] = 0
                obj['couponprice'] = 0
                if n.coupon:
                    obj['couponprice'] = n.coupon.coupontotal.price
                if n.payment == 0:  # 代收手续费
                    obj['sxprice'] = get_sx_fee(n.currentprice)
                result.append(obj)

            ft2 = (Order.status < 5) & (Order.status > -1) & (Order.payment == 9) \
              & (Order.ordered >= beginvalue) & (Order.ordered < endvalue)
            q2 = Order.select().where(ft2).order_by(Order.id)
            for n in q2:
                obj = {'ordernum': n.ordernum + u'(补)', 'weight': n.weight, 'id': n.id, 'currentprice': 0,
                       'freight': n.freight, 'ordered': n.ordered, 'status': n.status, 'payment': n.payment}
                price = 0
                for item in n.items:
                    cgprice = get_cg_price(item.product_standard, tp)
                    if not cgprice:
                        cgprice = item.price
                    else:
                        cgprice = cgprice * item.weight / 500
                    price += cgprice * item.quantity
                obj['price'] = round(price, 2)
                obj['sxprice'] = 0
                obj['couponprice'] = 0
                if n.coupon:
                    obj['couponprice'] = n.coupon.coupontotal.price
                result.append(obj)
        return result

@route(r'/admin/report/user/order', name='admin_report_user_order')  # 用户订单数统计
class ReportUserOrderHandler(AdminBaseHandler):
    def get(self):
        begindate = self.get_argument('begindate', '')
        enddate = self.get_argument('enddate', '')
        page = int(self.get_argument("page", 1))
        pagesize = self.settings['admin_pagesize']
        order_sign = self.get_argument("order_sign", "")
        datetime = int(time.time())

        order_str = db.fn.COUNT(Order.user).desc()
        if order_sign == '0':
            order_str = db.fn.COUNT(Order.user).desc()
        elif order_sign == '1':
            order_str = db.fn.COUNT(Order.user).asc()
        elif order_sign == '2':
            order_str = db.fn.SUM(Order.currentprice).desc()
        elif order_sign == '3':
            order_str = db.fn.SUM(Order.currentprice).asc()
        elif order_sign == '4':
            order_str = User.signuped.desc()
        elif order_sign == '5':
            order_str = User.signuped.asc()
        elif order_sign == '6':
            order_str = (datetime - db.fn.Max(Order.ordered)).desc()
        elif order_sign == '7':
            order_str = (datetime - db.fn.Max(Order.ordered)).asc()
        elif order_sign == '8':
            order_str = (datetime - db.fn.Max(Order.ordered)).desc()
        elif order_sign == '9':
            order_str = (datetime - db.fn.Max(Order.ordered)).asc()
        if not begindate:
            begindate = '2015-01-13'
            beginvalue = time.mktime(time.strptime('2015-01-13', "%Y-%m-%d"))
        else:
            beginvalue = time.mktime(time.strptime(begindate, "%Y-%m-%d"))

        ft = (User.signuped > beginvalue)
        uq = User.select(User,db.fn.COUNT(Order.user).alias('order_count'),db.fn.Max(Order.ordered).alias('max_ordered'),
                                    db.fn.SUM(Order.currentprice).alias('order_price')).\
                                    join(Order, db.JOIN_LEFT_OUTER,
                                    on=((User.id==Order.user) &
                                    (((Order.status>-1) & (Order.payment==0)) | ((Order.payment>0) &
                                    (Order.status>0))) & (Order.payment<9) &
                                    (Order.status<5))).where(ft).group_by(User.id)
        total = uq.count()
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        users =  uq.order_by(order_str).paginate(page, pagesize)

        self.render('/admin/report/r_user_order.html', list=users, total=total, page=page, pagesize=pagesize,
                    totalpage=totalpage, begindate=begindate, enddate=enddate,datetime=datetime,order_sign=order_sign, active='r_user_order')

@route(r'/admin/report/invoice_total', name='admin_report_invoice_total')  # 采购及销售情况汇总
class ReportTotalInvoiceHandler(AdminBaseHandler):
    def get(self):
        begindate = self.get_argument('begindate', '')
        enddate = self.get_argument('enddate', '')

        if begindate and enddate:
            beginvalue = time.mktime(time.strptime(begindate, "%Y-%m-%d"))
            endvalue = time.mktime(time.strptime((enddate + " 23:59:59"), "%Y-%m-%d %H:%M:%S"))
        else:
            beginvalue = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', time.localtime(time.time())), "%Y-%m-%d %H:%M:%S"))
            endvalue = time.mktime(time.strptime(time.strftime('%Y-%m-%d 23:59:59', time.localtime(time.time())), "%Y-%m-%d %H:%M:%S"))
        sql1 = '''select sum(t1.quantity) as quantity,
sum((SELECT round(sum(t2.price),2) FROM tb_invoicing t2 where t2.addtime >= %s and t2.addtime < %s and t2.product_id = t1.id)) as in_price,
sum((SELECT round(sum(t2.quantity),2) FROM tb_invoicing t2 where t2.addtime >= %s and t2.addtime < %s and t2.product_id = t1.id)) as in_quantity,
sum((SELECT round(sum(t4.price * t4.quantity),2) FROM tb_orders t3 join tb_order_items t4 on t4.order_id=t3.id where t3.ordered >= %s and t3.ordered < %s and t4.product_id=t1.id)) as s_price,
sum((SELECT round(sum(t4.quantity * t4.weight/500),2) FROM tb_orders t3 join tb_order_items t4 on t4.order_id=t3.id where t3.ordered >= %s and t3.ordered < %s and t4.product_id=t1.id)) as s_quantity
from tb_product t1 where status>0 and is_store=0 %s '''
        skus1 = " and sku like '01%%'"
        q1 = db.handle.execute_sql(sql1 % (beginvalue, endvalue, beginvalue, endvalue, beginvalue, endvalue, beginvalue,
                                         endvalue, skus1))
        sql2 = '''select sum(t1.quantity) as quantity,
sum((SELECT round(sum(t2.price),2) FROM tb_invoicing t2 where t2.addtime >= %s and t2.addtime < %s and t2.product_id = t1.id)) as in_price,
sum((SELECT round(sum(t2.quantity),2) FROM tb_invoicing t2 where t2.addtime >= %s and t2.addtime < %s and t2.product_id = t1.id)) as in_quantity,
sum((SELECT round(sum(t4.price * t4.quantity),2) FROM tb_orders t3 join tb_order_items t4 on t4.order_id=t3.id where t3.ordered >= %s and t3.ordered < %s and t4.product_id=t1.id)) as s_price,
sum((SELECT round(sum(t4.quantity * t4.weight/500),2) FROM tb_orders t3 join tb_order_items t4 on t4.order_id=t3.id where t3.ordered >= %s and t3.ordered < %s and t4.product_id=t1.id)) as s_quantity
from tb_product t1 where status>0 and is_store=0 %s '''
        skus2 = " and sku like '02%%'"
        q2 = db.handle.execute_sql(sql1 % (beginvalue, endvalue, beginvalue, endvalue, beginvalue, endvalue, beginvalue,
                                         endvalue, skus2))
        list = []
        for row in q1.fetchall():
            list.append({'name': u'水果', 'quantity':row[0], 'in_price':row[1],'in_quantity':row[2],
                         's_price':row[3],'s_quantity':row[4], 'sku': '01'})
        for row in q2.fetchall():
            list.append({'name': u'蔬菜', 'quantity':row[0], 'in_price':row[1],'in_quantity':row[2],
                         's_price':row[3],'s_quantity':row[4], 'sku': '02'})
        self.render('/admin/report/r_invoice_total.html', list=list, begindate=begindate, enddate=enddate, active='r_invoice')


@route(r'/admin/report/invoice', name='admin_report_invoice')  # 采购及销售情况明细
class ReportInvoiceHandler(AdminBaseHandler):
    def get(self):
        begindate = self.get_argument('begindate', '')
        enddate = self.get_argument('enddate', '')
        sku = self.get_argument('sku', '')
        page = int(self.get_argument("page", 1))
        pagesize = self.settings['admin_pagesize']

        category = ''
        if sku:
            key = sku + '%%'
            category = " and sku like '"+ key + "'"

        if begindate and enddate:
            beginvalue = time.mktime(time.strptime(begindate, "%Y-%m-%d"))
            endvalue = time.mktime(time.strptime((enddate + " 23:59:59"), "%Y-%m-%d %H:%M:%S"))
        else:
            beginvalue = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', time.localtime(time.time())), "%Y-%m-%d %H:%M:%S"))
            endvalue = time.mktime(time.strptime(time.strftime('%Y-%m-%d 23:59:59', time.localtime(time.time())), "%Y-%m-%d %H:%M:%S"))
        sql = '''select t1.id,t1.name,t1.quantity,t1.sku,t1.defaultstandard,
(SELECT round(sum(t2.price),2) FROM tb_invoicing t2 where t2.addtime >= %s and t2.addtime < %s and t2.product_id = t1.id) as in_price,
(SELECT round(sum(t2.quantity),2) FROM tb_invoicing t2 where t2.addtime >= %s and t2.addtime < %s and t2.product_id = t1.id) as in_quantity,
(SELECT round(sum(t4.price * t4.quantity),2) FROM tb_orders t3 join tb_order_items t4 on t4.order_id=t3.id where t3.ordered >= %s and t3.ordered < %s and t4.product_id=t1.id) as s_price,
(SELECT round(sum(t4.quantity * t4.weight/500),2) FROM tb_orders t3 join tb_order_items t4 on t4.order_id=t3.id where t3.ordered >= %s and t3.ordered < %s and t4.product_id=t1.id) as s_quantity
from tb_product t1 where status>0 and is_store=0 %s order by in_price desc,s_price desc limit %s,%s'''
        countsql = '''select count(1) from tb_product where status>0 and is_store=0 %s '''
        q = db.handle.execute_sql(countsql % category)
        total = q.fetchone()[0]
        if total % pagesize > 0:
            totalpage = total / pagesize + 1
        else:
            totalpage = total / pagesize
        q = db.handle.execute_sql(sql % (beginvalue, endvalue, beginvalue, endvalue, beginvalue, endvalue, beginvalue,
                                         endvalue, category, (page if page==0 else page-1)*pagesize, pagesize))
        list = []
        for row in q.fetchall():
            if row[5] and row[6]:
                in_uint = float(row[5]) / float(row[6])
            else:
                in_uint = 0
            if row[7] and row[8]:
                s_uint = float(row[7]) / float(row[8])
            else:
                s_uint = 0
            list.append({'id':row[0], 'pname':row[1], 'quantity':row[2], 'sku':row[3], 'psid':row[4],'in_price':row[5],'in_quantity':row[6],
                         's_price':row[7],'s_quantity':row[8], 'in_unit':round(in_uint,2), 's_unit':round(s_uint,2)})
        self.render('/admin/report/r_invoice.html', list=list, total=total, page=page, pagesize=pagesize,sku=sku,
                    totalpage=totalpage, begindate=begindate, enddate=enddate, active='r_invoice')