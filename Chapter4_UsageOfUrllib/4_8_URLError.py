#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request
import urllib.error

urlNormal   = "http://www.baidu.com"
urlForbidden= "https://btso.pw"
urlError    = "http://1111"

def VisitWeb(ReqUrl):
    try:
        data = urllib.request.urlopen(ReqUrl).read()

    # 1. Use HTTPError and URLError to figure the error type
#    except urllib.error.HTTPError as HttpErr:
#        print( '[USER ERRO] [HTTP Error] Code: %d --> Reason: %s' % (HttpErr.code, HttpErr.reason) )
#    except urllib.error.URLError as UrlErr:
#        print( '[USER ERRO] [URL  Error] Reason: %s' % (UrlErr.reason) )
    
    # 2. Only Use URLError to print Error Info
    except urllib.error.URLError as UrlErr:
        if hasattr(UrlErr,"code") and hasattr(UrlErr, "reason"):
            print( '[USER ERRO] [HTTP Error] Code: %d --> Reason: %s' % (UrlErr.code, UrlErr.reason) )
        else:
            print( '[USER ERRO] [URL  Error] Reason: %s' % (UrlErr.reason) )
    else:
        print( '[USER INFO] Length of data: %d' % (len(data)) )

if __name__ == '__main__':
    VisitWeb(urlNormal)
    VisitWeb(urlForbidden)
    VisitWeb(urlError)

