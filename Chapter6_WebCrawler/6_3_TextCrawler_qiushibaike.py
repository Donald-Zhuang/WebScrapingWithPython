#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request
import http.cookiejar
import re

UrlTemp     = 'https://www.qiushibaike.com'
RegExp_Text   = '<div class="content">.*?<span>(.*?)</span>'

Headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
        }

def Build_Cookie(CookieFile=None):
    '''build the cookie processor and install it for global use'''
    cookie          = http.cookiejar.MozillaCookieJar(CookieFile)
    CookieProcessor = urllib.request.HTTPCookieProcessor(cookie)
    CookieOpener    = urllib.request.build_opener(CookieProcessor,  urllib.request.HTTPHandler)
    urllib.request.install_opener(CookieOpener)
       
def Find_TextOnPage(PageUrl):
    
    setPhotoUrl = {}
    req     = urllib.request.Request(PageUrl, None, Headers)
    content = urllib.request.urlopen(req)
    data    = content.read().decode('utf-8')
    with open('qiushi.html','w') as hFile:
        hFile.write(data)
    setUrl = re.compile(RegExp_Text,re.S).findall(data)
    setUrl = list(set(setUrl))
    return setUrl

def Main_Func():
    setText = Find_TextOnPage(UrlTemp)      # Get the set of Text
    for i in setText:
        print(i)

if __name__ == '__main__':
#   Build_Cookie()
    Main_Func()


