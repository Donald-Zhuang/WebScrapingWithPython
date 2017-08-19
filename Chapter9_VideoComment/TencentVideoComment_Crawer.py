#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request
import http.cookiejar
import gzip
import io
import json

#For templates and configrations
url_temp  = 'https://video.coral.qq.com/filmreviewr/c/upcomment/%s?commentid=%s&reqnum=%d'

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

    '''data process: Get full data'''
    encoding = content.getheader('Content-Encoding')
    if ( encoding == 'gzip' ):
        data = Decode_GzipString(data)
    
    if len(data) == 0:
        print(data)
        print('[DBG ERR ] Get Data Error ')
    else:
        data = json.loads(data.decode('utf-8'))

    return data['data']

def Analyse_Comments(data):
    if data['retnum'] == 0 :
        print('='*50,'end of comment', '='*50)
        return '0'
    else:
        for comment in data['commentid']:
            if comment['isdeleted'] == '0':
                print('user:', comment['userinfo']['nick'], end = '')
                if comment['replyuser'] != '' :
                    print(' reply to ',comment['replyuser'], end = '')
                commstr = comment['content'].replace(u'<p>',u'\r\n\t')
                commstr = re.sub('<[a-zA-Z/]*?>', '',commstr)
                print('\r\ncomment:', commstr) 
            else:
                print(comment['title'], ' is been deleted.')
        return data['last']
    
if __name__ == '__main__':
    
    BuildAndInstall_Opener()
    LastCommentId = ''
    VideoId = input('Please input the videoid which you want to get its comments: \r\n')
    while True:
        url = url_temp % (VideoId, LastCommentId, 20)        
        data = Get_Data(url)
        if len(data) == 0:
            break
        LastCommentId = Analyse_Comments(data) 
        if LastCommentId == '0':
            break
