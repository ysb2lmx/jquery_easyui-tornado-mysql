#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
	database schema 
	---------------
	FUNCTIONAL
	使用TRAN表示
"""
from feature import feature, function
from product import product
from connect import *
from party import *


function_appl = Table('function_appl', con.metadata,
  Column('id',BigInteger,Sequence('function_appl_seq'),primary_key=True),
  Column('function_id', BigInteger, ForeignKey('function.id'), doc="功能设置ID"),
  Column('feature_id', BigInteger, ForeignKey('feature.id'), doc="所属特征"),
  Column('from_date', Date, doc="起始日期"),
  Column('thru_date', Date, doc="终止日期"),
  Column('value', String(256), doc="功能设置适用值"),
  info={'doc':'功能设置适用性'},
)

tran_type = Table('tran_type', con.metadata,
  Column('code', String(32), primary_key = True),
  Column('name', String(128), doc="交易类型名称"),
  Column('description', String(256), doc="交易类型描述"),
  info={'doc':'交易类型'},
)

tran = Table('tran', con.metadata,
	Column('id',BigInteger,Sequence('tran_seq'),primary_key=True),
	Column('tran_type_code', String(32), ForeignKey('tran_type.code'), doc="交易类型编码"),
#	Column('classification_id', BigInteger, ForeignKey('classification.id'), doc="所属交易分类"), ##仅用于参考
	Column('code', String(32), doc="交易编码"),
	Column('name', String(128), doc="交易名称"),
	Column('is_allowed_rev', String(32), doc="是否允许反交易"),
	Column('description', String(256), doc="交易描述"),
	Column('tran_process_code', String(32), ForeignKey('tran_process.code'), doc="交易对应流程名称,无流程时，为NULL"),
	Column('tran_status', String(10), doc="交易状态:正常"),
	Column('authz_class', String(10), doc="交易类别：金额、交易、不授权"),
	Column('control_level', String(10), doc="重点监控级别：无、一级、二级、三级"),
	Column('auth_before', String(1), doc="是否后检查授权,Y--后检查,N--先检查"),
	info={'doc':'交付渠道交易'},
)
tran_permit_branch = Table('tran_permit_branch', con.metadata,
  Column('id',BigInteger,Sequence('tran_nonopen_branch_seq'),primary_key=True),
  Column('tran_id', BigInteger, ForeignKey('tran.id'), doc="交易场景ID"),
  Column('branch_id', BigInteger, ForeignKey('branch.id'),  doc="不开放机构ID"),
  Column('flag',  String(2),   doc="Y/N"),
  Column('from_date', DateTime, doc="起始时间"),
  Column('thru_date', DateTime, doc="终止时间"),
	info = {'doc':'交易不开放机构表'}
)

tran_class=Table('tran_class',con.metadata,
  Column('id',BigInteger, Sequence('tran_class_seq'),primary_key=True , doc="分类id"),
  Column('classification_id',BigInteger,ForeignKey('classification.id',onupdate='CASCADE',ondelete='CASCADE'),doc='分类id'),
  Column('tran_id',BigInteger, ForeignKey('tran.id',onupdate='CASCADE',ondelete='CASCADE'),doc='分类交易id'),

  Column('from_date',Date,doc='起效时间'),
  Column('thru_date',Date,doc='终止时间'),

  info={'doc':'交易分类'},
  )

	
tran_feature_appl = Table('tran_feature_appl', con.metadata,
	Column('id',BigInteger,Sequence('tran_feature_appl_seq'),primary_key=True),
	Column('tran_id', BigInteger, ForeignKey('tran.id'), doc="交易ID"),
	Column('feature_id', BigInteger, ForeignKey('feature.id'), doc="交易ID"),
	Column('feature_appl_type_code', String(32), ForeignKey('feature_appl_type.code'), doc="特征应用类型"),
	Column('from_date', Date, doc="起始日期"),
	Column('thru_date', Date, doc="终止日期"),
	Column('value', String(256), doc="适用值"),
	UniqueConstraint('tran_id', 'from_date', name='tran_feature_appl_idx1'),
	info={'doc':'交易特征适用'},
)

tran_process = Table('tran_process', con.metadata,
	Column('code', String(32), doc="流程名称",primary_key=True),
	Column('name', String(128), doc="流程中文名称"),
	Column('description', String(256), doc="流程描述"),
	info={'doc':'交易流程'},
)

tran_task_type = Table('tran_task_type', con.metadata,
	Column('code', String(32), doc="交易任务类型编码", primary_key=True),
	Column('name', String(128), doc="交易任务名称"),
	Column('description', String(256), doc="描述"),
	info={'doc':'交易任务类型'},
)

tran_task = Table('tran_task', con.metadata,
	Column('id',BigInteger,Sequence('tran_task_seq'),primary_key=True),
	Column('tran_task_type_code', String(32), ForeignKey('tran_task_type.code'), doc="交易任务类型"),
	Column('code', String(32), doc="任务编码"),
	Column('name', String(128), doc="任务名称"),
	Column('system', String(128), doc="系统"),
	Column('service', String(128), doc="服务"),
	Column('value', String(256), doc="任务值"),
	#UniqueConstraint('code', name='tran_task_code_idx'),
	info={'doc':'交易任务'},
)

tran_timeout=Table('tran_timeout', con.metadata,
	Column('code', String(32), doc="交易编码", primary_key=True),
	Column('timeout', BigInteger, doc="交易远程超时时间"),
	Column('transaction', String(1), doc="是否包含事务控制"),
	Column('transaction_timeout', BigInteger, doc="全局事件超时时间"),
)

tran_tasks=Table('tran_tasks', con.metadata,
	Column('id',BigInteger,Sequence('tran_tasks_seq'),primary_key=True),
	Column('tran_id', BigInteger, ForeignKey('tran.id'), doc="交易ID"),
	Column('tran_task_id', BigInteger, ForeignKey('tran_task.id'), doc="任务ID"),
	Column('sequence', BigInteger, doc="交易内序列号"),
	Column('is_final_token', String(1), doc="是否最终状态"),
	info={'doc':'交易内任务列表'}
)

""" 交易流水 """
tran_jrnl=Table('tran_jrnl',con.metadata,
	Column('id',BigInteger,Sequence('tran_jrnl_seq'),primary_key=True),
	Column('fiscal_date', Date, doc="会计日期"),
	Column('request_id', BigInteger,ForeignKey('tran_message.id',onupdate='CASCADE',ondelete='CASCADE'),doc='请求ID'),
	Column('respond_id', BigInteger, nullable=True, doc='响应ID'),
	Column('tran_date',DateTime,doc='交易时间'),
	Column('tran_code',String(32),doc='交易编码'),
	Column('channel_id',BigInteger,ForeignKey('channel.id',onupdate='CASCADE',ondelete='CASCADE'),nullable=True, doc='交易渠道'),
	Column('teller_id',BigInteger,ForeignKey('teller.id',onupdate='CASCADE',ondelete='CASCADE'),nullable=True, doc='交易柜员,账务关联柜员'),
	Column('branch_id',BigInteger,ForeignKey('branch.id',onupdate='CASCADE',ondelete='CASCADE'),nullable=True, doc='交易机构'),
	Column('resp_code', String(5), doc="响应码"),
	Column('resp_mesg', String(128), doc="响应信息"),
	Column('status', String(32), doc="状态, 初始化|录入|复核|完成|已冲正|"),
	Column('original_jrnl_id', BigInteger, ForeignKey('tran_jrnl.id'), nullable=True, doc="原流水,适用于复核与授权交易"),
	Column('actual_teller_id', BigInteger, ForeignKey('teller.id'), nullable=True, doc="实际发生柜员"),
	Column('service_name', String(64), doc="服务名称"),
	info={'doc':'交易流水'},
	)

tran_jrnl_relation=Table('tran_jrnl_relation', con.metadata,
	Column('id', BigInteger, Sequence('tran_jrnl_relation_seq'), primary_key=True),
	Column('relation_type_code', String(32), ForeignKey('relation_type.code'), doc="联系类型"),
	Column('from_id', BigInteger, ForeignKey('tran_jrnl.id'), doc="源流水"),
	Column('to_id', BigInteger, ForeignKey('tran_jrnl.id'), doc="目标流水"),
	Column('description', String(256), doc="说明"),
	UniqueConstraint('relation_type_code', 'from_id', 'to_id', name='tran_jrnl_rel_idx'),
	info={'doc':'交易流水联系,主要用于集中授权和集中复核的流水关联'}
)

third_type = Table('third_type', con.metadata,
	Column('code', String(32), primary_key = True),
	Column('name', String(128), doc="第三方业务名称"),
	Column('status', String(32), doc="状态"),
	info={'doc':'第三方业务类型'},
)

""" 第三方流水 """
third_jrnl=Table('third_jrnl',con.metadata,
	Column('id',BigInteger,Sequence('third_jrnl_seq'),primary_key=True),
	Column('jrnl_id', BigInteger, ForeignKey('tran_jrnl.id'), doc="交易流水"),
	Column('third_type_code', String(32), ForeignKey('third_type.code'), doc="业务类型"),
	Column('third_date', String(16), doc="第三方清算日期"),
	Column('third_seq', String(32), doc="第三方流水"),
	Column('original_third_date', String(16), doc="原始的第三方日期"),
	Column('original_third_seq', String(32), doc="原始的第三方流水"),
	Column('tran_time', String(40), doc="交易时间"),
	Column('tran_code', String(16), doc="交易代码"),
	Column('terminal_no', String(32), doc="终端编号"),
	Column('institution_code', String(32), doc="受理机构"),
	Column('acct_no', String(32), doc="交易账号"),
	Column('to_acct', String(32), doc="对方账号"),
	Column('amount',BigInteger, doc='交易金额'),
	Column('status', String(32), doc="流水状态 正常|撤消|冲正"),
	Column('resp_code', String(5), doc="响应码"),
	Column('resp_mesg', String(128), doc="响应信息"),
	Column('check_status', String(32), doc="对账状态 未对账|已对账"),
	)


""" 第三方对账临时表 """
third_check =Table('third_check',con.metadata,
	Column('id',BigInteger,Sequence('third_check_seq'),primary_key=True),
	Column('third_type_code', String(32), ForeignKey('third_type.code'), doc="业务类型"),
	Column('third_date', String(16), doc="第三方清算日期"),
	Column('third_seq', String(32), doc="第三方流水"),
	Column('original_third_date', String(16), doc="原始的第三方日期"),
	Column('original_third_seq', String(32), doc="原始的第三方流水"),
	Column('tran_time', String(40), doc="交易时间"),
	Column('tran_code', String(16), doc="交易代码"),
	Column('terminal_no', String(32), doc="终端编号"),
	Column('institution_code', String(32), doc="受理机构"),
	Column('acct_no', String(32), doc="交易账号"),
	Column('to_acct', String(32), doc="对方账号"),
	Column('amount',BigInteger, doc='交易金额'),
	Column('status', String(32), doc="流水状态 正常|撤消|冲正"),
	Column('check_status', String(32), doc="对账状态 未对账|已对账"),
	UniqueConstraint('third_seq', 'terminal_no', 'institution_code', 'acct_no', name='third_check_idx'),
	)

"""支付宝卡通流水"""
alipay_jrnl=Table('alipay_third_jrnl',con.metadata,
	Column('id',BigInteger, ForeignKey('third_jrnl.id'), primary_key=True),
	Column('handling_charge',BigInteger, doc="手续费"),
	Column('tran_type', String(32), doc="交易类型 提现|支付|退货"),
	Column('card_agreement_no', String(64), doc="卡通协议号"),
	Column('tran_money_code',String(32),doc="交易货币代码"),
	Column('fail_reason', String(128), doc="失败原因"),
	info={'doc':'支付宝卡通第三方流水'},
)

"""新支付宝流水"""
new_alipay_third_jrnl=Table('new_alipay_third_jrnl',con.metadata,
	Column('id',BigInteger, ForeignKey('third_jrnl.id'), primary_key=True),
	Column('handling_charge',BigInteger, doc="手续费"),
	Column('tran_type', String(32), doc="交易类型 网上支付|充值退回"),
	Column('town_date',String(32),doc="村镇日期(YYYYMMDD)"),
	Column('town_jrnl', String(32), doc="村镇流水"),
	info={'doc':'新支付宝第三方流水'},
)

"""手机银行汇款流水"""
mbank_jrnl=Table('mbank_third_jrnl',con.metadata,
	Column('id',BigInteger, ForeignKey('third_jrnl.id'), primary_key=True),
	Column('mobile_no', String(16), doc="手机号码"),
	Column('handling_fee', BigInteger, doc="手续费"),
	Column('customer_no', String(32), doc="客户编号"),
	Column('bill_no', String(32), doc="账单号"),
	Column('acpt_acct_name', String(128), doc="对方户名"),
	Column('acpt_bank_no', String(32), doc="对方行号"),
	Column('acpt_bank_name', String(128), doc="对方行名"),
	Column('tran_type', String(64), doc="交易类型"),
	info={'doc':'手机银行汇款流水表'},
)

"""兴业柜面通第三方流水"""
cib_term_third_jrnl=Table('cib_term_third_jrnl',con.metadata,
	Column('id', BigInteger, ForeignKey('third_jrnl.id'), primary_key=True),
	Column('teller_id', BigInteger, ForeignKey('teller.id'), doc="操作柜员ID"),
	Column('auth_response', String(32), doc="授权应答码"),
	Column('oth_bank_code', String(32), doc="发卡方行号"),
	Column('oth_acct_name', String(128), doc="他行客户名称"),
	Column('accounting_jrnl_id', BigInteger, ForeignKey('tran_jrnl.id'), doc="记账交易流水"),
	Column('tran_date', String(32), doc="交易日期YYYYMMDD"),
	info={'doc':'兴业柜面通第三方流水'},
	)

"""兴业柜面通系统配置"""
cib_sys_para = Table('cib_sys_para', con.metadata,
	Column('code', String(32), primary_key = True),
	Column('cib_settle_date', String(10), doc="兴业清算日期"),
	Column('inst_id', String(11), doc="入网机构标识"),
	Column('cib_inst_id', String(11), doc="兴业标识"),
	Column('cib_status', String(10), doc="兴业状态，日切/日终/正常"),
	info={'doc':'兴业系统参数'},
)

"""烟草代扣第三方流水"""
tobacco_third_jrnl=Table('tobacco_third_jrnl',con.metadata,
	Column('id', BigInteger, ForeignKey('third_jrnl.id'), primary_key=True),
	Column('company_code', String(32), doc="公司代码"),
	Column('customer_code', String(32), doc="客户代码"),
	Column('customer_name', String(32), doc="客户姓名"),
	info={'doc':'烟草代扣第三方流水'},
	)


"""通联贷记卡第三方流水"""
ccs_third_jrnl=Table('ccs_third_jrnl',con.metadata,
	Column('id', BigInteger, ForeignKey('third_jrnl.id'), primary_key=True),
	Column('union_date', String(16), doc="通联清算日期"),
	Column('union_seq', String(32), doc="通联流水"),
	Column('auth_seq', String(32), doc="预授权号"),
	Column('send_code', String(32), doc="发送机构"),
	Column('old_third_jrnl_id', BigInteger, ForeignKey('ccs_third_jrnl.id'), nullable=True, doc="原第三方交易记录的id"),
	Column('channel_id', BigInteger, ForeignKey('channel.id'), doc="渠道" ),
	info={'doc':'贷记卡流水'},
	)

"""网银第三方流水"""
"""交易类型: 查询|个人行内转账|个人批量转账|个人跨行加急|个人跨行普通"""
""" |企业行内转账|企业批量转账|企业批量代发|企业跨行加急|企业跨行普通|网银互联"""
ebank_third_jrnl=Table('ebank_third_jrnl',con.metadata,
	Column('id', BigInteger, ForeignKey('third_jrnl.id'), primary_key=True),
	Column('fiscal_date', Date, doc="会计日期"),
	Column('tran_type', String(32), doc="交易类型"),
	Column('contract_id', BigInteger, ForeignKey('contract.id'), doc="签约ID"),
	Column('handling_fee',BigInteger, doc='手续费'),
	Column('post_fee',BigInteger, doc='邮电费'),
	Column('payee_name', String(512), doc="收款人名称"),
	Column('payee_bank_no', String(32), doc="收款行行号"),
	Column('usage', String(512), doc="用途"),
	Column('acct_type', String(5), doc="收款人账号类型"),
	Column('payer_name', String(512), doc="付款人名称"),
	Column('ip_addr', String(40), doc="ip地址"),
	info={'doc':'网银第三方流水'},
	)


""" 影像类型 """
image_type = Table('image_type', con.metadata,
	Column('code', String(32), doc="影像类型编码", primary_key=True),
	Column('name', String(128), doc="影像名称"),
	Column('description', String(256), doc="描述"),
	info={'doc':'影像类型定义'},
)

""" 交易需要录入的影像数据类型 """
tran_def_images=Table('tran_def_images', con.metadata,
	Column('id', BigInteger, Sequence('tran_def_images_seq'), primary_key = True),
	Column('tran_task_id', BigInteger, ForeignKey('tran_task.id'), doc="交易任务ID"),
	Column('image_type_code', String(32), ForeignKey('image_type.code'), doc="影像类型编码"),
	Column('flag', String(1), doc="标志，为A表示授权影像，T表示交易成功后补录影像"),
	Column('seq', BigInteger, doc="顺序号"),
	info={'doc':'交易需要录入的影像数据'},
)


""" 影像数据 """
images=Table('images', con.metadata,
	Column('id',BigInteger,Sequence('images_id_seq'),primary_key=True),
	Column('image_type_code', String(32), ForeignKey('image_type.code'), doc="影像类型编码"),
	Column('name',String(128),doc='名称'),
	Column('description',String(255),doc='描述'),
	Column('content_key',String(255),doc='影像标识(影像存储系统标识)'),
	Column('create_date',DateTime,doc='创建时间'),
	info = {'doc':'交易影像索引'}
)

""" 交易影像数据 """
tran_images=Table('tran_images', con.metadata,
	Column('id',BigInteger,Sequence('tran_images_seq'),primary_key=True),
	Column('tran_jrnl_id', BigInteger, ForeignKey('tran_jrnl.id'), doc="交易流水号"),
	Column('images_id', BigInteger, ForeignKey('images.id'), doc="影像ID"),
	info= {'doc':'交易影像'}
)

"""影像打印授权"""
images_authz=Table('images_authz', con.metadata,
    Column('id',BigInteger,Sequence('images_authz_seq'),primary_key=True),
    Column('image_type_code', String(32), ForeignKey('image_type.code'), doc="影像类型编>码"),
    Column('authz_id', BigInteger, ForeignKey('authz.id'), doc="授权ID"),
    Column('from_date',Date,doc='起效日期'),
    Column('thru_date',Date,doc='终止日期'),
    info= {'doc':'影像打印授权'}
)

""" 交易报文 """
message_detail=Table('message_detail',con.metadata,
	Column('id',BigInteger,Sequence('message_detail_seq'),primary_key=True),
	Column('message_id', BigInteger,ForeignKey('tran_message.id',onupdate='CASCADE',ondelete='CASCADE'),doc='报文ID'),
	Column('name', String(128),doc='字段名称'),
	Column('value',String(256),doc='字段内容'),

	info={'doc':'交易流水'},
)
	
""" 交易授权记录 """
auth_jrnl=Table('auth_jrnl',con.metadata,
	Column('id',BigInteger,Sequence('auth_jrnl_seq'),primary_key=True),
	Column('tran_jrnl_id', BigInteger,ForeignKey('tran_jrnl.id'),nullable=True,doc='请求ID'),
	Column('auth_type',String(32),doc='授权类型'),
	Column('auth_role',String(32),doc='授权主体'),
	Column('auth_data',String(1024), doc="授权数据"),
	Column('status',String(8),doc='检查结果'),
	Column('result',String(128),doc='失败原因'),

	info={'doc':'授权流水'},
)

dayend_task=Table('dayend_task',con.metadata,
	Column('id',BigInteger,Sequence('dayend_task_seq'),primary_key=True),
	Column('name',String(64),doc='任务名称'),
	Column('step_order',BigInteger,doc='任务步骤'),
	Column('from_date',DateTime,doc='开始时间'),
	Column('thru_date',DateTime,doc='结束时间'),
  Column('status',String(16),doc='任务状态'),
  Column('reason',String(128),doc='失败原因'),
	Column('init_service',String(128),doc='初始化服务'),
	Column('proc_service',String(128),doc='处理服务'),
	Column('fail_service',String(128),doc='失败服务'),
	Column('parallel_num',BigInteger, default=5, doc='并发度'),
	UniqueConstraint('step_order', name='step_order_idx'),
	info={'doc':'日终任务表'},
)

dayend_task_stop=Table('dayend_task_stop',con.metadata,
	Column('id',BigInteger,Sequence('dayend_task_stop_seq'),primary_key=True),
	Column('dayend_task_id', BigInteger,ForeignKey('dayend_task.id'),doc='批量日志任务ID'),
	Column('prompt',String(128),doc='暂停提示'),
	Column('from_date',Date,doc='开始日期'),
	Column('thru_date',Date,doc='结束日期'),
	info={'doc':'登记需要暂停的特殊任务'},
)

dayend_task_relation=Table('dayend_task_relation',con.metadata,
	Column('id',BigInteger,Sequence('dayend_task_relation_seq'),primary_key=True),
	Column('pre_dayend_task_id', BigInteger,ForeignKey('dayend_task.id'),doc='前驱批量日志任务ID'),
	Column('dayend_task_id', BigInteger,ForeignKey('dayend_task.id'),doc='批量日志任务ID'),
	Column('from_date',Date,doc='开始日期'),
	Column('thru_date',Date,doc='结束日期'),
	info={'doc':'日终关系表'},
)

dayend_task_deal=Table('dayend_task_deal',con.metadata,
	Column('id',BigInteger,Sequence('dayend_task_deal_seq'),primary_key=True),
	Column('deal_date',Date,doc='处理日期'),
	Column('dayend_task_id', BigInteger,ForeignKey('dayend_task.id'),doc='批量任务ID'),
	Column('tran_jrnl_id', BigInteger,ForeignKey('tran_jrnl.id'),doc='任务的流水ID'),
	Column('from_date',DateTime,doc='开始时间'),
	Column('thru_date',DateTime,doc='结束时间'),
	Column('status',String(32),doc='任务状态 未处理|初始化|待处理|处理中|失败|完成|暂停'),
	Column('reason',String(128),doc='失败原因'),
	UniqueConstraint('deal_date', 'dayend_task_id', name='dayend_task_deal_idx1'),
	info={'doc':'批量日终处理总状态表'},
)

dayend_task_detail=Table('dayend_task_detail',con.metadata,
	Column('id',BigInteger,Sequence('dayend_task_detail_seq'),primary_key=True),
	Column('task_detail_id', BigInteger, doc='具体任务的ID'),
	Column('dayend_task_deal_id', BigInteger,ForeignKey('dayend_task_deal.id'),doc='批量日志任务ID'),
	Column('tran_jrnl_id', BigInteger,ForeignKey('tran_jrnl.id'),doc='处理单笔任务的流水ID'),
	Column('from_date',DateTime,doc='开始时间'),
	Column('thru_date',DateTime,doc='结束时间'),
	Column('status',String(32),doc='任务状态 待处理|成功|失败'),
	Column('reason',String(128),doc='失败原因'),
	UniqueConstraint('task_detail_id', 'dayend_task_deal_id', name='dayend_task_detail_idx1'),
	info={'doc':'批量日终处理单笔状态表'},
)

daysum_jrnl=Table('daysum_jrnl',con.metadata,
	Column('id',BigInteger,Sequence('daysum_jrnl_seq'),primary_key=True),
	Column('fiscal_date',Date,doc='会计日期'),
	Column('teller_no',String(32),doc='柜员号'),
	Column('total_num',BigInteger,doc='总笔数'),
	Column('succ_num',BigInteger,doc='成功笔数'),
	Column('succ_rate',BigInteger,doc='成功率'),
	Column('type_num',BigInteger,doc='交易类型'),
	Column('fail_type',BigInteger,doc='失败类型'),
	Column('teller_name',String(32),doc='柜员名称'),
)

gmt_message=Table('gmt_message',con.metadata,
	Column('id',BigInteger,Sequence('gmt_message_id'),primary_key=True),
	Column('agent_date',Date,doc='委托日期'),
	Column('message_type',String(32),doc='信息类型'),
	Column('tran_code',String(32),doc='交易编码'),
	Column('tran_seq', String(32), doc="交易序号"),
	Column('send_bank', String(12), doc="发起行号"),
	Column('send_clear', String(12), doc="发起清算行号"),
	Column('recv_bank', String(12), doc="接收行号"),
	Column('recv_clear', String(12), doc="接收清算行号"),
	Column('original_tran', String(32), doc="原交易编码"),
	Column('original_date',Date,doc='原委托日期'),
	Column('original_seq', String(32), doc="原交易序号"),
	Column('original_send_bank', String(12), doc="原发起行号"),
	Column('original_send_clear', String(12), doc="原清算行号"),
	Column('original_recv_bank', String(12), doc="原接收行号"),
	Column('original_recv_clear', String(12), doc="原接收清算行号"),
	Column('original_currency', String(12), doc="原交易币种"),
	Column('original_amount',BigInteger,doc='原交易金额'),
	Column('remarks',String(255),doc='附言'),
	Column('message_status',String(32),doc='信息状态'),
	info={'doc':'城诚事务登记薄'},
)

"""
	plans 的使用和设计：
        ==================
        时间发生器依据plans的配置确定是否需要发送配置中 *计划发送的消息* 到 *计划消息接收队列*,发送的消息例子：
           <Message>
	   	<Head>
			<Channel>PLANS</Channel>
	   	</Head>
		<RequestBodyData>
			<Field name="消息生成时间">20080102140000</Field> <!-- YYYYMMDDhhmmss -->
			<!-- 以下是定义在plan_message中的消息 -->
			<Group name="消息">
				<Field name="方式">测试</Field>
			</Group>

		</RequestBodyData>
           </Message>
	
	所有需要接收计划消息的服务需要监听相应的 *计划消息接收队列* , 处理完成后必须把结果放入 *计划消息回复队列* .
	小额定时发送例子伪代码：
	main() { 
		....
		cb_amq_subscribe( "/queue/beps/sender" );
		while( True )  {
			cb_amq_receive_b64( &msg );

			foreach(record, "BatchEntry",当前批次) {
				sendRecord();
			}
		}
		...
	}
	或者tuxedo服务
	.... TODO

	计划消息回复队列的后续处理，TODO

	缺省计划消息回复队列处理服务，启动方式： plan_reply_server QUEUENAME
"""
plans=Table('plans', con.metadata,
	Column('id',BigInteger, Sequence('plans_id'),primary_key=True),
	Column('plan_month', String(32), nullable=False, doc='计划消息的月,或者 *'),
	Column('plan_weekday', String(32), nullable=False, doc='计划消息的周天 0-6,或者 *'),
	Column('plan_day', String(32), nullable=False, doc='计划消息的天,或者 *'),
	Column('plan_hour', String(32), nullable=False, doc='计划消息的小时,或者 *'),
	Column('plan_minute', String(32), nullable=False, doc='计划消息的分钟,或者 *'),

	Column('plan_queue', String(128), nullable=False, doc="计划消息接收队列"),
	Column('plan_message', String(512), nullable=True,doc="计划发送的消息"),
	Column('plan_reply_queue',String(128),nullable=True,doc="计划消息回复队列"),
	Column('description',String(256),nullable=True,doc="计划任务描述"),
	info={'doc':'计划消息发生器,'},
)

batchmid = Table('batchmid', con.metadata,
	Column('id',BigInteger, Sequence('batchmid_seq'),primary_key=True),
	Column('middate', Date, doc="日切日期"),
	Column('db_scn', BigInteger, doc="数据库SCN"),
	Column('current_stamp', DateTime, doc="日切日期"),
	info = {'doc':'切点信息表'}
)

bankpos_jrnl = Table('bankpos_jrnl', con.metadata,
	Column('id', BigInteger, ForeignKey("third_jrnl.id"), primary_key=True),
	Column('out_branch', String(32), doc="转出机构"),
	Column('out_acct_type', String(32), doc="转出账户类型"),
	Column('in_branch', String(32), doc="转入机构"),
	Column('in_acct_type', String(32), doc="转入账户类型"),
	Column('fee_amount', BigInteger, doc="手续费"),
	Column('merchant_no', String(32), doc="商户号"),
  Column('cups_merchant_no', String(32), doc="银联商户号"),
  Column('cups_terminal_no', String(32),doc="银联终端编号"),
  Column('cups_jrnl_no', String(32), doc="银联中心流水号"),
	info = {'doc':'银联定制终端流水'}
)

#集中支付网银交易流水
ebank_exf_jrnl = Table('ebank_exf_jrnl', con.metadata,
	Column('id', BigInteger, Sequence('ebank_exf_jrnl_seq'),primary_key=True),
	##指令信息
	Column('year', String(4), doc='账本年度'),
 	Column('bill_no', String(6), doc='凭证号,与支付申请号一致'),
 	Column('exchange_code', String(6), doc='单位编码'),
 	Column('payment_type_code', String(32), doc="授权支付,直接支付"),
 	Column('total_money', String(16), doc="实际支付发生金额"),
	Column('fina_code', String(6), doc='财政局代码'),
	Column('ename', String(255), doc='单位名称'),

    Column('pay_bank_code', String(60), doc='付款行编码'),
    Column('pay_bank_name', String(255), doc='付款行名称'),
    Column('pay_bank_no', String(60), doc='付款行账号'),
    Column('rec_name', String(255), doc='收款人名称'),
    Column('rec_bank_name', String(255), doc='收款人开户行名称'),
    Column('rec_bank_no', String(60), doc='收款人账号'),

	Column('fiscal_date', Date, doc="会计日期"),
	Column('work_date', Date, doc="财政工作日期"),

	Column('tran_mode', String(32), doc="交易类型,单笔，批量"),
	Column('reg_jrnl_id', BigInteger,ForeignKey('tran_jrnl.id'),doc='处理单笔任务的流水ID'),
	Column('purpose', String(64),doc="汇款用途"),

	#批量发送登记
	Column('status', String(32), doc="往账状态:待发送, 已发送, 已撤销"),
	Column('reason', String(64),doc="撤销原因"),
	Column('payee_bank_no', String(64),doc="收款行行号"),
	Column('deal_jrnl_id', BigInteger,ForeignKey('tran_jrnl.id'),doc='发送处理流水ID'),

	UniqueConstraint('fina_code', 'bill_no', 'year', 'exchange_code', 'payment_type_code', name='ebank_exf_jrnl_idx1'),

	info = {'doc':'网银集中支付流水登记'}
)

ccbfsc_apply_money = Table('ccbfsc_apply_money', con.metadata,
	Column('id',BigInteger, Sequence('ccbfsc_apply_money_seq'),primary_key=True),
	Column('tran_jrnl_id', BigInteger,ForeignKey('tran_jrnl.id'),doc='发送处理流水ID'),
	Column('entrust_date', String(32), doc="委托日期,以城商行中心日期为准"),
	Column('send_bank', String(32), doc="发起行号"),
	Column('seq', String(32), doc="发起序号"),
	Column('amount', BigInteger, doc="金额"),
	Column('deal_status', String(32), doc="已发送|已收妥|处理成功|处理失败"),
	Column('reason', String(256), doc="失败原因"),
	info = {'doc':'申请城市商业银行清算中心资金划回'}
)

""" ATMP对账登记表 """
atmp_check=Table('atmp_check',con.metadata,
	Column('id',BigInteger,Sequence('atmp_check_seq'), primary_key=True),
	Column('check_time', DateTime, doc="对账时间"),
	Column('third_date', String(16), doc="第三方清算日期"),
	)

""" ATMP对账明细表 """
atmp_check_detail=Table('atmp_check_detail',con.metadata,
	Column('id',BigInteger,Sequence('atmp_check_detail_seq'), primary_key=True),
	Column('atmp_check_id', BigInteger, ForeignKey('atmp_check.id'), doc="对账ID"),
	Column('clear_date', String(32), doc="清算日期"),
	Column('third_seq', String(32), doc="第三方流水号"),
	Column('terminal_no', String(32), doc="终端编号"),
	Column('acct_no', String(32), doc="交易账号"),
	Column('amount',BigInteger, doc='交易金额'),
	Column('tran_type', String(32), doc="存取款类型 存款|取款"),
	Column('already_print', String(32), doc="打印状态 未打印|已打印"),
	Column('error_description', String(128), doc="错误描述"),
	Column('standby', String(128), doc="备用字段"),
	)

""" 反洗钱日间抽取表 """
anti_money=Table('anti_money',con.metadata,
	Column('id',BigInteger,Sequence('anti_money_seq'), primary_key=True),
	Column('fiscal_date', Date, doc='过账会计日期'),
	Column('type_code', String(1), doc="提取类型:1-自然人与自然人的转账 2-自然人与单位的转账 3-单位与单位之间的转账 4-自然人的存取款 5-单位的存取款 6-单位与自然人的转账"),
	Column('tran_jrnl_id', BigInteger, ForeignKey('tran_jrnl.id'), nullable=True, doc="交易流水ID"),
	Column('entry_id', BigInteger, ForeignKey('entry.id'), doc="分录ID"),
	Column('account_id', BigInteger,ForeignKey( 'account.id' ,onupdate='CASCADE',ondelete='CASCADE') , nullable=False,doc='记账账户'),
	Column('peer_id', BigInteger,ForeignKey( 'account.id' ,onupdate='CASCADE',ondelete='CASCADE') , doc='记账对方账户'),
	Column('direct', String(1), doc='借贷标志 1-借 2-贷'),
	Column('money_type', String(1), doc='现转标志 1-现金 2-跨行转账 3-行内转账'),
	Column('tran_type', String(32), doc="交易代码"),
	Column('amount',BigInteger, nullable=False,doc='发生额'),
	Column('fee_amount',BigInteger,doc='交易手续费'),
	Column('party_role_no',String(32),doc='客户编号'),
	Column('usage', String(256), nullable=True,doc="用途"),
	info = {'doc':'反洗钱日间数据抽取表'}
)

""" 日终批量汇总总账短信息登记表 """
send_message=Table('send_message',con.metadata,
	Column('id',BigInteger,Sequence('send_messageseq'), primary_key=True),
	Column('fiscal_date', Date, doc='会计日期'),
	Column('gen_time', DateTime, doc="生成时间"),
	Column('send_phone_no', String(32), doc="手机号码"),
	Column('message', String(1024), doc="短信内容"),
	Column('status', String(32), doc="发送状态 未发送|已发送"),
	info = {'doc':'领导人短信信息表'}
	)

""" 流水状态表,日终流水勾兑信息登记 """
tran_jrnl_status=Table('tran_jrnl_status', con.metadata,
  Column('id', BigInteger, Sequence('tran_jrnl_status_seq'), primary_key=True),
  Column('tran_jrnl_id', BigInteger, ForeignKey('tran_jrnl.id'), doc="流失"),
	Column('check_time', DateTime, doc="勾兑时间"),
	Column('status', String(32), doc="状态:已勾对"),
	Column('teller_no', String(10), doc="柜员号"),
  Column('description', String(256), doc="说明"),
  UniqueConstraint('tran_jrnl_id', name='tran_jrnl_status_idx1'),
  info={'doc':'交易状态表，用于日终勾对'}
)

#转账受理登记薄 包括各渠道（atm, 柜面， 自助设备，网银等）
tt_plans_regist_lock = Table('tt_plans_regist_lock', con.metadata,
	Column('id', BigInteger, Sequence('tt_accept_regist_lock_seq'),primary_key=True),
	Column('tt_plans_regist_lock_id', BigInteger,),
  UniqueConstraint('tt_plans_regist_lock_id', name='tt_plans_regist_lock_idx1'),
)
tt_plans_regist = Table('tt_plans_regist', con.metadata,
	Column('id', BigInteger, Sequence('tt_accept_regist_seq'),primary_key=True),

	Column('payer_acct_id', BigInteger, doc='付款人账户id'),
	Column('payee_acct_id', BigInteger, doc='收款人账户id'),
	Column('amount', BigInteger, doc="发生金额"),

	Column('tt_plan', String(32), doc='计划：实时, 普通，次日(24小时)'),
	Column('tt_type', String(6), doc='行内, 跨行'),
	Column('pay_chnl', String(32), doc='支付渠道, 二代小额, 二代大额'),
	Column('bus_chnl', String(32), doc='业务渠道, ATMP, CUPS, EBANK等'),
	Column('revoked', String(6), doc='是否允许撤销: 是，否'),

	Column('tran_code', String(32), doc='受理交易码'),
	Column('service', String(32), doc='受理服务'),

	Column('reg_jrnl', BigInteger, doc="受理流水"),
	Column('reg_date', DateTime, doc="受理时间"),

	Column('status', String(32), doc="当前状态:待处理, 已处理, 已撤销"),
	Column('code', String(32), doc="处理结果"),
	Column('reason', String(128), doc="处理结果"),

	Column('revoked_jrnl', BigInteger, doc="撤销流水"),
	Column('tt_jrnl', BigInteger, doc="处理流水"),
	Column('tt_date', DateTime, doc="处理时间"),

	Column('temp_acct', BigInteger, doc='转账过渡户'),
	Column('fee_temp_acct', BigInteger, doc='手续费转账过渡户'),
	Column('fee_amount', BigInteger, doc="手续费金额"),
	Column('entry_id', BigInteger, doc='入账分录ID, 销账用'),
	Column('fee_entry_id', BigInteger, doc='费用入账分录ID , 销账用'),

	info={'doc':'转账受理登记薄'},
)

# 转账金额及累计笔数控制
tt_stats_contract = Table('tt_stats_contract', con.metadata,
	Column('id',BigInteger, ForeignKey('contract.id'),primary_key=True),
	Column('channel', String(32), doc='渠道'),
	Column('daily_cnt_limit', BigInteger, doc='日累计笔数'),
	Column('daily_amt_limit', BigInteger, doc='日累计限额'),
	Column('annual_cnt_limit', BigInteger, doc='年累计笔数'),
	Column('annual_amt_limit', BigInteger, doc='年累计限额'),
	info={'doc':'转账累计签约表'},
)

party_role_contract=Table('party_role_contract',con.metadata,
	Column('id',BigInteger, Sequence('party_role_contract_seq') ,primary_key=True),
	Column('party_role_id',BigInteger, ForeignKey('party_role.id',onupdate='CASCADE',ondelete='CASCADE'),doc='账户ID'),
	Column('contract_id',BigInteger, ForeignKey('contract.id',onupdate='CASCADE',ondelete='CASCADE'),doc='分类账户id'),
	Column('from_date',DateTime,doc='起效时间'),
	Column('thru_date',DateTime,doc='终止时间'),
	Column('teller_id',BigInteger, ForeignKey('teller.id'), doc='签约柜员'),
	Column('jrnl_id', BigInteger, ForeignKey('tran_jrnl.id'), doc="签约交易流水"),
	info = {'doc':'客户签约表'},
)

"""通用理财赎回锁"""
finance_jrnl_lock=Table('finance_jrnl_lock',con.metadata,
	Column('id',BigInteger,Sequence('finance_jrnl_lock_seq'),primary_key=True),
	Column('fiscal_date', Date, doc="会计日期"),
    Column('from_date', DateTime, doc="交易时间"), 
    Column('thru_date', DateTime, doc="失效时间"), 
    Column('jrnl_id', BigInteger, ForeignKey('tran_jrnl.id'), doc="交易流水"), 
	Column('tran_code', String(32), doc="交易码"),
	Column('tran_type', String(32), doc="交易类型"),
	Column('acct_no', String(32), doc="账号"),
    Column('product_code', String(32), doc="产品编号"), 
    Column('contract_jrnl', String(32), doc="签约流水"), 
	info={'doc':'理财赎回流水锁'},
)

if __name__ == '__main__':
	connect()
	gmt_message.create()
