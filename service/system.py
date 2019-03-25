#encoding=utf8
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.escape import json_decode

from utils.logger import log
from database.user  import Menus

def get_system_menu_info(session):
    log.info("查询菜单")
    treeData = []
    sql = "select m.name,IFNULL((select name from menus  where id=m.parent_id),'') parent_name,service,remark from menus m where parent_id is not null"
    log.info(sql)
    data = session.execute(sql)
    log.info(data)
    for d in data:
        if d.service is not None:
            treeData.append({
                'name' : d.name,
                'parent_name' : d.parent_name,
                'service' : d.service,
                'remark' : d.remark
            })
    log.info(treeData)
    return treeData
