#encoding=utf8
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.escape import json_decode

from utils.logger import log
from database.user  import Menus

def get_menus_info(session,user_name,tree_type):
    log.info("查询菜单")
    treeData = []
    sql = "select *from menus where parent_id in (select id from menus where service='%s')"%(tree_type)
    log.info(sql)
    data = session.execute(sql)
    log.info(data)
    for d in data:
        if d.service is not None:
            treeData.append({
                'id' : d.service,
                'text' : d.name,
                'attributes' : {
                'url':"""<iframe id="%s" width="100%%" height="100%%" frameborder="0" src="/%s" fit="true" style="overflow:hidden,width:100%%;height:100%%;margin:0px 0px;"></iframe>"""%(d.service,d.service)
                }
            })
    log.info(treeData)
    return treeData
