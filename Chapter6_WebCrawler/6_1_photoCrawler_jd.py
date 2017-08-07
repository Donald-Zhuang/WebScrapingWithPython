#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request
import http.cookiejar
import re
import logging


UrlTemp     = 'https://list.jd.com/list.html?cat=9987,653,655'
UrlKeyWord  = '&page=%d'

HttpHeaders ={

        }

def Build_Cookie(CookieFile=None):
    '''build the cookie processor and install it for global use'''
    cookie          = http.cookiejar.MozillaCookieJar(CookieFile)
    CookieProcessor = urllib.request.HTTPCookieProcessor(cookie)
    CookieOpener    = urllib.request.build_opener(CookieProcessor,  urllib.request.HTTPHandler)
    urllib.request.install_opener(CookieOpener)
       
def Find_UrlOfPhoto(PageUrl):
    setPhotoUrl = None
    return setPhotoUrl

def DownloadAndSave_Photo(PhotoUrl):
    statusOfProcess = None
    if statusOfProcess == False:
        logging.debug('Download or Save Failed! %s ' % PhotoUrl)
    return statusOfProcess

def Main_Func():
    for i in range(1,151):
        PageUrl = UrlTemp+(UrlKeyWord % i)          # Get the URL of the page
        setPhotoUrl = Find_UrlOfPhoto(PageUrl)      # Get the set of photos' URL
        for url in setPhotoUrl:
            DownloadAndSave_Photo(url)

if __name__ == '__main__':
    Build_Cookie()
    Main_Func()


