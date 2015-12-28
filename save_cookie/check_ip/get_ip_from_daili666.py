# -*- coding:utf-8 -*-
'''
doc
'''
import urllib2

class GetIPFromDaili666(object):
    '''
    从API中获取ip
    '''
    all_ip_list = []
    api_url = ''

    def __init__(self):
        '''
        '''
        self.all_ip_list = []
        self.api_url = \
        'http://xvre.daili666api.com/ip/?tid=558465838696598&num=50&foreign=none&ports=80,8080'
        while len(self.all_ip_list) == 0:
            self.start_request()

    def start_request(self):
        '''
        从api接口中json中获得IP、port、type
        '''
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; \
    rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        proxy_support = urllib2.ProxyHandler(None)
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        i_headers = {'User_Agent': user_agent}
        req = urllib2.Request(self.api_url, headers=i_headers)
        try:
            data = urllib2.urlopen(req).read()
            ip_port__list = data.split('\r\n')
            for ip_port in ip_port__list:
                #将json中的IP信息存入all_IP_list
                self.all_ip_list.append(ip_port)
        except:
            print '------get ip from daili666api error-------'

if __name__ == '__main__':
    print GetIPFromDaili666().all_ip_list
    