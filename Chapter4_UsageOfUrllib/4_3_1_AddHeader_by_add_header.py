#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request
import gzip
import io 

'''[TEST]'''
url = 'https://btso.pw/'
req = urllib.request.Request(url)
req.add_header('Host', 'btso.pw')
req.add_header('Connection','keep-alive')
req.add_header('Cache-Control','max-age=0')
req.add_header('Upgrade-Insecure-Request','1')
req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
req.add_header('Accept-Encoding', 'gzip, deflate, sdch, br')
req.add_header('Accept-Language','zh-CN,zh;q=0.8,en;q=0.6')

data = urllib.request.urlopen(req)
encoding = data.getheader('Content-Encoding')
content = data.read()
if encoding == 'gzip':
    buf = io.BytesIO(content)
    gf = gzip.GzipFile(fileobj=buf)
    content = gf.read()

with open('test.html',"wb") as fb:
    fb.write(content)
    
#print(content)

