# shell_online
Tornado 在线调试工具，一个基于IPython的Shell，用于调试Tornado，可以使用命令行进行调试，直接使用`get`和`post`方法调用接口。

**环境**

    Python 2.7

**依赖包**

    IPython: 5.8.0
    Tornado: 5.1.1


**Example:**

```bash
$ ./shell.py
In [1]: r = get("/", {"name": "Jack"})
Request URL: http://127.0.0.1:51891/?name=Jack

In [2]: r
Out[2]: 
{'body': 'Hello, Jack',
 'headers': {'Connection': 'close',
  'Content-Length': '11',
  'Content-Type': 'text/html; charset=UTF-8',
  'Date': 'Sat, 10 Aug 2019 13:44:40 GMT',
  'Etag': '"ec4a1529faa8c5ea0b9b9c23b838e605938cd498"',
  'Server': 'TornadoServer/5.1.1'},
 'request': <tornado.httpclient.HTTPRequest at 0x1025c2c10>}

In [3]: r = post("/", {"name": "Jack"})
Request URL: http://127.0.0.1:51891/

In [4]: r
Out[4]: 
{'body': '{"name": "Jack"}',
 'headers': {'Connection': 'close',
  'Content-Length': '16',
  'Content-Type': 'application/json; charset=UTF-8',
  'Date': 'Sat, 10 Aug 2019 13:44:58 GMT',
  'Server': 'TornadoServer/5.1.1'},
 'request': <tornado.httpclient.HTTPRequest at 0x1025d0250>}

In [5]: r.json
Out[5]: {u'name': u'Jack'}

In [6]: 
```