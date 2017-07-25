#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'

class PrintFabonacci(object):
    '''print fabonacci sequence'''
    def __init__(self):
        self.fList = [1, 1]
        self.main()
    
    def main(self):
        listlen = input("please input the length of the sequence(range: 3 ~ 50): ")
        self.checkListLength(listlen)
        while len(self.fList) < int(listlen):
            self.fList.append(self.fList[-1] + self.fList[-2])
        print("the result of the fabonacci sequence:\n\t%s " % self.fList)

    def checkListLength(self,listlen):
        listlen = int(listlen)
        if listlen in range(3, 51):
            print("[INPUT]: The input is correct.")
        else:
            print("[INPUT]: The range should be between 3 and 50, please check the input and try again")
            exit()

if __name__ == '__main__':
    funcPF = PrintFabonacci()
