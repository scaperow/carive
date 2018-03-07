#!/usr/bin/env python
# coding=utf8

import time
import signal
import mymoudles
import logging
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.options import define, parse_command_line, options
import sys
from bootloader import settings, jinja_environment, memcachedb
from lib.filter import register_filters
from lib.route import Route
from lib.session import MemcacheSessionStore
from handler import PageNotFoundHandler,site2,cart,ajax2,user2,pay2,mobile,activity,map

define('cmd', default='runserver', metavar='runserver|syncdb')


class Application(tornado.web.Application):
    def __init__(self):
        self.jinja_env = jinja_environment
        self.jinja_env.filters.update(register_filters())
        self.jinja_env.tests.update({})
        self.jinja_env.globals['settings'] = settings

        self.memcachedb = memcachedb
        self.session_store = MemcacheSessionStore(memcachedb)

        handlers = [
                       tornado.web.url(r"/style2/(.+)", tornado.web.StaticFileHandler,
                                       dict(path=settings['static_path']), name='static_path'),
                       tornado.web.url(r"/upload/(.+)", tornado.web.StaticFileHandler,
                                       dict(path=settings['upload_path']), name='upload_path')
                   ] + Route.routes() +[(r".*", PageNotFoundHandler)]
        settings['ui_modules'] = mymoudles
        tornado.web.Application.__init__(self, handlers, **settings)


def syncdb():
    from model import initDB
    initDB()

def runserver():
    http_server = HTTPServer(Application(), xheaders=True)
    port = 8889
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    http_server.listen(port)
    loop = tornado.ioloop.IOLoop.instance()

    logging.info('Server running on http://127.0.0.1:%d' % port)
    loop.start()


if __name__ == '__main__':
    parse_command_line()

    if options.cmd == 'syncdb':
        syncdb()
    else:
        runserver()

