# -*- coding:utf-8 -*-
'''
Created on 2015年12月23日

@author: slm
'''
import ConfigParser

class ReadFile(object):
    '''
    读取数据库配置文件
    '''
    def __init__(self):
        self.__read_file()

    def __read_file(self):
        '''
        读取
        '''
        cf = ConfigParser.ConfigParser()
        cf.read('db_unit.conf')
        self.host = cf.get('db_info', 'host')
        self.user = cf.get('db_info', 'user')
        self.passwd = cf.get('db_info', 'passwd')
        self.db = cf.get('db_info', 'db')
        self.time_interval = cf.get('db_info', 'time_interval')
        