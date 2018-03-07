#!/usr/bin/env python
#coding=utf8

from tornado import httpclient, escape
from tornado.auth import OAuth2Mixin, _auth_return_future, AuthError
import urllib
from tornado import httpclient
from tornado import escape
from tornado.httputil import url_concat
from tornado.auth import OAuth2Mixin
from tornado import gen
import logging
import re

class WeiboMixin(OAuth2Mixin):
    
    _OAUTH_ACCESS_TOKEN_URL = 'https://api.weibo.com/oauth2/access_token'
    _OAUTH_AUTHORIZE_URL = 'https://api.weibo.com/oauth2/authorize?'
    
    @_auth_return_future
    def get_authenticated_user(self, redirect_uri, client_id, client_secret, code, callback, grant_type='authorization_code', extra_fields=None):
        http = self.get_auth_http_client()
        args = {
            'redirect_uri': redirect_uri,
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': grant_type,
            }
        
        fields = set(['id', 'screen_name', 'profile_image_url'])
        
        if extra_fields:
            fields.update(extra_fields)
        
        http.fetch(self._OAUTH_ACCESS_TOKEN_URL, method='POST', 
                   body=urllib.urlencode(args),
                   callback=self.async_callback(self._on_access_token, redirect_uri, client_id, client_secret, callback, fields))

    def _oauth_request_token_url(self, redirect_uri=None, client_id=None,
                                 client_secret=None, code=None,
                                 grant_type=None, extra_params=None):
        pass
    
    def _on_access_token(self, redirect_uri, client_id, client_secret,
                         future, fields, response):
        if response.error:
            future.set_exception(AuthError('Weibo auth error %s' % str(response)))
            return

        args = escape.json_decode(escape.native_str(response.body))
        session = {
            'access_token': args['access_token'],
            'expires': args['expires_in'],
            'uid': args['uid'],
            }

        self.weibo_request(
            path='/users/show.json',
            callback=self.async_callback(
                self._on_get_user_info, future, session, fields),
            access_token=session['access_token'],
            uid=session['uid']
            )

    def _on_get_user_info(self, future, session, fields, user):
        if user is None:
            future.set_result(None)
            return

        fieldmap = {}
        for field in fields:
            fieldmap[field] = user.get(field)
        
        fieldmap.update({'access_token': session['access_token'], 'session_expires': session['expires']})

        future.set_result(fieldmap)

    @_auth_return_future
    def weibo_request(self, path, callback, access_token=None, uid=None, post_args=None, **args):
        url = "https://api.weibo.com/2" + path
        all_args = {}
        if access_token:
            all_args['access_token'] = access_token
        if uid:
            all_args['uid'] = uid
        if args:
            all_args.update(args)

        if all_args:
            url += '?' + urllib.urlencode(all_args)
        callback = self.async_callback(self._on_weibo_request, callback)
        http = self.get_auth_http_client()
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib.urlencode(post_args),
                       callback=callback)
        else:
            http.fetch(url, callback=callback)

    def _on_weibo_request(self, future, response):
        if response.error:
            future.set_exception(AuthError('Error response %s fetching %s',
                                           response.error, response.request.url))

            return

        future.set_result(escape.json_decode(response.body))
    
    def get_auth_http_client(self):
        return httpclient.AsyncHTTPClient()

class AlipayMixin(OAuth2Mixin):
    
    _OAUTH_ACCESS_TOKEN_URL = 'http://openapi.alipay.com/gateway.do'
    _OAUTH_AUTHORIZE_URL = 'https://openauth.alipay.com/oauth2/authorize.htm?'


class QQAuth2Minix(OAuth2Mixin):
    """docstring for QQAuth2Minix"""
    _OAUTH_OPEND_API = "https://graph.qq.com"
    _OAUTH_AUTHORIZE_URL = "https://graph.qq.com/oauth2.0/authorize"
    _OAUTH_ACCESS_TOKEN_URL = "https://graph.qq.com/oauth2.0/token"
    _OAUTH_OPEND_ID_URL = "https://graph.qq.com/oauth2.0/me"
    _OAUTH_NO_CALLBACKS = False

    def authorize_redirect(self, redirect_uri=None, client_id=None,
                           client_secret=None, extra_params=None ):
        """调用父类方法跳转认证获取code, QQ认证需要加入
           参数response_type:(code)和state所以作为附加参数传递给父类方法"""
        args = {
            "response_type" : "code",
            "state": "authorize",
        }
        logging.warn("redirect: " + str(args))
        if extra_params:
            args.update(extra_params)
        super(QQAuth2Minix, self).authorize_redirect(redirect_uri, client_id,
                                                     client_secret, args)
    @gen.engine
    def get_authenticated_user(self, redirect_uri, client_id, client_secret,
                              code, callback, extra_fields=None):
        """获取用户的token和openId, 并传入回调函数"""
        http = self.get_auth_http_client()
        args = {
            "redirect_uri": redirect_uri,
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "extra_params": {
                "grant_type": "authorization_code"
            }
        }
        response = yield gen.Task(http.fetch, self._oauth_request_token_url(**args))
        self._on_access_token(redirect_uri, client_id,
                              client_secret, callback, response)
    @gen.engine
    def _on_access_token(self, redirect_uri, client_id, client_secret,
                        callback, response):
        if response.error:
            logging.warning('QQ auth error: %s' % str(response))
            callback(None)
            return
        args = escape.parse_qs_bytes(escape.native_str(response.body))
        session = {
            "access_token": args["access_token"][-1],
            "expires": args.get("expires_in")[0]
        }
        http = self.get_auth_http_client()
        response = yield gen.Task(http.fetch, url_concat(self._OAUTH_OPEND_ID_URL, {"access_token":session["access_token"]}))
        self._on_open_id(redirect_uri, client_id,
                         client_secret, callback, session, response)

    def _on_open_id(self, redirect_uri, client_id, client_secret,
                        callback, session, response):
        if response.error:
            logging.warning('QQ get openId error: %s' % str(response))
            callback(None)
            return
        res_json = re.match(r".*?\((.*?)\)", escape.native_str(response.body)).group(1)
        args = escape.json_decode(res_json)
        session.update(args)
        callback(session)

    @gen.engine
    def qq_request(self, path, method, open_id, token, client_id, callback, **args):
        """调用QQ API接口, path需要传绝对路径"""
        params = {
            "access_token" : token,
            "oauth_consumer_key" : client_id,
            "openid" : open_id
        }
        params.update(args)
        url = self._OAUTH_OPEND_API + path
        http = self.get_auth_http_client()
        if "POST" == method:
            response = yield gen.Task(http.fetch , url, method = method, body=urllib.urlencode(params))
            self._on_qq_request(callback, response)
        else:
            url = url_concat(url, params)
            response = yield gen.Task(http.fetch, url)
            self._on_qq_request(callback, response)

    def _on_qq_request(self, callback, response):
        if response.error:
            logging.warning("Error response %s fetching %s", response.error,
                            response.request.url)
            callback(None)
            return
        callback(escape.native_str(response.body))
    def get_auth_http_client(self):
        """Returns the AsyncHTTPClient instance to be used for auth requests.

        May be overridden by subclasses to use an http client other than
        the default.
        """
        return httpclient.AsyncHTTPClient()