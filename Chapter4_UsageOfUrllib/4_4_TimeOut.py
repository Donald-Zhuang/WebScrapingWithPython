#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request

url = 'https://github.com/'
for i in range(1,100):
    try:
        data = urllib.request.urlopen(url,timeout = 1).read()
        #print(data)
    except Exception as e:
        print("UrlOpen error: %s" % e)


