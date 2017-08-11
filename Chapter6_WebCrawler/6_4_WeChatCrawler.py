#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request
import http.cookiejar
import re

UrlTemp     = 'http://weixin.sogou.com/weixin?query=%s&type=%d&page=%d'
KeyWd_Type  = 2
KeyWd_Page  = 1
KeyWd_Query = 'Crawler'

RegExp_UrlTitle   = '(?<=<a target="_blank" href=")(https?://[^\s\(\)<>"]*).*?>(.*?)</a>'

Headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
        }

def Build_CookieAndProxy(CookieFile=None, ProxyAddr=None):
    '''build the cookie processor and install it for global use'''
    #for Cookie
    cookie          = http.cookiejar.MozillaCookieJar(CookieFile)
    CookieProcessor = urllib.request.HTTPCookieProcessor(cookie)
    
    #TODO: for Proxy
    pass

    Opener    = urllib.request.build_opener(CookieProcessor) 
    urllib.request.install_opener(Opener)

def Generate_PageUrl():
    pass

def Find_UrlAndTitleOnPage(PageUrl):
    
    setPhotoUrl = {}
    req     = urllib.request.Request(PageUrl, None, Headers)
    content = urllib.request.urlopen(req)
    data    = content.read().decode('utf-8')
    setUrl = re.compile(RegExp_UrlTitle,re.S).findall(data)
    # setUrl = list(set(setUrl))
    return setUrl

def Fix_UrlAndTitle(Url, Title):
    UrlTitle = []
    Url     = Url.replace( 'amp;', '' )
    Title   = Title.replace( '<em><!--red_beg-->',  '' ).replace( '<!--red_end--></em>', '' )
    UrlTitle.append(Url)
    UrlTitle.append(Title)
    return UrlTitle

def Save_Article(Url,Title):
    req = urllib.request.Request(Url, None, Headers)
    data = urllib.request.urlopen(req).read().decode('utf-8')
    with open(Title+'.html', 'w') as hFile:  # TODO: title name may cause some fault 
        hFile.write(data)

def Save_Photo(TitleUrl):
    pass

def Main_Func():
    Url = UrlTemp % (KeyWd_Query, KeyWd_Type, KeyWd_Page)
    setText = Find_UrlAndTitleOnPage(Url)      # Get the set of Text
    for i in setText:
        i = Fix_UrlAndTitle(i[0], i[1])
        Save_Article(i[0], i[1])

if __name__ == '__main__':
    Build_Cookie()
    Main_Func()


