#encoding=utf8

from user import *

#创建mysql操作对象
Session = sessionmaker(bind=engine)
session = Session()

#增
obj = Users(name=u'杨少博',extra='sb')
session.add(obj)
session.add_all([
    Users(name='赵晨',extra='cow'),
    Users(name='张存良',extra='cowcow'),
    Users(name='cc',extra='cow'),
    Users(name='dd',extra='cowcow'),
    Users(name='alex',extra='sb')
])
#提交
session.commit()


#删
session.query(Users).filter(Users.id > 2).delete()
#提交
session.commit()

#改
session.query(Users).filter(Users.id > 2).update({"name" : "099"})
session.query(Users).filter(Users.id > 2).update({Users.name: Users.name + "099"}, synchronize_session=False)
session.query(Users).filter(Users.id > 2).update({"id": Users.id + 1}, synchronize_session="evaluate")
session.commit()
# 提交
session.commit()

#查
ret=session.query(Users).all()
#ret = session.query(Users.id, Users.extra).all()    #结果为一个列表
#ret = session.query(Users).filter_by(name='cc').first()
#ret = session.query(Users).filter_by(name='cc').all()
print(type(ret))
print(ret)
print(ret[0].extra)
