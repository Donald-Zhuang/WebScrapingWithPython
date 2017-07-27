#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'
import urllib.request

'''[TEST] for urlopen'''
Content = urllib.request.urlopen('http://www.baidu.com')
# print(Content)

'''[TEST] for read and readline'''
data = Content.read()
# print(data)
#dataline = Content.readline()
#print(dataline)

'''[TEST] for file operation'''
with open('baidu.html','wb') as hBaiduDoc:
    hBaiduDoc.write(data)

filename = urllib.request.urlretrieve("http://www.baidu.com", filename='2.html')
urllib.request.urlcleanup()

'''[TEST] other information'''
print(Content.info())

'''[TEST] some funtions'''
print(Content.getcode()) # get the status code from http header
print(Content.geturl())
encodeUrl = print(urllib.request.quote(Content.geturl()))
print(urllib.request.unquote('http%3A//www.baidu.com'))

#if __name__ == '__main__':

