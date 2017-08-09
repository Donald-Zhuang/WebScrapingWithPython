#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request
import re

url = 'https://list.jd.com/list.html?cat=9987,653,655&page=2'

html = urllib.request.urlopen(url).read().decode('utf-8')

pat = '<img width="220" height="220" data-img="1" data-lazy-img="//(.+?(\.jpg|\.png){1,})">' # '<img width="220" height="220" data-img="1" data-lazy-img="//(.+?\.jpg)?(\>)?' 
imagelist = re.compile(pat).findall(html)
imagelist = set(imagelist)
for urlphoto in imagelist:
    print(urlphoto)

