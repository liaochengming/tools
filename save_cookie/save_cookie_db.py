# -*- coding:utf-8 -*-
'''
Created on 2015年12月11日

@author: slm
'''
import MySQLdb
from read_db_info import ReadFile

class SaveCookie(object):
    '''
    将cookie信息添加到数据库
    '''
    def __init__(self, unuseful_info_list, useful_info_list):
        self.unuseful_info_list = unuseful_info_list
        self.useful_info_list = useful_info_list
        self.file = ReadFile()
        self.save_cookie()

    def save_cookie(self):
        '''
        存储
        '''
        # 打开数据库连接
        db_connect = MySQLdb.connect(host=self.file.host,
                                     user=self.file.user,
                                     passwd=self.file.passwd,
                                     db=self.file.db)
        #使用cursor()方法获取操作游标
        cursor = db_connect.cursor()
        try:
            if len(self.unuseful_info_list) > 0:
                update_sql = '''
                UPDATE crawler_cookie_info SET is_valid = 0 where id = %s;'''
                cursor.executemany(update_sql, self.unuseful_info_list)
            if len(self.useful_info_list) > 0:
                update_sql = '''
                    UPDATE crawler_cookie_info SET 
                    cookie = "%s",
                    last_time = %s,
                    plt_uid = %s,
                    is_valid = 1 where id = %s;'''
                cursor.executemany(update_sql, self.useful_info_list)
        except:
        # 发生错误时回滚(已存在此数据,更新)
            db_connect.rollback()
            print '-------save error,data has exist-------'
        db_connect.commit()
        cursor.close()
        db_connect.close()

def main():
    '''
    执行
    '''
    uname_info_list = [('ciikie', '1', '1', '178'), ('ciikie22222', '1', '2', '179')]
#     SaveCookie('1', [], uname_info_list)
    SaveCookie([(176)], uname_info_list)

if __name__ == '__main__':
    main()
    