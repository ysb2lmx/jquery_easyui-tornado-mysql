#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
	database schema 
	---------------
	STATUS
"""
from connect import *

status_type= Table('status_type', con.metadata,
	Column('code', String(32), primary_key = True),
	Column('name', String(128), doc='名称'),
	Column('description', String(256), doc="描述"),
	info={'doc':'状态类型'},
)
status=Table('status',con.metadata,
	Column('id',BigInteger, Sequence('status_seq') ,primary_key=True),
	Column('status_type_code',String(32), ForeignKey('status_type.code') ,nullable=False),
	Column('value',String(128),doc='状态值,这个和status_type_code 一起构成唯一索引',nullable=False),
	UniqueConstraint('status_type_code', 'value', name='status_idx_1'),
	info={'doc':'状态'},
)
sys_para=Table('sys_para',con.metadata,
	Column('id',BigInteger, Sequence('sys_para_seq') ,primary_key=True),
	Column('sys_name', String(64), doc="系统名称"),
	Column('fiscal_date', Date, doc="会计日期"),
	Column('status_id',BigInteger, ForeignKey('status.id')),
	Column('clear_bank', String(16), doc="清算行号"),
	Column('description', String(256), doc="描述"),
	Column('legal_id', BigInteger, ForeignKey('party.id'), nullable=True, doc="法人ID"),
	UniqueConstraint('legal_id', name='sys_para_idx'),
	info={'doc':'状态'},
)

authority_jrnl=Table('authority_jrnl',con.metadata,
	Column('id',BigInteger, Sequence('authority_jrnl_seq') ,primary_key=True),
	Column('operator_type',String(32), doc="操作类型"),
	Column('account_id',BigInteger, ForeignKey('account.id'),doc='账户id'),
	Column('operator_amount',BigInteger,doc='操作金额'),
	Column('peer_id',BigInteger, ForeignKey('account.id'),nullable=True,doc='收款账户id'),
	Column('depend_id',BigInteger, ForeignKey('authority_jrnl.id'),nullable=True,doc='相关流水'),
	Column('organ_name',String(128),doc='执行机关'),
	Column('reason',String(255),doc='执行原因'),
	Column('notice_no',String(256),doc='通知书编号'),
	Column('cert_type1', String(64), doc="证件名称1"),
	Column('cert_no1', String(64), doc="证件号码1"),
	Column('name1', String(64), doc="执行人1名称"),
	Column('cert_type2', String(64), doc="证件名称2"),
	Column('cert_no2', String(64), doc="证件号码2"),
	Column('name2', String(64), doc="执行人2名称"),
	Column('from_date',DateTime,doc='起效时间'),
	Column('thru_date',DateTime,doc='终止时间'),
	Column('bill_no',String(32), doc="票据号码"),
	Column('tran_jrnl_id',BigInteger, ForeignKey('tran_jrnl.id'),doc='关联流水'),

	info={'doc':'有权机关操作流水'},
)

if __name__ == '__main__':
	connect()
	con.metadata.drop_all()
	con.metadata.create_all()
