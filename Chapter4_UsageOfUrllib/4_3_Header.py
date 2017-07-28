#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request

'''[TEST]'''
url='https://btso.pw/search/EYAN'
# Content = urllib.request.urlopen(url)
urllib.request.urlretrieve(url, 'test.html')
 

