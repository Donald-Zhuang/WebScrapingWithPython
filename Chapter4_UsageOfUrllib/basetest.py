#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'
import urllib.request

file = urllib.request.urlopen('http://www.baidu.com')
#print(file)

data = file.read()
print(data)

with open('baidu.html','wb') as hBaiduDoc:
    hBaiduDoc.write(data)

#dataline = file.readline()
#print(dataline)

#if __name__ == '__main__':

