#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

'''import the libraries'''
import urllib.request
import socket 
import errno

'''Global Variables'''
ProxyAddr   = '221.225.159.69:8118'
UrlToVisit  = 'http://www.baidu.com'

def use_proxy(proxy_addr, url):
    '''build a proxy handler'''
    data = None
    
    proxy   = urllib.request.ProxyHandler({'http':proxy_addr})
    httphd  = urllib.request.HTTPHandler(debuglevel=1)
    httpshd = urllib.request.HTTPSHandler(debuglevel=1)
    
    opener  = urllib.request.build_opener(proxy, httphd, httpshd)
    urllib.request.install_opener(opener)
    
    try:
        data    = urllib.request.urlopen(url).read().decode('utf-8')
    except socket.error as SocketError:
        if SocketError.errno == errno.ECONNRESET:
            print('\r\n[USER Test]Connection reset by peer')
        else:
            pass
    
    return data

if __name__ == '__main__':
    data = use_proxy(ProxyAddr, UrlToVisit)
    if data != None:
        print("\r\n[USER Test] the length of data : %d." % (len(data)) )
        '''write out data for test'''
        with open('test.html','w') as hfile:
            hfile.write(data)
    else:
        print("\r\n[USER Test]Get Nothing")


