#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

class PrintMultiTable(object):
    '''print multiplication table'''
    def __init__(self):
        print(u'Start to print the multiplication table')
        self.printMultiTab()
    
    def printMultiTab(self):
        for i in range(1, 10):
            for j in range(1, i+1):
                print( "%d*%d=%d  " % (j, i, j*i ), end = '' )
            print("\r") 
if __name__ == '__main__':
    pt=PrintMultiTable()

