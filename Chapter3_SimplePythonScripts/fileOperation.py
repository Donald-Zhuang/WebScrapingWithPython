#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import os

def FileOperation():
    print("to make sure the test.txt is not in this directory.")
    os.system('rm test.txt')
    os.system('ls -l test.txt')
    print('Try to Create a New file')
    fp = open('test.txt','w')
    fp.write('hello world!\r\n')
    fp.close()
    
    os.system('ls -l test.txt')
    os.system('cat test.txt')
    
    with open('test.txt', 'r') as fp:
        st = fp.read()
    print('[FILE] %s' % st)

if __name__ == '__main__':
    FileOperation()
