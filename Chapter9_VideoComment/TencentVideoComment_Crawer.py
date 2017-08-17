#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request
import http.cookiejar
import re
import gzip
import io

host    = 'video.coral.qq.com'
refer   = 'https://v.qq.com/txyp/coralComment_yp_1.0.htm'
url_temp  = 'https://video.coral.qq.com/filmreviewr/c/upcomment/%s?commentid=%d&reqnum=%d'
VideoId =   'yoz60y87rdgl1vp'

#For Regular Expression
##Comment Filter
RegExp_CommentAll   = '"commentid":\[(.*?)\],"targetinfo"'
RegExp_OneComment   = '\{("targetid":.*?,"poked":.*?)\}'
RegExp_LastCommentId    = '"last":"(.*?)",'
##Content Filter
RegExp_Content      = '"content":"(.*?)",'
RegExp_ReplyUser    = '"replyuser":"(.*?)",'
RegExp_User         = '"nick":"(.*?)",'

#For DEBUG test
url = 'https://video.coral.qq.com/filmreviewr/c/upcomment/yoz60y87rdgl1vp?commentid=6294113144277778568&reqnum=3&callback=jQuery1124031176169755473926_1502928590299&_=15029285'

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
    ReplyUser   = re.compile(RegExp_ReplyUser).findall(data.decode('utf-8'))
    User        = re.compile(RegExp_User).findall(data.decode('utf-8'))

    print(eval('u"'+User[0]+'"'), ' reply to ', eval('u"' + ReplyUser[1] + '"'))

if __name__ == '__main__':
    BuildAndInstall_Opener()
    Visit_Website(url)
