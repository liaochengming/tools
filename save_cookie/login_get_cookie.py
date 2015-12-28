# -*- coding:utf-8 -*-
'''
Created on 2015年12月11日

@author: slm
'''
import urllib
import urllib2
import time
import random
import cookielib
import socket
import global_num
# from check_ip.check_proxy import USEFUL_IP_LIST
# USEFUL_IP_LIST = ["124.42.7.103:80"]

class LoginGetCookie(object):
    '''
    登陆并获取cookie
    '''
    def __init__(self, uname, passwd):
        self.uname = uname
        self.passwd = passwd
        self.cookie = ''
        self.userid = ''
        self.last_time = ''
        self.cookie_name = ''
        print len(global_num.USEFUL_IP_LIST)
        while len(global_num.USEFUL_IP_LIST) == 0:
            print 'sleep'
            print len(global_num.USEFUL_IP_LIST)
            time.sleep(5)
        self.ip = random.choice(global_num.USEFUL_IP_LIST)
        self.login_ths()

    def login_ths(self):
        '''
        post请求获得cookie
        '''
        try:
            login_url = 'http://pass.10jqka.com.cn/login'
            cj = cookielib.LWPCookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            params = urllib.urlencode({'act': 'login_submit',
                                       'uname':self.uname,
                                       'passwd':self.passwd,
                                       'captchaCode':'code_str',
                                       'longLogin':'on',
                                       'submit':'登　录'})
            request = urllib2.Request(login_url, params)
            request.set_proxy(self.ip, 'http')
            response = opener.open(request)
            time.sleep(0.5)
        except urllib2.URLError:
            print global_num.USEFUL_IP_LIST
            print '--------time out---------'
            if self.ip in global_num.USEFUL_IP_LIST:
                global_num.USEFUL_IP_LIST.remove(self.ip)
            print global_num.USEFUL_IP_LIST
            self.cookie_name = 'PHPSESSID'
            return
        except socket.timeout:
            print global_num.USEFUL_IP_LIST
            print '--------socket.timeout---------'
            if self.ip in global_num.USEFUL_IP_LIST:
                global_num.USEFUL_IP_LIST.remove(self.ip)
            print global_num.USEFUL_IP_LIST
            self.cookie_name = 'PHPSESSID'
            return
        except Exception, ex:
            print Exception, ":", ex
            print self.ip
            print self.uname
            print self.passwd
            print '------login error------'
            print global_num.USEFUL_IP_LIST
            print len(global_num.USEFUL_IP_LIST)
            self.cookie_name = 'PHPSESSID'
            return
        self.last_time = long(time.time())
        try:
            html = response.read()  # @UnusedVariable
        except:
            pass
        print cj
        self.get_cookie(cj)

    def get_cookie(self, cj):
        '''
        解析获得cookie
        '''
        if cj:
            cookies = ''
            for index, cookie in enumerate(cj):  # @UnusedVariable
                if cookie.name == 'PHPSESSID':
                    self.cookie_name = cookie.name
                    if self.ip in global_num.USEFUL_IP_LIST:
                        global_num.USEFUL_IP_LIST.remove(self.ip)
                    return
                element_str = cookie.name + '=' + cookie.value + ';'
                cookies += element_str
                if cookie.name == 'userid':
                    self.userid = long(cookie.value)
            self.cookie = cookies

def main(uname, passwd):
    '''
    执行
    '''
    login = LoginGetCookie(uname, passwd)
    print login.cookie_name
    print login.uname
    print login.passwd
    print login.last_time
    print login.cookie
    print login.userid

if __name__ == '__main__':
# 221.229.169.246:8080
    ip_list = ["221.229.169.246:8080"]
#     main('005010354235', '710709')
    main('13862013414', '990515')
    