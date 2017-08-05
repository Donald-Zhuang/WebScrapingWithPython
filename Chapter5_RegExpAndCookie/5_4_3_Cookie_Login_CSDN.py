#!/usr/local/bin/python3
#-*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import http.cookiejar
import re

'''data for login'''
LoginUrl    = "https://passport.csdn.net/account/login?ref=toolbar"
VisitUrl    = "http://my.csdn.net/?ref=toolbar"
LoginData   ={
    "username" : "",
    "password" : ""
}

Headers = {
        'Connection'    :'keep-alive',
        'Cache-Control' :'max-age=0',
        'User-Agent'    :'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept'        :'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#       'Accept-Encoding'   :'gzip, deflate, br',
        'Accept-Language'   :'zh-CN,zh;q=0.8,en;q=0.6',
        'Upgrade-Insecure-Request':'1',
        } 

'''please test the following regular expression before actual use'''
RegExp_Template         = "(?<=name=\"%s\" value=\")%s(?=(\">)?)"      # tempalate for Regular Expression 
Lt_RegExp        = RegExp_Template % ( "lt",         "LT-\d{6}-\w+" )
Execution_RegExp = RegExp_Template % ( "execution",  "\w+" )
EventId_RegExp   = RegExp_Template % ( "_eventId",   "\w+" ) 

    
def Login_Func(LoginData):
   
    '''for cookie function'''
    CookieFile  = "cookie.txt"
    CookieJar   = http.cookiejar.MozillaCookieJar(CookieFile)
    CookieProcessor = urllib.request.HTTPCookieProcessor(CookieJar)
    Opener  = urllib.request.build_opener(CookieProcessor, urllib.request.HTTPHandler)
    urllib.request.install_opener(Opener)

    '''pretreatment for login'''
    req = urllib.request.Request(LoginUrl, None, Headers)
    String = urllib.request.urlopen(req).read().decode('utf-8')
    CookieJar.save(ignore_discard=True, ignore_expires=True)
    
    '''To get the data we need to post to Login Server'''
    LoginData['lt'] = re.search(Lt_RegExp, String).group()
    print("[DEBUG] Get LT:  %s "%Lt_RegExp, LoginData.get('lt'))
    LoginData['execution']  = re.search(Execution_RegExp, String).group()
    print("[DEBUG] Get execution: %s "%Execution_RegExp, LoginData.get('execution'))
    LoginData['_eventId']   = re.search(EventId_RegExp, String).group()
    print("[DEBUG] Get eventId: %s "%EventId_RegExp, LoginData.get('_eventId'))
    
    '''log in'''
    PostData = urllib.parse.urlencode(LoginData).encode('utf-8')
    req = urllib.request.Request(LoginUrl, PostData, Headers)
    UrlData = urllib.request.urlopen(req)
    CookieJar.save(ignore_discard=True, ignore_expires=True)

    data = UrlData.read()
    print('\n' + '='*10 + 'login response headers' + '='*10 + '\n', UrlData.info(), '\n'+'='*42 ) 
    with open('LoginPage.html','wb') as hfile:
        hfile.write(data)
    
    '''Check whether log in sucessfully'''
    req = urllib.request.Request(VisitUrl,None,Headers)
    UrlData = urllib.request.urlopen(req)
    data = UrlData.read()
    print('\n' + '='*10 + 'Visit response headers'+'='*10 + '\n', UrlData.info(), '\n'+'='*42 ) 
    with open('VisitPage.html','wb') as hfile:
        hfile.write(data)

if __name__ == '__main__':
    Login_Func(LoginData)

