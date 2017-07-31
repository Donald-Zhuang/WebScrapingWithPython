#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request

UrlMain='http://www.baidu.com/s?wd='
UrlQueryStr="hello中国"

UrlFinal=UrlMain + urllib.request.quote(UrlQueryStr)
# UrlFinal=UrlMain + UrlQueryStr.encode("utf-8")  --> it couldn't work.
print(UrlFinal)

req = urllib.request.urlopen(UrlFinal)
StatusCode = req.getcode()
print("Status-Code: %d" % StatusCode)

data = req.read()
# print(data)
with open("test.html","wb") as fhandle:
    fhandle.write(data)

    
