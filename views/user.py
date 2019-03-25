#encoding=utf8
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.escape import json_decode

from utils.logger import log
import database.base as base 
from database.user  import Menus

session  = base.session

from service.user import get_menus_info

def js_message(message_info):
    return json_decode(message_info)
  

#创建视图处理器
class Login(RequestHandler):
    def get(self, *args, **kwargs):
        #self.write('<form method="post"><input type="submit" value="登陆"></form>')
        #self.write("<h1>hello，world</h1>")
        print(self.request.arguments)
        if self.request.arguments.get("Message") is None:
            print("Login get 1")
            self.render('login.html')
        else:
            print("Login get 2")
            self.render('index.html')


    def post(self, *args, **kwargs):
        print(self.request.body_arguments)
        #data = self.request.arguments
        data = json_decode(self.request.body_arguments.get("Message")[0])
        username = data.get("username","")
        password = data.get("username","")
        print(username,password)
        if username != u"杨少博" and password != u"qwe123":
            self.write({"code":"-1","status":"登陆失败"})
        else:
            self.write({"code":"0","status":"登陆成功"})
        #self.render('index.html')

class Index(RequestHandler):
    def get(self, *args, **kwargs):
        print(self.request)
        print(self.request.body_arguments)
        print(self.request.body)
        print(self.request.arguments)
        print(self.request.arguments.get("Message")[0])
        items = self.request.arguments.get("Message")[0] 
        print("index get 1")
        #self.render('index.html', title="欢迎使用杨少博的资产管理系统", items={"username":u"杨少博"})
        data = {
            "title":"主页面",
            "sys_name":"欢迎使用杨少博的资产管理系统",
            "username":"赵晨",
        }

        self.render('index.html', **data)
        #self.write(json_decode(self.request.arguments.get("Message")[0]))

    def post(self, *args, **kwargs):
        print("index post 1")
        print(self.request.arguments)
        print(self.request.body)
        #告知浏览器需要跳转到的url
        #self.redirect('index')
        self.render('index.html')


class IndexUser(RequestHandler):
    def get(self, *args, **kwargs):
        #return {"code":"200","data":{"username":"杨少博"}}
        #self.write({"username":u"杨少博"})
        print("ahahah")

    def post(self, *args, **kwargs):
        #self.redirect('index')
        #return {"username":"杨少博"}
        #print("1ahahah")
        #查询sys_para表,回显当前系统名称
        data = {
            "title":"welcome to yangshaobo is manage system",
            "username":"赵晨",
        }

        self.write( {"code":"200","data":data} )
        #self.write({"username":u"杨少博"})

#获取菜单
class GetMenusInfo(RequestHandler):
    def post(self, *args, **kwargs):
        log.info(self.request.arguments)
        tree_type = json_decode(self.request.arguments.get("Message")[0]).get("tree_type")
        data = get_menus_info(session,"杨少博",tree_type)
        self.write( {"code":"200","data":data} )
 
