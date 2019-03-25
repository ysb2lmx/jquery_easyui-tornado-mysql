#encoding=utf8 

from database.base import *

#菜单表
class Menus(Base):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True)
    name = Column(String(32),nullable=False,comment=u"菜单名称")
    parent_id = Column(Integer, comment=u"菜单名称")
    service = Column(String(32), comment=u"服务名")
    remark = Column(String(254), comment=u"备注")


# 用户表
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    extra = Column(String(16))

    __table_args__ = (
    UniqueConstraint('id', 'name', name='uix_id_name'),
        Index('ix_id_name', 'name', 'extra'),
    )


#定义初始化数据库函数
def init_db():
    Base.metadata.create_all(engine)

#顶固删除数据库函数
def drop_db():
    Base.metadata.drop_all(engine)

#初始化表
#drop_db()
#init_db()


