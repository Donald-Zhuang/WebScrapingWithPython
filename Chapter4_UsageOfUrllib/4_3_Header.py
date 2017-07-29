#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request

'''[TEST]'''
url='https://btso.pw/search/EYAN'
# Content = urllib.request.urlopen(url).read()
# print(Content)
# urllib.request.urlretrieve(url, 'test.html')
req = urllib.request.Request(url)
req.add_header('Host', 'btso.pw')
req.add_header('Connection','keep-alive')
req.add_header('Cache-Control','max-age=0')
req.add_header('Upgrade-Insecure-Request','1')
req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
req.add_header('Referer','https://btso.pw/search/%E3%80%90%E8%A3%A8%E6%9A%A3%E5%A3%9E%E5%A3%9E%E3%80%91')
req.add_header('Accept-Encoding', 'gzip, deflate, sdch, br')
req.add_header('Accept-Language','zh-CN,zh;q=0.8,en;q=0.6')

data = urllib.request.urlopen(req).read().decode('utf-8')
#with open('test.html',"wb") as fb:
#    fb.write(data)
    
print(data)

