#encoding=utf8
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from tornado.options import define, options
import views
import os

from utils import log

#定义端口配置
define('port', type=int, default=8080)

#创建路由表
urls = [
    (r"/", views.user.Login),
    (r"/index", views.user.Index),
    (r"/index/get_user_info", views.user.IndexUser),
    (r"/index/get_menus_info", views.user.GetMenusInfo),
    (r"/login/login_in", views.user.Login),
    (r"/login/add_user", views.user.Login),
    (r"/login/login_out", views.user.Login),
    (r"/register", views.user.Login),

    #客户信息
    (r"/customer_add", views.customer.CustomerAdd),
    (r"/customer_form_add", views.customer.CustomerFormAdd),



    #系统信息
    (r"/system_manage", views.system.SystemManage),
    (r"/system/system_manage_menu_query", views.system.SystemManageMenuQuery),
    (r"/system/system_manage_menu_update", views.system.SystemManageMenuUpdate),
]

#创建配置-开启调试模式
configs =  {
    'cookie_secret':'0Q1AKOKTQHqaa+N80XhYW7KCGskOUE2snCW06UIxXgI=',
    'xsrf_cookies':False,
    'debug':True,
    'template_path': 'template',
    'static_path': 'static',
    'static_url_prefix': '/static/',
}

log_path = os.path.join(os.path.dirname(__file__), 'logs/log')

#自定义应用
class MyApplication(tornado.web.Application):
    def __init__(self, urls, configs):
        super(MyApplication, self).__init__(handlers=urls, **configs)
#创建服务器
def make_app():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(MyApplication(urls,configs))
    http_server.listen(options.port)
    http_server.start(1)
    #http_server.start(num_processes=1)方法指定开启几个进程，参数num_processes默认值为1，即默认仅开启一个进程；如果num_processes为None或者<=0，则自动根据机器硬件的cpu核芯数创建同等数目的子进程；如果num_processes>0，则创建num_processes个子进程。
    tornado.ioloop.IOLoop.current().start()

#启动服务器
if __name__ == '__main__':
    log.debug("test")
    make_app()
