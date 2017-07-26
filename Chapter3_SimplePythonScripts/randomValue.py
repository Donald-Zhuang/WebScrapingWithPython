#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

import random

class SelectBall(object):
    def __init__(self):
        self.run()
    
    def run(self):
        while True:
            strcnt = input("please input the count of test:")
            try:
                cnt = int(strcnt)
            except ValueError:
                print("The input should be a number, please try again.")
                continue
            else:
                break

        ballcnt = [0,0,0, 0,0,0, 0,0,0, 0]
        for i in range(cnt):
            ballcnt[random.randint(1,10) - 1] += 1
        for i in range(10):
            print( u'num %d, probability: %f' % (i+1, ballcnt[i]*1.0/cnt) )

if __name__ == '__main__':
    funSB = SelectBall()
