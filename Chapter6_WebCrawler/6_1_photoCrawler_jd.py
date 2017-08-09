#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request
import http.cookiejar
import re


UrlTemp     = 'https://list.jd.com/list.html?cat=9987,653,655'
UrlKeyWord  = '&page=%d'

RegExp_MainPage = '<ul class="gl-warp clearfix">(.*)<div class="page clearfix">'
RegExp_Photo    = '<img width="220" height="220" data-img="1" data-lazy-img="//(.+?\.jpg)?">'

def Build_Cookie(CookieFile=None):
    '''build the cookie processor and install it for global use'''
    cookie          = http.cookiejar.MozillaCookieJar(CookieFile)
    CookieProcessor = urllib.request.HTTPCookieProcessor(cookie)
    CookieOpener    = urllib.request.build_opener(CookieProcessor,  urllib.request.HTTPHandler)
    urllib.request.install_opener(CookieOpener)
       
def Find_UrlOfPhoto(PageUrl):
    
    setPhotoUrl = {}
    data = urllib.request.urlopen(PageUrl).read().decode('utf-8')
    
    MainPage = re.compile(RegExp_MainPage).findall(data)
    setPhotoUrl = re.compile(RegExp_Photo).findall(data)

    return setPhotoUrl

def DownloadAndSave_Photo(PhotoUrl, page, cnt):
    
    statusOfProcess = None
    ImageName   = 'jd/p%03d_c%03d_jd.jpg'%(page, cnt)
    ImageUrl    = 'https://'+PhotoUrl
    print(ImageUrl)
    try:
        urllib.request.urlretrieve(ImageUrl, filename=ImageName)
    except urllib.error.URLError as e:
        print('[DBG USR] Download image error.',)
        if hasattr(e, 'code'):
            print('code: ', e.code)
        if hasattr(e, 'reason'):
            print('reason: ', e.reason)
        statusOfProcess = False
    return statusOfProcess

def Main_Func():
    for i in range(1,151):
        PageUrl = UrlTemp+(UrlKeyWord % i)          # Get the URL of the page
        print('[DBG USR] Page Url: %s' % PageUrl)
        setPhotoUrl = Find_UrlOfPhoto(PageUrl)      # Get the set of photos' URL
        x = 0
        for url in setPhotoUrl:
            DownloadAndSave_Photo(url, i, x )
            x+=1

if __name__ == '__main__':
#   Build_Cookie()
    Main_Func()


