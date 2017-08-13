#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request
import http.cookiejar
import random
import re
import os
import socket

# for collecting proxy address
Url_ProxyAddr   = 'http://www.xicidaili.com/nn'
RegExp_ProxyAddr= '<tr class=.*?<td>(.*?)</td>\s+<td>(.*?)</td>.*?(HTTPS?)</td>' # because of re.S, HTTPS should be filtered.

# for Article
UrlTemp     = 'http://weixin.sogou.com/weixin?query=%s&type=2&page=%d'
KeyWd_Page  = 1
KeyWd_Query = 'Crawler'

RegExp_UrlTitle   = '(?<=<a target="_blank" href=")(https?://[^\s\(\)<>"]*).*?>(.*?)</a>'

# request header 
Headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
        }

# cookie
Cookie      = None
CookieFile  = 'cookie.txt'

# global Varibles
setProxyAddr = []

def Get_ProxyAddr():
    
    global setProxyAddr

    try:
        req     = urllib.request.Request(Url_ProxyAddr, None, Headers)
    except:
        print('[DBG ERR ] Get proxy address error.')
        return setProxyAddr

    data    = urllib.request.urlopen(req).read().decode('utf-8')
    AllProxyAd = re.compile(RegExp_ProxyAddr, re.S).findall(data)
    for proxy in AllProxyAd:
        if proxy[2] == 'HTTP':
            setProxyAddr.append(proxy[0]+':'+proxy[1])
    return setProxyAddr

def Build_CookieAndProxy(ProxyAddr=None):
    '''build the cookie processor and install it for global use'''
    global Cookie, CookieFile
    CookieProcessor = None
    ProxyHandler    = None

    #for Cookie
    if (CookieFile == None) or not(os.path.exists(CookieFile)):
        print("[DBG INFO] Make a New File to store the cookie")
        Cookie          = http.cookiejar.MozillaCookieJar(CookieFile)
    else:
        print("[DBG INFO] Load %s to save cookie"%CookieFile)
        Cookie          = http.cookiejar.MozillaCookieJar()
        Cookie.load(filename = CookieFile, ignore_discard = True, ignore_expires = True)
    CookieProcessor = urllib.request.HTTPCookieProcessor(Cookie)
    Cookie.save(CookieFile, ignore_discard = True, ignore_expires = True)       # save the cookie file  
    
    #TODO: for Proxy
    print("[DBG INFO] Proxy address: %s" % ProxyAddr)
    if ProxyAddr != None:
        ProxyHandler = urllib.request.ProxyHandler({'http':ProxyAddr})
    else:
        ProxyHandler = urllib.request.ProxyHandler({})
    
    #build and install the opener
    Opener  = urllib.request.build_opener(CookieProcessor,ProxyHandler) 
    urllib.request.install_opener(Opener)

def Change_Proxy():
    
    proxyaddr = random.choice(setProxyAddr)
    Build_CookieAndProxy(proxyaddr)
    pass 

def Generate_PageUrl():
    pass

def Find_UrlAndTitleOnPage(PageUrl):
    
    global Cookie, CookieFile
    
    try:
        req     = urllib.request.Request(PageUrl, None, Headers)
        content = urllib.request.urlopen(req, timeout = 30)         # set Timeout as 10s
    except urllib.error.URLError as UrlErr:
        print('[DBG ERR ] URLError ', end = '')
        if hasattr(UrlErr, 'code'):
            print('Error Code: ', UrlErr.code)
        if hasattr(UrlErr, 'reason'):
            print('Error Reason: ', UrlErr.reason)
        return
    except socket.error as SocketErr:
        print('[DBG ERR ] Sokect Error: ', SocketErr)
        return
    except requests.exceptions.RequestException as ReqErr:
        print('[DBG ERR ] RequestException')
        return
    else:
        print('[DBG INFO] Get Title Url Here')
        data    = content.read().decode('utf-8')
        Cookie.save(CookieFile, ignore_discard = True, ignore_expires = True)       # save the cookie file  
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

    global Cookie, CookieFile

    req = urllib.request.Request(Url, None, Headers)
    data = urllib.request.urlopen(req).read().decode('utf-8')
    Cookie.save(CookieFile, ignore_discard = True, ignore_expires = True)       # save the cookie file  
    
    with open(Title+'.html', 'w') as hFile:  # TODO: title name may cause some fault 
        hFile.write(data)

def Save_Photo(TitleUrl):
    pass

def Main_Func():

    Url = UrlTemp % (KeyWd_Query, KeyWd_Page)
    setText = Find_UrlAndTitleOnPage(Url)      # Get the set of Text
    while setText is None:
        Change_Proxy()
        setText = Find_UrlAndTitleOnPage(Url)      
        
    for i in setText:
        i = Fix_UrlAndTitle(i[0], i[1])
        Save_Article(i[0], i[1])

if __name__ == '__main__':
    Get_ProxyAddr()
    Change_Proxy()
#    Build_CookieAndProxy()
    Main_Func()

