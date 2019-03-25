#encoding=utf8
import logging
import os
import time
'''
日志配置

'''


# 第一步，创建一个logger
log = logging.getLogger()
#log.setLevel(logging.INFO)  # Log等级总开关
log.setLevel(logging.DEBUG)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
#rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
rq = time.strftime('%Y%m%d', time.localtime(time.time()))
#log_path = os.path.dirname(os.getcwd()) + '/logs/'
log_path = os.getcwd() + '/logs/'
log_name = log_path + rq + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# 第三步，定义handler的输出格式
LOG_FORMAT="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
formatter = logging.Formatter(LOG_FORMAT)
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
log.addHandler(fh)

sh = logging.StreamHandler()#往屏幕上输出
sh.setFormatter(formatter) #设置屏幕上显示的格式
log.addHandler(sh) 

# 日志
#log.debug('this is a logger debug message')
#log.info('this is a logger info message')
#log.warning('this is a logger warning message')
#log.error('this is a logger error message')
#log.critical('this is a logger critical message')



