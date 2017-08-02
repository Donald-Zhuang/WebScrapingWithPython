#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import re

OriString   = "python\npythonworldcdddcdcdcd\nhello123world"

pattern1    = "py" # normal string 
pattern2    = '\n' # nonprinting characters
pattern3    = '\t' # character for abnormal test
pattern4    = '\wcd\s' 
pattern5    = '\shell.*\d'
pattern6    = '\shell.*?\d'
pattern7    = 'cd{3}'
pattern8    = '(cd){2,}' # '(cd){2,}*' is an incorrect expression
pattern9    = '^python'
pattern10   = 'world$'
pattern11   = 'cd+'
pattern12   = '(cd)+' # please notice difference between the result of pattern11 and pattern12
pattern13   = '\s|cddd'
pattern14   = 'Cddd'
pattern13   = '\s|cddd'
pattern13   = '\s|cddd'
pattern13   = '\s|cddd'

def RegExp_Search(pattern, string, flag = 0):

    print("pattern: %s -- flag: %s" % (pattern, flag))    
    ret = re.search(pattern, OriString, flag)
    if ret != None:
        print(ret)
        print(ret.span())
        print("\n")
    else:
        print("None : Nothing Match\n")

if __name__ == '__main__':

    print("Str: %s \n" % (OriString))    
    RegExp_Search(pattern1, OriString)
    RegExp_Search(pattern2, OriString)
    RegExp_Search(pattern3, OriString)
    RegExp_Search(pattern4, OriString)
    RegExp_Search(pattern5, OriString)
    RegExp_Search(pattern6, OriString)
    RegExp_Search(pattern7, OriString)
    RegExp_Search(pattern8, OriString)
    RegExp_Search(pattern9, OriString)
    RegExp_Search(pattern10, OriString)
    RegExp_Search(pattern11, OriString)
    RegExp_Search(pattern12, OriString)
    RegExp_Search(pattern13, OriString)
    RegExp_Search(pattern14, OriString)
    RegExp_Search(pattern14, OriString, re.I)
    
