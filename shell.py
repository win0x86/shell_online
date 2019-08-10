#!/usr/bin/env python
# coding: utf-8
"""
IPython Shell
"""

import json
from urllib import urlencode
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient
from tornado.httpserver import HTTPServer
from tornado.testing import bind_unused_port
from tornado.process import Subprocess
from IPython import start_ipython

from web import get_app


class Response(dict):
    @property
    def json(self):
        return json.loads(self["body"])


class MockHTTPServer(object):
    def __init__(self):
        self._app = self.get_app()
        sock, port = bind_unused_port()
        self._port = port
        self.io_loop = self.get_new_ioloop()
        self.http_server = self.get_http_server()
        self.http_server.add_sockets([sock])
        self.timeout = 5
        self._remove_timeout = None

    @property
    def http_client(self):
        return self.get_http_client()

    def get_new_ioloop(self):
        return IOLoop()

    def get_http_client(self):
        return AsyncHTTPClient()

    def get_httpserver_options(self):
        return {}

    def get_http_server(self):
        return HTTPServer(self._app, **self.get_httpserver_options())

    def get_http_port(self):
        return self._port

    def get_app(self):
        return get_app()

    def get_url(self, path):
        return 'http://127.0.0.1:%s%s' % (self.get_http_port(), path)

    def fetch(self, path, raise_error=False, **kwargs):
        if path.lower().startswith("http://"):
            url = path
        else:
            url = self.get_url(path)

        print "Request URL: {}".format(url)
        return self.io_loop.run_sync(
            lambda: self.http_client.fetch(url, raise_error=raise_error, **kwargs),
            timeout=self.timeout)

    def run(self):
        self.clean()

    def clean(self):
        Subprocess.uninitialize()

    def urlencode(self, params):
        return urlencode(params)

    def return_resp(self, response):
        return Response(
            headers=dict(response.headers.items()),
            body=response.body,
            request=response.request
        )


mock_server = MockHTTPServer()


def get(path, params=None, **kwargs):
    """
    HTTP GET 请求:

    :param path str: 请求URL
    :param params dict: 参数字典
    :return dict: {headers: 响应头, body: 响应体, request: 请求对象}
    
    Example:

    >>> r = get("/info", {"name": "J"})  # GET /info?name=J
    >>> print r["body"]                  # 响应体
    >>> print r.json                     # 响应数据body转JSON
    """
    if params:
        path = "{}?{}".format(path, mock_server.urlencode(params))
    r = mock_server.fetch(path, **kwargs)
    mock_server.run()
    return mock_server.return_resp(r)


def post(path, params, **kwargs):
    """
    HTTP POST 请求:

    :param path str: 请求URL
    :param params dict: 参数字典
    :return dict: {headers: 响应头, body: 响应体, request: 请求对象}
    
    Example:

    >>> r = post("/info", {"name": "J"})
    >>> print r["body"]                   # 响应体
    >>> print r.json                      # 响应数据body转JSON
    """
    kwargs["method"] = "POST"
    if params:
        kwargs["body"] = mock_server.urlencode(params)
    
    r = mock_server.fetch(path, **kwargs)
    mock_server.run()
    return mock_server.return_resp(r)


def main():
    start_ipython(
        user_ns={
            "get": get,
            "post": post,
        }
    )


if __name__ == "__main__":
    main()