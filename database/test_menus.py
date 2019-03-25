#encoding=utf8
from user import *

#创建mysql操作对象
Session = sessionmaker(bind=engine)
session = Session()

#增菜单按钮
session.add(Menus(name='客户信息'))
session.commit()
cus_info = session.query(Menus).filter(Menus.name=="客户信息").first()
session.add_all([
    Menus(name='客户信息新增',parent_id=cus_info.id,service='customer_add',remark="客户信息新增"),
    Menus(name='客户信息查询',parent_id=cus_info.id,service='customer_query',remark="客户信息查询")
])
#提交
session.commit()
