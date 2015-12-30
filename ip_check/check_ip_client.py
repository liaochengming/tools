# -*- coding:utf-8 -*-
'''
doc
'''
import MySQLdb
from get_ip_from_daili666 import GetIPFromDaili666
from check_proxy import CheckProxy
from save_in_db import SaveInDatabase
import time

class Client(object):
    '''
    start
    '''
    all_ip_list = []

    def get_ips_from_db(self):
        '''
        获取当前数据库中ip
        '''
        # 打开数据库连接
        # 192.168.0.2 root crawler hadoop
        # 112.124.49.59 migfm crawler miglab2012
        db = MySQLdb.connect(host='222.73.34.101',
                             user='root',
                             db='crawler_test',
                             passwd='9fWagERpAs6hsikr')
        #使用cursor()方法获取操作游标
        cursor = db.cursor()
        select_sql = 'select * from crawler.crawler_forge_ip;'
        try:
            cursor.execute(select_sql)
        except Exception:
            db.rollback()
            return
        all_rows = cursor.fetchall()
        for row in all_rows:
            dic = {'type':1, 'ip':row[1], 'refuse':0, 'time_out':0, 'used':1}
            self.all_ip_list.append(dic)
        db.commit()
        cursor.close()
        db.close()

    def work(self):
        '''
        开始检测
        '''
        #获得IP
        self.all_ip_list = []
#         get_ip = GetIPs()
        get_ip = GetIPFromDaili666()
        get_ip.start_request()
        self.all_ip_list = get_ip.all_ip_list
        #获得当前数据库的ip
        self.get_ips_from_db()
        #检测有效ip
        check = CheckProxy(self.all_ip_list, self.checked_finished)
        check.start()

    def checked_finished(self, ip_list):
        #存入数据库
        save = SaveInDatabase(ip_list)
        save.connect_sql()

def main():
    while True:
        print 'start'
        client = Client()
        client.work()
        client = None
        time.sleep(30)

if __name__ == '__main__':
    main()
