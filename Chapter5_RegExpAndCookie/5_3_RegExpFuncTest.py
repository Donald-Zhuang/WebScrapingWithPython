#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import re

OriString   = "apythonHelloWorld123cddddcdcdcdfile\r\ngoodGreetGreat\t"
pattern1    = ".python."
pattern2    = ".cd."

def PrintRet(ret):
    if ret == None:
        print("The result is None.\n")
    else:
        print(ret, end = '\n\n') 
        # print(ret.pan(), end = '\n\n')

print('='*10, 'match','='*10)
ret = re.match(pattern1, OriString)
PrintRet(ret)
ret = re.match(pattern2, OriString)
PrintRet(ret)

print('='*10, 'search','='*10)
ret = re.search(pattern2, OriString)
PrintRet(ret)

print('='*10, 'findall','='*10)
ret = re.findall(pattern2,OriString)
PrintRet(ret)

print('='*10, 'sub','='*10)
ret1 = re.sub(pattern2, "**", OriString )
ret2 = re.sub(pattern2, "**", OriString, 1)
print(ret1)
print(ret2)
