#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
import tornado.httpclient

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument("name", "nil")
        self.write("Hello, %s" % name)

    def post(self):
        name = self.get_argument("name")
        self.write({"name": name})


class AsyncHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        resp = yield http_client.fetch("https://cn.bing.com/")
        self.write(str(len(resp.body)))

    @tornado.gen.coroutine
    def post(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        resp = yield http_client.fetch("https://cn.bing.com/")
        self.write(str(len(resp.body)))


def get_app():
    application = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/async", AsyncHandler),
        ]
    )
    return application


def main():
    tornado.options.parse_command_line()
    application = get_app()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
