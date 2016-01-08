# -*- coding:utf-8 -*-
'''
Created on 2015年12月11日

@author: slm
'''
import MySQLdb
import time
import threading
import global_num
from save_cookie_db import SaveCookie
from login_get_cookie import LoginGetCookie
from check_ip.check_proxy import CheckProxy
from read_db_info import ReadFile

class GetCookie(object):
    '''
    获得cookie信息
    '''
    def __init__(self):
        self.uname = ''
        self.passwd = ''
        self.threads_num = 0
        self.vaild_num = 0
        self.request_num = 0
        self.process = 0
        self.file = ReadFile()
        self.time_interval = int(self.file.time_interval)
        self.__use_thread()
        self.get_uname_from_db()

    def __use_thread(self):
        '''
        创建线程
        '''
        self.ip_ckeck = threading.Thread(target=self.start)
        self.ip_ckeck.setDaemon(True)
        self.ip_ckeck.start()

    def start(self):
        '''
        获取代理ip
        '''
        while True:
            print 'start'
            CheckProxy()
            if len(global_num.USEFUL_IP_LIST) > 0:
                time.sleep(30)

    def get_uname_from_db(self):
        '''
        从数据库中取出用户名
        '''
        try:
            db_connect = MySQLdb.connect(host=self.file.host,
                                         user=self.file.user,
                                         passwd=self.file.passwd,
                                         db=self.file.db)
            #使用cursor()方法获取操作游标
            cursor = db_connect.cursor()
            select_sql = '''
            select id, username, passwd, last_time from crawler_cookies order by id desc
            '''
            all_num = cursor.execute(select_sql)
            info = cursor.fetchmany(all_num)
            print info
        except:
        # 发生错误时回滚
            print '------select error------'
            db_connect.rollback()
        db_connect.commit()
        cursor.close()
        db_connect.close()
        old_process = 0.0
        for info_id, uname, passwd, last_time in info:
            self.process += 1
            cur_process = (100.0*self.process/all_num)
            if cur_process-old_process >= 0.5:
                print 'process:%.2f %%' % cur_process
                old_process = cur_process
            old_time = time.mktime(time.localtime(time.time()-self.time_interval))
            if last_time is None or last_time < old_time:
                #时间间隔超过一定范围，更新，否则跳过
                while True:
                    if self.threads_num < 8:
                        get_cookie_thread = threading.Thread(target=self.login_get_cookie,
                                                             args=(info_id,
                                                                   uname,
                                                                   passwd))
                        get_cookie_thread.setDaemon(True)
                        get_cookie_thread.start()
                        self.threads_num += 1
                        self.request_num += 1
                        print 'request num:%d' % self.request_num
                        break
                    time.sleep(1)
#                 self.login_get_cookie(info_id, uname, passwd)
#             else:
#                 print '=======skip, not update====='
                

    def login_get_cookie(self, info_id, uname, passwd):
        '''
        获得cookie
        '''
        login = LoginGetCookie(uname, passwd)
        #如果有验证码再重新登陆一次
        if login.cookie_name == 'PHPSESSID':
            login = None
            login = LoginGetCookie(uname, passwd)
        if login.userid == '':
            is_valid = '0'
        else:
            is_valid = '1'
            self.vaild_num += 1
            print 'valid num:%d' % self.vaild_num
#         print login.cookie
        SaveCookie(info_id, login.cookie, login.last_time, login.userid, is_valid)
        self.threads_num -= 1

def main():
    '''
    执行
    '''
    info = GetCookie()
    print info.uname
    print info.passwd

if __name__ == '__main__':
    main()
    