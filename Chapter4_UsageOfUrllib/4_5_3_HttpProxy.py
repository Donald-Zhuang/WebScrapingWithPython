#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

'''import the libraries'''
import urllib.request

'''Global Variables'''
ProxyAddr   = '111.155.116.221:8123'
UrlToVisit  = 'http://www.baidu.com'

def use_proxy(proxy_addr, url):
    '''build a proxy handler'''
    proxy   = urllib.request.ProxyHandler({'http':proxy_addr})
    opener  = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    data    = urllib.request.urlopen(url).read().decode('utf-8')
    return data

if __name__ == '__main__':
    data = use_proxy(ProxyAddr, UrlToVisit)
    print(len(data))
    '''write out data for test'''
    with open('test.html','w') as hfile:
        hfile.write(data)

