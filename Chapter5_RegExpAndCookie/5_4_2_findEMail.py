#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import urllib.request
import re

ReqUrl = "http://www.shlanbao.cn/contact/"

Pattern_Email = "(?<=mailto:)[\w\.]+@\w+[\.\w+]*" # "\w[.\w]+@\w+[\.\w]*"
def PrintRet(ret):
    if ret == None:
        print("[WARN] Nothing you need has been found in this website.")
    else:
        for i in ret:
            print(i)

def ReadDataFromURL():
    ''' read the data for Regular Expression practise from baidu '''    
    content = urllib.request.urlopen(ReqUrl).read().decode('utf-8')
    #print(content)
    return content

def FindURL(string):
    ret = re.findall(Pattern_Email, string, re.I)
    ret = list(set(ret)) # data deduplication
    return ret
    
if __name__ == '__main__':
    string = ReadDataFromURL()
    PrintRet(FindURL(string))
