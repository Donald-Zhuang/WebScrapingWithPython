#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request
import http.cookiejar
import re

UrlTemp     = 'http://www.baidu.com'

RegExp_UrlAll   = 'https?://[^\s"<>()]+'

def Build_Cookie(CookieFile=None):
    '''build the cookie processor and install it for global use'''
    cookie          = http.cookiejar.MozillaCookieJar(CookieFile)
    CookieProcessor = urllib.request.HTTPCookieProcessor(cookie)
    CookieOpener    = urllib.request.build_opener(CookieProcessor,  urllib.request.HTTPHandler)
    urllib.request.install_opener(CookieOpener)
       
def Find_UrlOnWeb(PageUrl):
    
    setPhotoUrl = {}
    data = urllib.request.urlopen(PageUrl).read().decode('utf-8')
    
    setUrl = re.compile(RegExp_UrlAll).findall(data)
    setUrl = list(set(setUrl))
    return setUrl

def Main_Func():
    setUrl = Find_UrlOnWeb(UrlTemp)      # Get the set of URLs
    for i in setUrl:
        print(i)

if __name__ == '__main__':
#   Build_Cookie()
    Main_Func()


