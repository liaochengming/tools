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
    def __init__(self, info_id, cookie, last_time, plt_uid, is_valid):
        self.info_id = info_id
        self.cookie = cookie
        self.last_time = last_time
        self.plt_uid = plt_uid
        self.is_valid = is_valid
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
        if self.is_valid == '0':
            update_sql = '''
            UPDATE crawler_cookies SET is_valid = 0 where id = %s''' %self.info_id
        else:
            update_sql = '''
                UPDATE crawler_cookies SET cookie = "%s", last_time = %s, plt_uid = %s, is_valid = 1 where id = %s
                ''' % (self.cookie, self.last_time, self.plt_uid, self.info_id)
        try:
            cursor.execute(update_sql)
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
    SaveCookie('86', '', '1', '0', '0')
#     SaveCookie('86', 'icket=c006345df0b9bea038b67b2aae421834', '2015', '123', '1')

if __name__ == '__main__':
    main()
    