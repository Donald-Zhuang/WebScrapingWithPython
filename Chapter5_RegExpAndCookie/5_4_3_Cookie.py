#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request
import urllib.parse

LoginUrl    = "https://passport.csdn.net/account/login?ref=toolbar"
VisitUrl    = "http://blog.csdn.net"
LoginData   ={
    "username" : "",
    "password" : ""
}
Headers = {
        'Host':'passport.csdn.net',
        'Connection':'keep-alive',
        'Cache-Control':'max-age=0',
        'Upgrade-Insecure-Request':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6'
        }
def Login_Func( LoginData ):
    postData = urllib.parse.urlencode(LoginData).encode('utf-8')
    req = urllib.request.Request(LoginUrl, postData)
    UrlData = urllib.request.urlopen(req)
    
    data = UrlData.read()
    print( UrlData.info() ) # only for debug 

    with open("LoginPage.html",'wb') as hfile:
        hfile.write(data)

    data = urllib.request.urlopen(VisitUrl).read()
    with open("VisitPage.html",'wb') as hfile:
        hfile.write(data)

if __name__ == '__main__':
    Login_Func(LoginData)

