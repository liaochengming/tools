# -*- coding:utf-8 -*-
'''
doc
'''
import urllib2
import time
import socket
import random
import global_num
from lxml import html
from check_ip.test_data import Data
from check_ip.get_ip_from_daili666 import GetIPFromDaili666
import threading

socket.setdefaulttimeout(5)#5s后超时

class CheckProxy(object):
    '''
    检测IP有效性
    '''
    user_agents = []
    test_urls = []
    test_ip_list = []
    test_cnt = 0
    callback = None

    def __init__(self):
        self.threads_num = 0
        self.test_ip_list = GetIPFromDaili666().all_ip_list
        if len(global_num.USEFUL_IP_LIST) > 0:
            self.test_ip_list += global_num.USEFUL_IP_LIST
            self.test_ip_list = set(self.test_ip_list)
            global_num.USEFUL_IP_LIST = []
        test = Data()
        self.user_agents = test.user_agents
        self.test_urls = test.test_urls
        for ip in self.test_ip_list:
            while True:
                if self.threads_num < 8:
                    check_thread = threading.Thread(target=self.use_thread, args=(ip,))
                    check_thread.setDaemon(True)
                    check_thread.start()
                    self.threads_num += 1
                    break
                else:
                    time.sleep(1)
#             self.use_thread(ip)

    def use_thread(self, ip):
        '''
        单个线程
        '''
        self.work(ip)

    def work(self, ip):
        '''
        利用urlib连接服务器
        proxy:当前ip和端口
        proxy_dic：存放当前IP的所有信息
        '''
        proxy = {'http':'http://%s' % (ip)}
        spider_url = self.test_urls[0]
        user_agent = random.choice(self.user_agents)
        #设置使用代理
        proxy_support = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        #添加头信息，模仿浏览器抓去网页，对付返回403禁止访问的问题
        i_headers = {'User_Agent': user_agent}
        req = urllib2.Request(spider_url, headers=i_headers)
        try:
            response = urllib2.urlopen(req, timeout=5)
            html_data = response.read()
            doc = html.fromstring(html_data)
            img_url = doc.xpath(r'//img[@id="captchaImg"]//@data-src')
            if len(img_url[0]) > 0:
                #存在验证码
#                 print '===>%s==>需要验证码' % proxy
                self.threads_num -= 1
                return
            global_num.USEFUL_IP_LIST.append(ip)
            print '===>%s==>正常' % proxy
            self.threads_num -= 1
        except urllib2.HTTPError, e:
#             print '===>%s==>无效(%s)' % (proxy, e.reason)
            self.threads_num -= 1
            return
        except Exception:
            self.threads_num -= 1
#             print '===>%s==>无效' % proxy
            return

if __name__ == '__main__':
    while True:
        print 'start'
        CheckProxy()
        time.sleep(30)
