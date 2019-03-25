#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
	database schema 
	---------------
	流程
"""
from functional import *
from party import party_role
from status import status

tran_instance = Table('tran_instance', con.metadata,
  Column('id',BigInteger,Sequence('tran_instance_seq'),primary_key=True),
  Column('tran_id', BigInteger, ForeignKey('tran.id'), doc="交易场景ID"),
  Column('actor_id', BigInteger, ForeignKey('party_role.id'), doc="发起人"),
  Column('from_date', DateTime, doc="起始时间"),
  Column('thru_date', DateTime, doc="终止时间"),
  Column('end_status', String(32), doc="终止状态"),
  info={'doc':'流程实例'},
)

tran_status = Table('tran_status', con.metadata,
  Column('id',BigInteger,Sequence('tran_status_seq'),primary_key=True),
  Column('tran_instance_id', BigInteger, ForeignKey('tran_instance.id'), doc="交易场景ID"),
  Column('status_id', BigInteger, ForeignKey('status.id'), doc="场景状态ID"),
  Column('actor_id', BigInteger, ForeignKey('party_role.id'), doc="发起人"),
  Column('from_date', DateTime, doc="起始时间"),
  Column('thru_date', DateTime, doc="终止时间"),
	info = {'doc':'流程实例状态'}
)

task_instance = Table('task_instance', con.metadata,
  Column('id',BigInteger,Sequence('task_instance_seq'),primary_key=True),
  Column('tran_instance_id', BigInteger, ForeignKey('tran_instance.id'), doc="流程实例ID"),
  Column('tran_task_id', BigInteger, ForeignKey('tran_task.id'), doc="交易任务ID"),
  Column('actor_id', BigInteger, ForeignKey('party_role.id'), doc="发起者"),
  Column('create_date', DateTime, doc="任务创建时间"),
  Column('from_date', DateTime, doc="起始时间"),
  Column('thru_date', DateTime, doc="终止时间"),
  Column('end_status', String(32), doc="终止状态"),
  info={'doc':'任务实例'},
)


task_status = Table('task_status', con.metadata,
  Column('id',BigInteger,Sequence('task_status_seq'),primary_key=True),
  Column('task_instance_id', BigInteger, ForeignKey('task_instance.id'), doc="交易场景ID"),
  Column('status_id', BigInteger, ForeignKey('status.id'), doc="交易任务ID"),

  Column('actor_id', BigInteger, ForeignKey('party_role.id'), doc="参与者"),
	Column('context_id',BigInteger,ForeignKey('tran_jrnl.id'), doc="原子交易流水"),
  Column('from_date', DateTime, doc="起始时间"),
  Column('thru_date', DateTime, doc="终止时间"),
	info = {'doc':'任务实例状态'}
)

keywords_type = Table('keywords_type', con.metadata,
	Column('code', String(32), primary_key = True),
	Column('name', String(128), doc = "关键字类型名称"),
	Column('description', String(256), doc = "关键字类型描述"),
	info = {'doc':'关键字类型'},
)

keywords = Table('keywords', con.metadata,
	Column('id', BigInteger, Sequence('keyworks_seq'), primary_key = True),
	Column('keywords_type_code', String(32), ForeignKey('keywords_type.code'), doc = "关键字类型编码"),
	Column('name', String(32), doc = "关键字名称"),
	info = {'doc':'关键字'},
)

tran_keywords = Table('tran_keywords', con.metadata,
	Column('id', BigInteger, Sequence('tran_keywords_seq'), primary_key = True, doc = "交易关键字id"),
	Column('tran_id', BigInteger, ForeignKey('tran.id', onupdate='CASCADE',ondelete='CASCADE'), doc = "交易id"),
	Column('keywords_id', BigInteger, ForeignKey('keywords.id',  onupdate='CASCADE',ondelete='CASCADE'), doc = '关键字id'),
	Column('from_date',Date,doc='起效时间'),
	Column('thru_date',Date,doc='终止时间'),
	info = {'doc':'交易关键字'},
)

interest_jrnl=Table('interest_jrnl', con.metadata,
	Column('id', BigInteger, Sequence('interest_jrnl_seq'), primary_key=True, doc="id"),
	Column('interest_date',Date,doc='结息日期'),
	Column('branch_id', BigInteger, ForeignKey('branch.id'), doc="机构号"),
	Column('type',String(32),doc="类型:单位,个人"),
	Column('amount', BigInteger, doc="利息总额"),
	Column('status',String(32),doc="处理状态"),
)

if __name__ == '__main__':
	connect()
	con.metadata.drop_all()
	con.metadata.create_all()
