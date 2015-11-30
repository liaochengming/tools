# -tools

back_redis.py　从redis中备份10小时之前的数据

backup_remote_data_files.py　将阿里云上的数据文件拉取到本地服务器上。

load_data.py　解析数据文件并加载到redis中

send_sms.py　发送短信模块

zjdx_data_linux.py 获取本地文件并调用load_data.py加载到redis中，之后执行back_redis.py备份数据，最后通过send_sms.py发送短信通知。

visit_and_search_linux.py　定时执行zjdx_data_linux.py

visit_and_search_service.py　守护进程






