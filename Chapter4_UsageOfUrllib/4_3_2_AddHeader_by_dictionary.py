#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request
import gzip
import io 

url = 'https://btso.pw/'

Headers = {
        'Host':'btso.pw',
        'Connection':'keep-alive',
        'Cache-Control':'max-age=0',
        'Upgrade-Insecure-Request':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6'
}

req = urllib.request.Request(url, None, Headers)
openUrl =urllib.request.urlopen(req)

encoding = openUrl.getheader('Content-Encoding')
content  = openUrl.read()

if encoding == 'gzip':
    buf = io.BytesIO(content)
    gf  = gzip.GzipFile(fileobj=buf)
    content = gf.read()

print(content)
