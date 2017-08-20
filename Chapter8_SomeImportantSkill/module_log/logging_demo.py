#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
__author__ = 'donald.zhuang'
                                                                                                                                                                                                           
import logging
import logging.config

LogLevel    = logging.DEBUG
MsgFormat   = '%(asctime)s %(filename)s@%(lineno)d %(levelname)-8s%(message)s'
MsgFileName = 'LogMsg.log'

def Config_OutputLogMsg(LogLevel, MsgFormat, MsgFileName ):
    logging.basicConfig(
            level   = LogLevel,
            format  = MsgFormat,
            datefmt = '%Y%m%d@%H:%M:%S',
            filename= MsgFileName,
            filemode= 'a'
            )

    loghandler  = logging.StreamHandler()
    loghandler.setLevel(logging.INFO)
    logformat   = logging.Formatter('%(filename)s@%(lineno)-04d %(levelname)-8s: %(message)s', None, style='%')
    loghandler.setFormatter(logformat)
    logging.getLogger('').addHandler(loghandler)

def Log_Demo():
    logging.debug('debug')
    logging.info('info')
    logging.warning('warning')

if __name__ == '__main__':
    
    #Config_OutputLogMsg(LogLevel, MsgFormat, MsgFileName )
    Log_Demo()
