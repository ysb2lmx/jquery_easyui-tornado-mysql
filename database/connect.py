import os
import string
import sqlalchemy

from sqlalchemy import *
from sqlalchemy.orm import mapper, sessionmaker
from conf import DBURL

from sqlalchemy import Table, Column, BigInteger, Integer, String, ForeignKey, Boolean, Date, DateTime,Text
from sqlalchemy.orm import relationship, backref,mapper,composite
from sqlalchemy.schema import Sequence
import datetime

class connect(object):
        pass
con=connect()
Session = sessionmaker()
con.metadata= MetaData()

def connect(url=DBURL):
        con.engine=create_engine(url)
        con.connection=con.engine.connect()
        con.session=Session(bind=con.connection)
        con.metadata.bind=con.engine


def get_table(name):
        return Table(name, con.metadata, autoload=True)

# @brief use to get a database session 
# @return 
def get_session():
        Session = sessionmaker(con.engine)
        return Session()

# @brief create mapper class
# @param clazz
# @param table
# 
# @return 
def get_mapper(clazz, table):
        if isinstance(table, Table):
                return mapper(clazz, table)

        elif isinstance(table, str):
                load_table = get_table(table)
                return mapper(clazz, load_table)

def drop_table( name ):
        get_table(name).drop(con.engine)
def create_table( name ):
        get_table(name).create(con.engine)
if __name__ == '__main__':
        connect()

