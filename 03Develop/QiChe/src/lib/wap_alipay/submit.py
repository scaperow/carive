# -*- coding: utf-8 -*-
import time
import urllib2
import urllib
import xml.etree.ElementTree as etree
try:
    from urllib.parse import parse_qs as _parse_qs  # py3
except ImportError:
    from urlparse import parse_qs as _parse_qs  # Python 2.6+
from config import Settings
import core


def get_pay_url(tn, subject, total_fee, isCZ=False):
    """get token

    """
    _GATEWAY = "http://wappaygw.alipay.com/service/rest.htm"
    req_id = str(time.time())
    req_token_data = "<direct_trade_create_req><notify_url>%s</notify_url>" \
                     "<call_back_url>%s</call_back_url><seller_account_name>%s</seller_account_name>" \
                     "<out_trade_no>%s</out_trade_no><subject>%s</subject>" \
                     "<total_fee>%s</total_fee><merchant_url>%s</merchant_url>" \
                     "</direct_trade_create_req>" % \
               (Settings.CZ_NOTIFY_URL if isCZ else Settings.NOTIFY_URL,
                Settings.CZ_RETURN_URL if isCZ else Settings.RETURN_URL,
                Settings.SELLER_EMAIL,
                tn, subject, total_fee,'')
                #Settings.CZ_MERCHANT_URL if isCZ else Settings.MERCHANT_URL)

    temp_param = {"partner": Settings.PARTNER,
                  "_input_charset": Settings.INPUT_CHARSET,
                  "sec_id": Settings.SIGN_TYPE,
                  "service": "alipay.wap.trade.create.direct",
                  "format": "xml",
                  "v": "2.0",
                  "req_id": req_id,
                  "req_data": req_token_data.replace("\n", ""),
                  }
    token_params = core.build_request_params(temp_param)
    request_url = "%s?_input_charset=%s" % (_GATEWAY, Settings.INPUT_CHARSET)
    data = urllib.urlencode(token_params)

    response = urllib2.urlopen(request_url, data=data).read()
    response_params = parse_response(response, Settings.SIGN_TYPE)
    #获得token
    token = response_params["request_token"]
    #再组装数据，生成签名，请求获得支付链接
    req_data = "<auth_and_execute_req><request_token>%s</request_token></auth_and_execute_req>" % (token)
    fr_temp_params = temp_param
    fr_temp_params["service"] = "alipay.wap.auth.authAndExecute"
    fr_temp_params["req_data"] = req_data
    fr_params = core.build_request_params(fr_temp_params)
    alipay_query_str = urllib.urlencode(fr_params)
    alipay_url = "%s?%s" % (_GATEWAY, alipay_query_str)
    return alipay_url


def parse_response(query_params, sign_type="MD5"):
    """解析远程模拟提交后返回的信息

    <param name="strText">要解析的字符串</param>
    <returns>解析结果</returns>
    """
    params = _parse_qs(query_params, True)
    if params["res_data"]:
        if sign_type == "0001":
            # TO DO RSA 解密
            params["res_data"] = "<r>解密结果</r>"
        tree = etree.fromstring(params["res_data"][0])
        token = tree.find("request_token").text
        params.update({"request_token": token})
    return params