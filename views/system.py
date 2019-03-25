#encoding=utf8
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.escape import json_decode

from utils import log
from database import party,base
from database.base import session
from service.system import get_system_menu_info
import time


#加载系统信息
class SystemManage(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('system_manage.html')


#查询菜单信息，回显给菜单管理
class SystemManageMenuQuery(RequestHandler):
    def post(self, *args, **kwargs):
        log.info(self.request.arguments)
        data = get_system_menu_info(session)
        time.sleep(6)
        self.write( {"code":"200","total":len(data),"rows":data,"page":"1","limit":"10",'totalCount':'1'} )
        #self.write( {"code":"200","total":0,"rows":""} )
 

#更新菜单信息
class SystemManageMenuUpdate(RequestHandler):
    def post(self, *args, **kwargs):
        log.info(self.request.arguments)
        data = get_system_menu_info(session)
        time.sleep(6)
        self.write( {"code":"200","total":len(data),"rows":data,"page":"1","limit":"10",'totalCount':'1'} )
        #self.write( {"code":"200","total":0,"rows":""} )
 
