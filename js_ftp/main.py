# -*- coding:utf-8 -*-
from ftplib import FTP
import os
import time

__author__ = 'tudou'


def ftpconnect():
    ftp_server = '180.96.28.71'
    username = 'e_kunyan'
    password = 'server@123'
    ftp = FTP()
    ftp.connect(ftp_server, 21)
    ftp.login(username, password)
    return ftp


def get_time():
    return time.strftime('%Y%m%d', time.localtime())


def download(ftpclient, localpath, ftppath):
    with open(localpath, 'wb') as f:
        ftpclient.retrbinary('RETR ' + ftppath, f.write, 1024)
        f.close()
        print '正在睡眠一小时...'

ftp_client = ftpconnect()

def ready_run():
    # 切换到out目录
    ftp_client.cwd("/out")
    # 获取目录下所有文件名
    date_files = ftp_client.nlst()
    # 判断目录下文件是否为空
    if date_files:
        # 取第一个文件的文件名
        date_file = date_files[0]
        # 切换到日期文件夹下的目录
        ftp_client.cwd("/out/"+date_file)
        # 获取小时文件夹的文件名
        hour_files = ftp_client.nlst()
        # 判断小时文件夹是否为空
        if hour_files:
            # 获取第一个小时文件夹名
            # hour_file = hour_files[0]
            for hour_file in hour_files:
                # 切换到小时文件夹下的目录
                ftp_client.cwd("/out/"+date_file+"/"+hour_file)
                # 获取数据文件名
                data_files = ftp_client.nlst()
                # 设置ftp数据文件path路径
                ftp_path = '/out/%s' % (date_file+"/"+hour_file)
                # 设置存放文件的路径
                local_path = '/home/jsdx/today_data/'
                # 取第一个文件夹
                # if local_files[0]:
                #     # 判断文件夹是否存在
                if not os.path.exists(local_path):
                    # 如果不存在就创建文件夹
                    os.makedirs(local_path)
                    # 遍历数据文件
                for data_file in data_files:
                    if data_file == "part-r-00000":
                        # 下载数据文件
                        print '正在下载'+date_file+hour_file+'...'
                        download(ftp_client, local_path+'jsdx_'+date_file+hour_file, "/out/"+date_file+"/"+hour_file+"/"+data_file)
                        print '下载完成!'
                        # 删除ftp数据文件
                    ftp_client.delete(data_file)
                # 切换工作目录
                ftp_client.cwd("/out/"+date_file)
                # 删除小时目录
                print hour_file
                if hour_file:
                    ftp_client.rmd(hour_file)
                if hour_file == '23':
                    ftp_client.cwd("/out/")
                    ftp_client.rmd(date_file)


if __name__ == '__main__':
    ready_run()



