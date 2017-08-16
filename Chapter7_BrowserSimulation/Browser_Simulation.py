#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request
import http.cookiejar
import gzip
import io

host    = 'www.baidu.com'
url  = 'http://www.baidu.com'

Headers = {
        'Host':             host,
        'Connection':       'keep-alive',
        'Cache-Control':    'max-age=0',
        'User-Agent':       'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
        'Accept':           'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer':          url,
        'Accept-Encoding':  'gzip, deflate',
        'Accept-Language':  'zh-CN,zh;q=0.8,en;q=0.6',
        'Upgrade-Insecure-Requests':  '1',
        }

cjar = None

def BuildAndInstall_Opener():

    global cjar

    cjar    = http.cookiejar.CookieJar()
    cprocs  = urllib.request.HTTPCookieProcessor(cjar)
    httphandler  = urllib.request.HTTPHandler(debuglevel = 1)
    httpshandler = urllib.request.HTTPSHandler(debuglevel = 1)
    
    opener  = urllib.request.build_opener(httpshandler, httphandler,cprocs)
    urllib.request.install_opener(opener)

def Decode_GzipString(data):
    buf = io.BytesIO(data)
    gf  = gzip.GzipFile(fileobj = buf)
    data= gf.read()
    return data

def Visit_Website(url):

    req = urllib.request.Request(url, None, Headers)
    content = urllib.request.urlopen(req)

    '''get the content'''
    data = content.read()
    response = content.info()
    print(response)

    '''data process'''
    encoding = content.getheader('Content-Encoding')
    if ( encoding == 'gzip' ):
        data = Decode_GzipString(data)
        print('[DBG INFO] Content Encoding in GZIP')

    '''print the result'''
    print('='*100,'\r\n', data.decode('utf-8'))

if __name__ == '__main__':
    BuildAndInstall_Opener()
    Visit_Website(url)
