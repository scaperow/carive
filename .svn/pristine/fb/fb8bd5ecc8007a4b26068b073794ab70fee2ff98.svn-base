#!/usr/bin/env python
# coding=utf8
import simplejson
from lib.route import route
from model import Store
from handler import BaseHandler
import urllib2
import setting
import math
import sys
reload(sys)
sys.setdefaultencoding('utf8')

EARTH_RADIUS = 6378.137;
def rad(d):
   return d * math.pi / 180.0;
def getDistance(lng1,lat1,lng2,lat2):
    radLat1 = rad(lat1);
    radLat2 = rad(lat2);
    a = radLat1 - radLat2;
    b = rad(lng1) - rad(lng2);
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2),2) +
    math.cos(radLat1)*math.cos(radLat2)*math.pow(math.sin(b/2),2)));
    s = s * EARTH_RADIUS;
    s = round(s * 10000) / 10000;
    return s;
def getPointByAddress(address):
    url="http://api.map.baidu.com/geocoder/v2/?address="+address+"&output=json&ak="+setting.BaiDuMapAK+"&callback=showLocation"
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    html = response.read()
    preLen=len("showLocation&&showLocation(")
    html=html[preLen:len(html)-1]
    result=simplejson.loads(html);
    return result["result"]["location"]
@route(r'/map/getDistanceAS', name='map_getdistance_as')  # 获取某个地址和经销商之间的距离
class MapGetDistanceASHandler(BaseHandler):
    def get(self):
        address = self.get_argument("address", '')
        storeid= self.get_argument("storeid", '0')
        result = getDistanceAS(address,storeid)
        self.write(simplejson.dumps(result))

@route(r'/map/getMinDistanceStore', name='map_getmindistancestore')  # 获取某个地址和经销商之间的距离
class MapGetDistanceASHandler(BaseHandler):
    def get(self):
        address = self.get_argument("address", '')
        result = getMinDistanceStore(address)
        self.write(simplejson.dumps(result))

def getDistanceAS(address, store_id):
    result = {"flag":0,"msg":"","data":""}
    try:
        if address:
            if store_id>0:
                store=Store.get(Store.id==store_id)
                result["flag"]=1
                point=getPointByAddress(address);
                result["data"]=str(getDistance(point["lng"],point["lat"],float(store.x),float(store.y)))
            else:
                result["flag"]=0
                result["msg"]="经销商ID不正确！"
        else:
            result["flag"]=0
            result["msg"]="地址不能为空！"

    except:
        result["flag"]=0
        result["msg"]="地址或者经销商信息错误！"

    return result

def getMinDistanceStore(address):
    result = {"flag":0,"msg":"","data":""}
    try:
        if address:

            if address.count('枫林绿洲')>0:
                address=address.replace('小区','')
            qstore = Store.select().where((Store.status == 1) & (Store.storetype == 0))
            point=getPointByAddress(address)
            minDistance=10000
            minStore=None
            for store in qstore:
                minD=getDistance(point["lng"],point["lat"],float(store.x),float(store.y))
                if minD<minDistance:
                    minDistance=minD
                    minStore=store
            if minDistance>0 and minStore and minDistance<minStore.psdistance:
                result["flag"]=1
                result["data"]={
                    "id":minStore.id,
                    "name":minStore.name,
                    "distance":minDistance,
                    "byprice":minStore.byprice,
                    "freight":minStore.freight,
                }
            else:
                result["flag"]=0
                result["msg"]="在该地址附近未找到可以配送的经销商！"
                result["data"]=""
        else:
            result["flag"]=0
            result["msg"]="地址不能为空！"

    except Exception, ex:
        result["flag"]=0
        result["msg"]="地址或者经销商信息错误！"

    return result

