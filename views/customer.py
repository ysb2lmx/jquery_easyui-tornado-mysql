#encoding=utf8
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.escape import json_decode

from utils import log
from database import party

#加载客户信息新增的页面
class CustomerAdd(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('customer_add.html')


#创建视图处理器
class CustomerFormAdd(RequestHandler):
    def post(self, *args, **kwargs):
        log.info(self.request.body_arguments)
        import time
        time.sleep(2)
        log.info(party)
         
        self.write({"code":"0","status":"添加成功"})
