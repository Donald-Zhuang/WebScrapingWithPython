#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request
import http.cookiejar
import re
import gzip
import io
import json

#For templates and configrations
url_temp  = 'https://video.coral.qq.com/filmreviewr/c/upcomment/%s?commentid=%s&reqnum=%d'
VideoId =   'yoz60y87rdgl1vp'

#For Regular Expression
##Content Filter
RegExp_jQuery       = 'jQuery.*?_.*?\((.*)\)'

#For simulate the behaviour of web browser
host    = 'video.coral.qq.com'
refer   = 'https://v.qq.com/txyp/coralComment_yp_1.0.htm'
Headers = {
        'Host':             host,
        'Connection':       'keep-alive',
        'Cache-Control':    'max-age=0',
        'User-Agent':       'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
        'Accept':           'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer':          refer,
        'Accept-Encoding':  'gzip, deflate',
        'Accept-Language':  'zh-CN,zh;q=0.8,en;q=0.6',
        'Upgrade-Insecure-Requests':  '1',
        }

def BuildAndInstall_Opener():

    cjar    = http.cookiejar.CookieJar()
    cprocs  = urllib.request.HTTPCookieProcessor(cjar)
    opener  = urllib.request.build_opener(cprocs)
    #httphandler  = urllib.request.HTTPHandler(debuglevel = 1)
    #httpshandler = urllib.request.HTTPSHandler(debuglevel = 1)
    #opener  = urllib.request.build_opener(httpshandler, httphandler, cprocs)
    
    urllib.request.install_opener(opener)

def Decode_GzipString(data):

    buf = io.BytesIO(data)
    gf  = gzip.GzipFile(fileobj = buf)
    data= gf.read()
    return data

def Get_Data(url):

    req = urllib.request.Request(url, None, Headers)
    content = urllib.request.urlopen(req)

    '''get the content'''
    data = content.read()
    #response = content.info()
    #print(response)

    '''data process: Get full data'''
    encoding = content.getheader('Content-Encoding')
    if ( encoding == 'gzip' ):
        data = Decode_GzipString(data)
        #print('[DBG INFO] Content Encoding in GZIP')
    
    # data = re.compile(RegExp_jQuery, re.S).findall(data.decode('utf-8'))
    if len(data) == 0:
        print(data)
        print('[DBG ERR ] Get Data Error ')
    else:
        '''Change the data from json to types in python'''
        data = json.loads(data.decode('utf-8'))

    return data['data']

def Analyse_Comments(data):
    if len(data['commentid']) == 0 :
        print('='*50,'end of comment', '='*50)
        return '0'
    else:
        for comment in data['commentid']:
            print('user:', comment['userinfo']['nick'])
            commstr = comment['content'].replace(u'<p>',u'\r\n\t')
            commstr = re.sub('<[a-zA-Z/]*?>', '',commstr)
            print('comment:', commstr) 
        return data['last']
    
if __name__ == '__main__':
    BuildAndInstall_Opener()
    LastCommentId = ''
    while True:
        url = url_temp % (VideoId, LastCommentId, 10)        
        data = Get_Data(url)
        if len(data) == 0:
            break
        LastCommentId = Analyse_Comments(data) 
        if LastCommentId == '0':
            break
