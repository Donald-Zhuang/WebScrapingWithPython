#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request
import urllib.parse

url = 'http://www.iqianyue.com/mypost/'
FormData = {
        "name" : "nihao",
        "pass" : "hello",
}

Headers ={
        'Host': 'www.iqianyue.com',
        'Connection'        : 'keep-alive',
        'Content-Length'    : '21',
        'Cache-Control'     : 'max-age=0',
        'Origin'            : 'http://www.iqianyue.com',
        'Upgrade-Insecure-Requests' : '1',
        'User-Agent'        : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Content-Type'      : 'application/x-www-form-urlencoded',
        'Accept'            : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer'           : 'http://www.iqianyue.com/mypost/',
        'Accept-Encoding'   : 'gzip, deflate',
        'Accept-Language'   : 'zh-CN,zh;q=0.8,en;q=0.6',
}

PostData= urllib.parse.urlencode(FormData).encode('utf-8')
req     = urllib.request.Request(url, PostData, Headers)
data    = urllib.request.urlopen(req).read()

with open("test.html", 'wb') as hfile:
    hfile.write(data)

print(data)


