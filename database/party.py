#!/usr/bin/python
# -*- coding: utf-8    -*- 
# Copyright (C) if-solutions 
# All Rights Reserved
# Use to create database tables
"""
    database schema 
    ---------------
    party
"""

from connect import *

party_type= Table('party_type', con.metadata,
    Column('code', String(32), primary_key = True),
    Column('name', String(128), doc="名称"),
    Column('description', String(256), doc="描述"),
    info={'doc':'party类型',
        },
)
#类型属性表
party_type_attr=Table('party_type_attr',con.metadata,
    Column('id',BigInteger, Sequence('party_type_attr_seq'),primary_key=True ),
    Column('party_type_code',  String(32), ForeignKey('party_type.code',onupdate='CASCADE',ondelete='CASCADE') ),
    Column('code', String(32), doc = '属性编码'),
    Column('name',  String(128), doc='属性名字' ),
    Column('description',String(256), nullable=True),
    info={'doc':'账户类型属性,所有值都是string'},
    )

party= Table('party', con.metadata,
    Column('id', BigInteger, Sequence('party_seq'), primary_key = True),
    Column('party_type_code',  String(32), ForeignKey('party_type.code',onupdate='CASCADE',ondelete='CASCADE') ),
    Column('comments', String(255), doc="描述"),
    info={'doc':'party'},
    )

party_role_class=Table('party_role_class',con.metadata,
    Column('id',BigInteger, Sequence('party_role_class_seq'),primary_key=True , doc="分类id"),
    Column('class_id',BigInteger,ForeignKey('classification.id',onupdate='CASCADE',ondelete='CASCADE'),doc='分类id'),
    Column('party_role_id',BigInteger, ForeignKey('party_role.id',onupdate='CASCADE',ondelete='CASCADE'),doc='分类party_role id'),

    Column('from_date',DateTime,doc='起效时间'),
    Column('thru_date',DateTime,doc='终止时间'),

    info={'doc':'party_role分类'},
    )
""" party role ,需要标准数据在 role_type: party_role  """

party_role=Table('party_role',con.metadata,
    Column('id',BigInteger, Sequence('party_role_seq'),primary_key=True , doc="party 角色id"),
#    Column('role_id',BigInteger,ForeignKey('role.id',onupdate='CASCADE',ondelete='CASCADE'),doc='所属角色id'),
    Column('role_type_code',String(32),ForeignKey('role_type.code',onupdate='CASCADE',ondelete='CASCADE'),doc='角色类型'),
    Column('party_id', BigInteger, ForeignKey('party.id',onupdate='CASCADE',ondelete='CASCADE'),doc='角色参与者id'),

    Column('party_role_no',String(32),doc='角色编号'),
    Column('from_date',Date,doc='起效时间'),
    Column('thru_date',Date,doc='终止时间'),

    info={'doc':'扮演角色','std':"""
    """},
    )

customer=Table('customer',con.metadata,
    Column('id',BigInteger, ForeignKey('party_role.id') ,primary_key=True),
    Column('account_seq', BigInteger, doc="账户序号"),
    Column('virtual_no', String(32), doc="虚拟客户编号"),
    Column('loan_seq', BigInteger, doc="贷款子帐户序号"),
)

teller_position=Table('teller_position',con.metadata,
    Column('id',BigInteger, Sequence('teller_position_seq'),primary_key=True,doc="柜员岗位id"),
    Column('code',String(32),doc="岗位编号"),
    Column('name', String(128), doc="名称"),
    Column('description', String(256), doc="描述"),
    UniqueConstraint('code', name='teller_position_idx'),
    info={'doc':'柜员岗位'},
    )

teller_level=Table('teller_level',con.metadata,
    Column('id',BigInteger, Sequence('teller_level_seq'),primary_key=True , doc="柜员级别id"),
    Column('level_code',String(32),doc="岗位级别"),
    Column('cash_oper',BigInteger,doc="现金操作金额"),
    Column('transfer_oper',BigInteger,doc="转账操作金额"),
    Column('cash_auth',BigInteger,doc="现金授权金额"),
    Column('transfer_auth',BigInteger,doc="转账授权金额"),
    Column('description', String(256), doc="描述"),
    info={'doc':'岗位级别'},
    )

position_tranlist=Table('position_tranlist',con.metadata,
    Column('id',BigInteger, Sequence('position_tranlist_seq'),primary_key=True ),
    Column('position_id',BigInteger,ForeignKey('teller_position.id'),doc="岗位编号"),
    Column('tran_id', BigInteger, ForeignKey('tran.id'), doc="ID"),
    Column('from_date', Date, doc="开始日期" ),
    Column('thru_date', Date, doc="到期日期" ),
    info={'doc':'岗位交易列表'},
    )

# 序号类型,影像序号、传票套号
serial_type= Table('serial_type', con.metadata,
  Column('code', String(32), primary_key = True),
  Column('name', String(128), doc='名称'),
  Column('description', String(256), doc="描述"),
    Column('max_serial_number', BigInteger, doc="序号最大值"),
  info={'doc':'状态类型'},
)

# 当事人序号
party_serial=Table('party_serial', con.metadata,
    Column('id', BigInteger, Sequence('party_serial_id'), primary_key=True, doc="ID"),
    Column('party_role_id', BigInteger, ForeignKey('party_role.id'), doc="ID"),
    Column('serial_type_code', String(32), ForeignKey('serial_type.code'), doc="序号类型"),
    Column('fiscal_date', Date, nullable=True, doc="会计日期"),
    Column('condition', String(32), nullable=True, doc="其它条件"),
    Column('serial_number', BigInteger, default = 0, doc="序号"),
    info = {'doc':'当事人序号'}
)

branch_type=Table('branch_type',con.metadata,
    Column('code', String(32), primary_key = True),
    Column('name', String(128), doc='名称'),
    Column('description', String(256), doc="描述"),
    info={'doc':'机构角色'},
)

branch=Table('branch',con.metadata,
    Column('id',BigInteger,ForeignKey('party_role.id'),primary_key=True),
    Column('short_name', String(128), doc='机构简称'),
    Column('branch_role',String(32),ForeignKey('branch_type.code'), doc='机构角色'),
    Column('bank_code',String(32),nullable=True, doc="支付系统行号"),
    Column('count_branch',BigInteger,ForeignKey('branch.id'),doc='核算机构'),
    Column('sum_branch',BigInteger,ForeignKey('branch.id'),doc='统计机构'),
    Column('central_delegation',String(1),nullable=False, default="N", doc="集中授权标志"),
    Column('branch_status',String(32),doc='机构状态 正常|关机|工前'),
    Column('legal_bank_id', BigInteger, ForeignKey('party.id'), nullable=True, doc="法人银行"),
    Column('cash_reserve_branch',BigInteger,ForeignKey('branch.id'),doc='现金预约机构'),
    info={'doc':'机构表'},
    )

other_bank= Table('other_bank', con.metadata,
    Column('id',BigInteger,ForeignKey('party.id'),primary_key=True),
    Column('code', String(32), doc="支付系统行号"),
    Column('bank_type', String(5),doc="行别" ),
    Column('clear_bank', String(32),doc="清算行号" ),
    Column('area_code', String(5),doc="城市代码" ),
    Column('status', String(10),doc="状态:正常，退出" ),
    Column('bank_name', String(255),doc="行名" ),
    Column('addr', String(255),doc="地址" ),
    Column('post_code', String(10),doc="邮编" ),
    Column('telephone', String(64),doc="电话" ),
    Column('from_date',Date,doc='起效日期'),
    Column('thru_date',Date,doc='失效时间'),

    Column('join_type', String(5),doc="参与机构类别" ),  #新增字段
 
    #参与机构类别：
    #01--直接参与人行，02--直接参与国库，03--EIS转换中心，04--直接参与商业银行，05—开户特许直接参与者，06—开户特许间接参与者，07--间接参与者，08—无户特许直接参与者(债券)
    Column('legal_person', String(32),doc="所属法人" ),   #新增字段
    Column('higer_bank', String(70),doc="本行上级参与机构" ),  #新增字段
    Column('bear_bank', String(32),doc="承接行行号" ),  #新增字段
    Column('charge_bank', String(32),doc="管辖人行行号" ),  #新增字段
    Column('ccpc_code', String(6),doc="所属CCPC" ),   #新增字段
    Column('auth_oper', String(32),doc="操作权限" ),   #新增字段

    UniqueConstraint('code', name='other_bank_dx1'),
    info={'doc':'其他银行,由于银行的特殊性，考虑不从机构继承'},

)

#一户通代理商机构参数
agent_branch_para=Table('agent_branch_para',con.metadata,
    Column('id',BigInteger, Sequence('agent_branch_para_seq'),primary_key=True),
    Column('branch_id',BigInteger,ForeignKey('branch.id')),
    Column('area_code',String(32),doc='一户通地区编号4位'),
    info={'doc':'代理商机构地区编号表'},
    )

exch_branch_para=Table('exch_branch_para',con.metadata,
    Column('id',BigInteger, Sequence('exch_branch_para_seq'),primary_key=True , doc="机构交易授权id"),
    Column('branch_id',BigInteger,ForeignKey('branch.id')),
    Column('exch_code',String(32),doc='同城提出交换行号 exch_bank_code'),
    Column('exch_clear_branch_id',BigInteger,ForeignKey('branch.id'),doc='和人行进行资金清算的机构'),
    Column('exch_status',String(32),doc='同城状态,加锁|解锁'),
    Column('code',String(32),doc='同城提出交换短交换号'),
    info={'doc':'同城机构参数表'},
    )

teller=Table('teller',con.metadata,
    Column('id',BigInteger,ForeignKey('party_role.id'),primary_key=True),
    Column('branch_id',BigInteger, ForeignKey('branch.id',onupdate='CASCADE',ondelete='CASCADE'),nullable=False),
    Column('position_id',BigInteger, ForeignKey('teller_position.id',onupdate='CASCADE',ondelete='CASCADE'),nullable=False),
    Column('level_id',BigInteger, ForeignKey('teller_level.id',onupdate='CASCADE',ondelete='CASCADE'),nullable=False),
    Column('passwd_errors',BigInteger, doc="密码错误次数"),
    Column('passwd_date',Date,doc='密码修改日期'),
    Column('logout_step',BigInteger,doc='签退步骤,0正常 1现金已轧账 2重空已检查 3已退 4已勾兑'),
    Column('virtual',String(1),default="N",doc='是否虚拟柜员'),
    Column('teller_status',String(32),doc='柜员状态 正常|停用|离职|注销|签到|签退|临时退出|密码错误锁定|退休'),

    info={'doc':'柜员表'},
    )

#柜员交接
teller_transfer=Table('teller_transfer',con.metadata,
    Column('id', BigInteger,Sequence('teller_transfer_seq'), primary_key=True),
    Column('teller_send_id',BigInteger, ForeignKey('teller.id'),doc="交接柜员id"),
    Column('teller_receive_id',BigInteger, ForeignKey('teller.id'),doc="接收柜员id"),
    Column('teller_proxy_id',BigInteger, ForeignKey('teller.id'), doc="委托柜员id"),
    Column('handover_type',String(32),doc="交接类型"),
    Column('transfer_date',DateTime,doc="交接时间"),
    Column('proxy_date',DateTime,doc="委托时间"),
    Column('cont_msg',String(256),doc="内容"),
    Column('branch_id',BigInteger, ForeignKey('branch.id'), doc="交接机构id"),
    Column('teller_supervision_id',BigInteger, ForeignKey('teller.id'), doc="监交柜员id"),
    info={'doc':'柜员交接表'},
    )

channel_virtual_teller=Table('channel_virtual_teller',con.metadata,
    Column('id',BigInteger,Sequence('channel_virtual_teller_seq'),primary_key=True),
    Column('channel_id', BigInteger, ForeignKey('channel.id'), doc="支付渠道ID" ),
    Column('teller_id', BigInteger, ForeignKey('teller.id'), doc="柜员ID" ),
    Column('branch_id', BigInteger, ForeignKey('branch.id'), doc="机构ID" ),
    Column('from_date', Date, doc="开始日期" ),
    Column('thru_date', Date, doc="到期日期" ),

    info={'doc':'渠道虚拟柜员表'},
)

party_role_rollup=Table('party_role_rollup',con.metadata,
    Column('id',BigInteger,Sequence('party_role_rollup_seq'),primary_key=True),
    Column('parent_id',BigInteger,ForeignKey('party_role.id',onupdate='CASCADE',ondelete='CASCADE'),nullable=True,doc='父角色扮演'),
    Column('child_id',BigInteger,ForeignKey('party_role.id',onupdate='CASCADE',ondelete='CASCADE'),nullable=True,doc='子角色扮演'),

#    Column('relation_id',BigInteger, ForeignKey('relation.id',onupdate='CASCADE',ondelete='CASCADE'),nullable=False),
    Column('relation_type_code',String(32), ForeignKey('relation_type.code',onupdate='CASCADE',ondelete='CASCADE'),nullable=False),
    Column('from_date',DateTime,doc='起效时间'),
    Column('thru_date',DateTime,doc='终止时间'),
    info={'doc':'账户角色扮演汇总关系'},
    )

party_role_relation=Table('party_role_relation',con.metadata,
    Column('id',BigInteger,Sequence('party_role_relation_seq'),primary_key=True),
    Column('parent_id',BigInteger,ForeignKey('party_role.id',onupdate='CASCADE',ondelete='CASCADE'),nullable=False,doc='父角色'),
    Column('child_id',BigInteger,ForeignKey('party_role.id',onupdate='CASCADE',ondelete='CASCADE'),nullable=False,doc='子角色'),

#    Column('relation_id',BigInteger, ForeignKey('relation.id',onupdate='CASCADE',ondelete='CASCADE'),nullable=False),
    Column('relation_type_code',String(32), ForeignKey('relation_type.code',onupdate='CASCADE',ondelete='CASCADE'),nullable=False),
    Column('from_date',DateTime,doc='起效时间'),
    Column('thru_date',DateTime,doc='终止时间'),
    info={'doc':'角色关系','TBD':'是否有必要'},
    )

party_role_authc=Table('party_role_authc',con.metadata,
    Column('id',BigInteger, Sequence('party_role_authc_seq'),primary_key=True ),
    Column('party_role_id',BigInteger,ForeignKey('party_role.id',onupdate='CASCADE',ondelete='CASCADE'),doc='所属party角色'),
    Column('authc_id',BigInteger,ForeignKey('authc.id',onupdate='CASCADE',ondelete='CASCADE'),doc='认证方式'),
    Column('from_date',DateTime,doc='起效时间'),
    Column('thru_date',DateTime,doc='终止时间'),
    info={'doc':'角色认证'},
    )


##################################################################
# PARTY CONTACT
##################################################################
""" PARTY 联系方式 """
party_contact_mech = Table('party_contact_mech', con.metadata,
    Column('id', BigInteger, Sequence('party_contact_mech_seq'), primary_key = True),
    Column('party_id', BigInteger, ForeignKey('party.id'), doc="当事人ID"),
    Column('contact_mech_id', BigInteger, ForeignKey('contact_mech.id'), doc="联系方式"),
    Column('role_type_code', String(32), ForeignKey('role_type.code'), doc="角色"),
    Column('from_date', Date, doc="起始日期"),
    Column('thru_date', Date, doc="终止日期"),
)

""" 联系方式用途"""
party_contact_mech_purpose = Table('party_contact_mech_purpose', con.metadata,
    Column('id', BigInteger, Sequence('party_contact_mech_purpose_seq'), primary_key = True),
    Column('party_id', BigInteger, ForeignKey('party.id')),
    Column('contact_mech_id', BigInteger, ForeignKey('contact_mech.id')),
    Column('contact_mech_purpose_type_code', String(32), ForeignKey('contact_mech_purpose_type.code')),
    Column('from_date', Date, doc="起始日期"),
    Column('thru_date', Date, doc="终止日期")
)

""" 联系方式对照表"""
contact_mech = Table('contact_mech', con.metadata,
    Column('id', BigInteger, Sequence('contact_mech_seq'), primary_key = True),
    Column('contact_mech_type_code', String(32), ForeignKey('contact_mech_type.code'), doc="联系方式类型"),
    Column('info_string', String(255), doc="联系方式内容"),
)

""" 联系方式类型描述"""
contact_mech_type = Table('contact_mech_type', con.metadata,
    Column('code', String(32), primary_key = True),
    Column('name', String(128), doc="名称"),
    Column('description', String(256), doc="描述"),
)

"""联系方式类型用途,约定的联系方式可以做何用途?参数表而已"""
contact_mech_purpose = Table('contact_mech_purpose', con.metadata,
    Column('id', BigInteger, Sequence('contact_mech_purpose_seq'), primary_key = True),
    Column('contact_mech_type_code', String(32), ForeignKey('contact_mech_type.code')),
    Column('contact_mech_purpose_type_code', String(32), ForeignKey('contact_mech_purpose_type.code'))
)

""" 联系方式用途类型"""
contact_mech_purpose_type = Table('contact_mech_purpose_type', con.metadata,
    Column('code', String(32), primary_key = True),
    Column('name', String(128), doc="名称"),
    Column('description', String(256), doc="描述"),
)

""" 电话联系方式"""
telecom_number = Table('telecom_number', con.metadata,
    Column('id', BigInteger, ForeignKey('contact_mech.id'), primary_key = True),
    Column('country_code', String(10), doc="国家编码"),
    Column('area_code', String(10), doc="区号"),
    Column('contact_number', String(60), doc="联系号码"),
    Column('description', String(255), doc="描述"),
)

""" 地址联系方式"""
postal_address = Table('postal_address', con.metadata,
    Column('id', BigInteger, ForeignKey('contact_mech.id'), primary_key = True),
    Column('addressee', String(128), doc="收件人"),
    Column('attentionee', String(128), doc="关注人"),
    Column('adress1', String(255), doc="地址1"),
    Column('adress2', String(255), doc="地址2"),
    Column('directions', String(255), doc="指示、标志性方向/地点"),
    Column('city', String(100), doc="指示、标志性方向/地点"),
    Column('postal_code', String(100), doc="邮政编码"),
    Column('postal_code_ext', String(100), doc="邮政编码扩展"),
    Column('country_geo_id', String(32), doc="国家"),
    Column('county_geo_id', String(32),doc="县,郡"),
    Column('state_province_geo_id', String(32), doc="省,州"),
    Column('postal_code_geo_id', String(32), doc="邮政地区"),
    Column('geo_point_id', String(32),doc="其它自定义,如公司销售大区"))

##################################################################
# 证件相关
##################################################################
""" 证件类型 """
certificate_type = Table('certificate_type', con.metadata,
    Column('code', String(32), primary_key = True),
    Column('name', String(128), doc="名称"),
    Column('type', String(32), doc="类型"),
    Column('description', String(256), doc="描述"),
    info = {'doc':'证件类型'},
)

""" 有效证件信息 """
certificate = Table('certificate', con.metadata,
    Column('id', BigInteger, Sequence('certificate_id_seq'), doc="ID", primary_key = True),
    Column('party_id', BigInteger, ForeignKey('party.id')),
    Column('certificate_type_code',String(20),ForeignKey('certificate_type.code'),doc="证件类型"),
    Column('certificate_number', String(32), doc="证件号码" ),
    Column('issue_office', String(100), doc="发证机关" ),
    Column('issue_date', Date, doc="签发日期", default = datetime.date.today),
    Column('expiration_date', Date, doc="到期日期"),
    Column('image_information_id', BigInteger), ### TBD 影像信息，关联到影像数据表
    Column('description', String(255)))

""" 有效证件信息查询记录 """
certificate_record = Table('certificate_record', con.metadata,
    Column('id', BigInteger, Sequence('certificate_record_seq'), doc="ID", primary_key = True),
    Column('branch_id', BigInteger, ForeignKey('branch.id'), doc="机构ID" ),
    Column('code', String(32), doc="交易编码"),
    Column('curr_name', String(40), doc="姓名"), 
    Column('certificate_type_code',String(20),ForeignKey('certificate_type.code'),doc="证件类型"),
    Column('certificate_number', String(32), doc="证件号码" ),
    Column('query_date', Date, doc="查询日期"))

##################################################################
# PERSON 相关
##################################################################

person= Table('person', con.metadata,
    Column('id', BigInteger, ForeignKey('party.id'), primary_key = True),
    Column('current_name', String(40), doc="姓名"),
    Column('current_first_name', String(40), doc="名字"), ##TBD
    Column('current_last_name', String(40), doc="姓氏"), ##TBD
    Column('country_name',String(40),doc="国籍"),
    Column('nation_name',String(20),doc="民族"),
    Column('educate_record',String(20),doc="学历"),
    Column('current_title', String(40), doc="当前职位"),
    Column('current_nick_name', String(40), doc="别名"),
    Column('gender', String(10), doc="性别"),
    Column('birth_date', Date, doc="出生日期"),
    Column('marital_status', String(10), doc="婚姻状况"),
    Column('residence_status', String(1), doc="居民标志"),
    Column('active_status', String(1), doc="客户状态"),
    Column('peasant_flag', String(1), doc="农户标志"),
    Column('area_flag', String(1), doc="境内境外标志"),
    Column('risk_level', String(10), doc="风险等级"),
    Column('current_id_number', String(40), doc="身份证号码"),
    Column('current_id_expire', Date, doc="身份证到期日期"), 
    Column('total_years_work_experience', BigInteger, doc="累计工作年限"),
    Column('professional_title',String(20),doc="职称"),
    Column('work_office', String(100), doc="工作单位"), 
    Column('department', String(40),doc="部门"),
    Column('work_serial',String(20),doc="工号"),
    Column('birth_place', String(40),doc="籍贯"),
    Column('main_income', String(40),doc="主要收入来源"),
    Column('other_income', String(40),doc="其他收入来源"),
    Column('year_incom', BigInteger, doc="年收入"),
    Column('home_year_incom', BigInteger, doc="家庭年收入"),
    Column('support_person', BigInteger, doc="供养人数"),
    Column('affiliate_type', String(1), doc="关联方类型"),
    Column('control_percent', BigInteger, doc="持股比例"),
    Column('occupation', String(100), doc="职业"), 
    Column('description', String(255)),
    Column('area_code', String(32), doc="地区代码"))


##################################################################
# 非个人(组织)相关
##################################################################
organization= Table('organization', con.metadata,
    Column('id', BigInteger, ForeignKey('party.id'), primary_key = True),
    Column('organization_name', String(100), doc="组织名称"),
    Column('english_name', String(100), doc="英文名称"),
    Column('build_date',Date,doc='注册日期'),
    Column('area_code', String(10), doc="注册地代码"),
    Column('organization_nature', String(255), doc="机构性质"),
    Column('organize_form', String(10), doc="组织性质,中文长度"),
    Column('business_type', String(10), doc="行业类别"),
    Column('owner_ship', String(10), doc="所有制性质"),
    Column('business_area', String(255), doc="主营业务范围"),
    Column('sub_area', String(255), doc="附属业务范围"),
    Column('currency_id',BigInteger, ForeignKey('uom.id'), doc="注册资本币种"),
    Column('capital_flang', String(1), doc="中资标志"),
    Column('regist_capital', BigInteger, doc="注册资本"),
    Column('real_capital', BigInteger, doc="实收资本"),
    Column('tax_code', String(32), doc="税务登记编号"),
    Column('company_type', String(2), doc="客户分类"),
    Column('public_type', String(2), doc="公用企业类型"),
    Column('income_level', String(2), doc="收入级别"),
    Column('hold_type', String(2), doc="控股类型"),
    Column('residence_status', String(1), doc="居民标志"),
    Column('rural_city', String(1), doc="农村城市标志"),
    Column('area_flag', String(1), doc="境内境外标志"),
    Column('company_scale', String(2), doc="企业规模"),
    Column('local_finance', String(2), doc="地方融资平台公司标志"),
    Column('finance_nature', String(2), doc="融资平台法律性质"),
    Column('labor_intensive', String(2), doc="劳动密集型企业标志"),
    Column('bank_agent', String(2), doc="是否本行附属经纪人"),
    Column('corporate_person',BigInteger, ForeignKey('party_role.id'),doc="法人代表"),
    Column('group_code', String(8), doc="集团客户编号"),
    Column('relation_type', String(2), doc="关联方类型"),
    Column('control_percent', BigInteger, doc="控股比例"),
    Column('credit_level', String(2), doc="信用等级"),
    Column('economic_type', String(10), doc="企业经济类型"),
    Column('office_site_name', String(100), doc="办公场所"),
    Column('num_empolyees', BigInteger, doc="员工数"),
    Column('ticker_symbol', String(10), doc="股票代码"),
    Column('loan_card', String(20), doc="贷款卡号"),
    Column('account_permit', String(32), doc="开户许可证号"),
    Column('base_account', String(32), doc="基本账号"),
    Column('bank_code', String(12), doc="开户行号"),
    Column('open_branch', String(60), doc="开户银行"),
    Column('taxper_code_national', String(60), doc="纳税人识别号(国税)"),
    Column('national_tax_from_date', Date, doc="国税-税务登记证起始日期"),
    Column('national_tax_thru_date', Date, doc="国税-税务登记证终止日期"),
    Column('taxper_code_land', String(60), doc="纳税人识别号(地税)"),
    Column('land_tax_from_date', Date, doc="地税-税务登记证起始日期"),
    Column('land_tax_thru_date', Date, doc="地税-税务登记证终止日期"),
    Column('register_address', String(255), doc="注册(登记)地址"),
    Column('status', String(8), doc="机构状态:1-正常,2-注销"),
    Column('organization_type', String(8), doc="组织机构类别"),
    Column('description', String(255)),
    Column('bank_certno', String(32), doc="金融机构代码证"),
    Column('bank_level', String(32), doc="客户风险评级"),
    Column('institution_credit_no', String(32), doc="机构信用代码证"),
    Column('district_code', String(32),  doc="行政区划码"),
)

""" 交易报文数据 """
tran_message=Table('tran_message',con.metadata,
    Column('id',BigInteger, Sequence('tran_message_seq'),primary_key=True , doc="上下文id"),
    Column('code', String(32)),
    Column('data',Text,doc='数据内容'),

    info={'doc':'上下文数据'},
    )

""" 机构状态 """
branch_status=Table('branch_status',con.metadata,
    Column('id',BigInteger, Sequence('branch_status_seq'),primary_key=True , doc="机构状态id"),
    Column('branch_id', BigInteger,ForeignKey('branch.id',onupdate='CASCADE',ondelete='CASCADE'),doc='机构角色ID'),
    Column('status_id',BigInteger,ForeignKey('status.id',onupdate='CASCADE',ondelete='CASCADE'),doc='状态'),
    Column('from_date',DateTime,doc='起效时间'),
    Column('thru_date',DateTime,doc='终止时间'),
    info={'doc':'机构状态'},
    )

""" 机构授权参数 """
branch_authz=Table('branch_authz',con.metadata,
    Column('id',BigInteger, Sequence('branch_authz_seq'),primary_key=True , doc="机构授权id"),
    Column('branch_id', BigInteger,ForeignKey('branch.id',onupdate='CASCADE',ondelete='CASCADE'),doc='机构角色ID'),
    Column('authz_id',BigInteger,ForeignKey('authz.id',onupdate='CASCADE',ondelete='CASCADE'),doc='授权ID'),
    Column('from_date',Date,doc='起效时间'),
    Column('thru_date',Date,doc='终止时间'),
    info={'doc':'机构授权检查类型'},
    )

""" 柜员授权参数 """
teller_authz=Table('teller_authz',con.metadata,
    Column('id',BigInteger, Sequence('teller_authz_seq'),primary_key=True , doc="柜员授权id"),
    Column('teller_id', BigInteger,ForeignKey('teller.id',onupdate='CASCADE',ondelete='CASCADE'),doc='柜员角色ID'),
    Column('authz_id',BigInteger,ForeignKey('authz.id',onupdate='CASCADE',ondelete='CASCADE'),doc='授权ID'),
    Column('from_date',DateTime,doc='起效时间'),
    Column('thru_date',DateTime,doc='终止时间'),
    info={'doc':'柜员授权检查类型'},
    )

""" 交易授权参数 """
tran_authz=Table('tran_authz',con.metadata,
    Column('id',BigInteger, Sequence('tran_authz_seq'),primary_key=True , doc="交易授权id"),
    Column('tran_id', BigInteger,ForeignKey('tran.id',onupdate='CASCADE',ondelete='CASCADE'),doc='交易ID'),
    Column('authz_id',BigInteger,ForeignKey('authz.id',onupdate='CASCADE',ondelete='CASCADE'),doc='授权ID'),
    Column('from_date',Date,doc='起效时间'),
    Column('thru_date',Date,doc='终止时间'),
    info={'doc':'交易授权检查类型'},
    )
""" 交易认证参数 """
tran_authc=Table('tran_authc',con.metadata,
    Column('id',BigInteger, Sequence('tran_authc_seq'),primary_key=True , doc="交易认证id"),
    Column('tran_id', BigInteger,ForeignKey('tran.id',onupdate='CASCADE',ondelete='CASCADE'),doc='交易ID'),
    Column('authc_id',BigInteger,ForeignKey('authc.id',onupdate='CASCADE',ondelete='CASCADE'),doc='认证ID'),
    Column('from_date',Date,doc='起效时间'),
    Column('thru_date',Date,doc='终止时间'),
    info={'doc':'交易认证检查类型'},
    )

branch_tran_authz=Table('branch_tran_authz', con.metadata,
    Column('id',BigInteger, Sequence('branch_tran_authz_seq'),primary_key=True , doc="机构交易授权id"),
    Column('branch_id', BigInteger, ForeignKey('branch.id'), doc="机构ID"),
    Column('authz_id',BigInteger,ForeignKey('authz.id',onupdate='CASCADE',ondelete='CASCADE'),doc='授权ID'),
    Column('tran_id', BigInteger, ForeignKey('tran.id'), doc='交易'),
    Column('from_date',Date,doc='起效时间'),
    Column('thru_date',Date,doc='终止时间'),
    info={'doc':'机构交易授权检查类型'},
)

""" 法人机构参数 """
branch_para=Table('branch_para',con.metadata,
#    Column('id',BigInteger, Sequence('branch_para_seq'),primary_key=True , doc="机构参数id"),
    Column('id', BigInteger,ForeignKey('party_role.id',onupdate='CASCADE',ondelete='CASCADE'),primary_key=True ,doc='法人机构角色ID'),
    Column('work_date',Date,doc='营业日期'),
    info={'doc':'法人机构参数'},
    )

""" 柜员状态 """
teller_status=Table('teller_status',con.metadata,
    Column('id',BigInteger, Sequence('teller_status_seq'),primary_key=True , doc="柜员状态id"),
    Column('teller_id', BigInteger,ForeignKey('teller.id',onupdate='CASCADE',ondelete='CASCADE'),doc='柜员角色ID'),
    Column('status_id',BigInteger,ForeignKey('status.id',onupdate='CASCADE',ondelete='CASCADE'),doc='状态'),
    Column('from_date',DateTime,doc='起效时间'),
    Column('thru_date',DateTime,doc='终止时间'),
    info={'doc':'柜员状态'},
    )

"""ATM设备登记簿,  待删除
atm_register=Table('atm_register', con.metadata,
    Column('id', BigInteger, Sequence('atm_register_seq'), primary_key=True, doc="ATM机具ID"),
    Column('atm_no', String(32), doc="ATM机具编号"),
    Column('branch_id', BigInteger, ForeignKey('branch.id'), doc="记账机构"),
    Column('save_teller_id', BigInteger, ForeignKey('teller.id'), doc = "存款尾箱记账操作员"),
    Column('draw_teller_id', BigInteger, ForeignKey('teller.id'), doc = "取款尾箱记账操作员"),
    Column('atm_status', String(32), doc="ENABLE:启用|DISABLE:停用"),
    Column('address', String(256), doc="ATM地址"),
    Column('from_date', DateTime, doc='起效时间'),
    Column('thru_date', DateTime, doc="终止时间"),
    info={'doc':'ATM设备登记簿'},
)
"""

"""押运线路管理"""
escort_route=Table('escort_route', con.metadata,
    Column('id', BigInteger, Sequence('escort_route_seq'), primary_key=True, doc="押运线路ID"),
    Column('escort_route_no', String(32), doc="线路号"),
    Column('branch_id', BigInteger, ForeignKey('branch.id', onupdate='CASCADE',ondelete='CASCADE'), doc='操作机构id'),
    Column('teller_id', BigInteger,ForeignKey('teller.id',onupdate='CASCADE',ondelete='CASCADE'),doc='操作柜员ID'),
    Column('from_date', DateTime, doc='起效时间'),
    Column('thru_date', DateTime, doc="终止时间"),
    info={'doc':'押运线路管理'},
)

"""榐员指纹"""
teller_finger=Table('teller_finger', con.metadata,
    Column('id', BigInteger, Sequence('teller_finger_seq'), primary_key=True, doc="柜员指纹ID"),
    Column('teller_id', BigInteger,ForeignKey('teller.id',onupdate='CASCADE',ondelete='CASCADE'),doc='操作柜员ID'),
    Column('finger_feature_0', String(512), doc="指纹特征值0"),
    Column('finger_feature_1', String(512), doc="指纹特征值1"),
    Column('finger_feature_2', String(512), doc="指纹特征值2"),
    Column('finger_feature_3', String(512), doc="指纹特征值3"),
    Column('finger_feature_4', String(512), doc="指纹特征值4"),
    Column('finger_feature_5', String(512), doc="指纹特征值5"),
    Column('finger_feature_6', String(512), doc="指纹特征值6"),
    Column('finger_feature_7', String(512), doc="指纹特征值7"),
    Column('finger_feature_8', String(512), doc="指纹特征值8"),
    Column('finger_feature_9', String(512), doc="指纹特征值9"),
    Column('availabe_fingers', String(2), doc="启用指纹,如10代表finger1与finger0"),
    Column('remark', String(100), doc="备注"),
    Column('from_date', DateTime, doc='起效时间'),
    Column('thru_date', DateTime, doc="终止时间"),
    info={'doc':'柜员指纹'},
)

teller_login= Table('teller_login', con.metadata,
    Column('id', BigInteger, Sequence('teller_login_seq'), primary_key=True, doc="柜员指纹ID"),
    Column('teller_id', BigInteger,ForeignKey('teller.id',onupdate='CASCADE',ondelete='CASCADE'),doc='操作柜员ID'),
    Column('journal_id', BigInteger, ForeignKey('tran_jrnl.id'), doc="流水号"),
        Column('login_type', String(32), doc="登录方式"),
        Column('description', String(256), doc="描述"),
    Column('from_date', DateTime, doc='起效时间'),
    Column('thru_date', DateTime, doc="终止时间"),
        info={'doc':'柜员登录方式'},
)

#农保客户信息表
medins_cust=Table('medins_cust', con.metadata,
    Column('id',BigInteger, Sequence('medins_cust_seq') ,primary_key=True),
     Column('medi_id', String(32), doc='医疗卡号'),
     Column('card_no', String(32), doc='百合卡卡号'),
     Column('medi_no', String(32), doc='合作医疗号'),
     Column('cust_name', String(128), doc='客户名称'),
     Column('id_num', String(20), doc='身份证号码'),
     Column('gender', String(10), doc="性别"),
     Column('birth_date', Date(), doc='出生年月'),
     Column('addr', String(255),doc="地址" ),
     Column('party_role_id', BigInteger, ForeignKey('party_role.id'), nullable=True, doc='关联客户'),
)

#农保客户状态表: 已导入 已制卡 已配卡 已开户 已激活 已撤销
medins_cust_status=Table('medins_cust_status', con.metadata,
     Column('id', BigInteger, Sequence('medins_cust_status_seq'), primary_key = True),
     Column('medins_cust_id', BigInteger, ForeignKey('medins_cust.id'), doc='农保信息ID'),
     Column('status_id', BigInteger, ForeignKey('status.id'), doc='状态'),
     Column('from_date', DateTime, doc="起始时间"),
     Column('thru_date', DateTime, doc="终止时间"),
     Column('journal_id', BigInteger, ForeignKey('tran_jrnl.id'), doc="状态变更流水"),
     Column('teller_id',BigInteger,nullable=True, doc='操作柜员'),
     Column('branch_id',BigInteger,nullable=True, doc='操作机构'),
     Column('description',String(256), doc='描述'),
)
""" 柜员变动 """
teller_change=Table('teller_change',con.metadata,
    Column('id',BigInteger, Sequence('teller_change_seq'),primary_key=True , doc="柜员变动id"),
    Column('teller_id', BigInteger,ForeignKey('teller.id'),doc='柜员角色ID'),
    Column('tran_jrnl_id', BigInteger,ForeignKey('tran_jrnl.id'),doc='柜员变更流水号'),
    Column('branch_id',BigInteger,ForeignKey('branch.id'),doc='原柜员机构ID'),
    Column('position_id',BigInteger,ForeignKey('teller_position.id'),doc='原柜员岗位ID'),
    Column('level_id',BigInteger,ForeignKey('teller_level.id'),doc='原柜员级别ID'),
    Column('login_type',String(32),doc='柜员登陆方式'),
    Column('teller_status',String(256),doc='柜员状态'),
    Column('new_branch_id',BigInteger,ForeignKey('branch.id'),doc='新柜员机构ID'),
    Column('from_date',Date,doc='岗位起效时间'),
    Column('thru_date',Date,doc='岗位终止时间'),
    Column('change_date',Date,doc='变动时间'),
    info={'doc':'柜员变动'},
)

"""社区银行机构编码表"""
community_branch=Table("community_branch", con.metadata,
    Column('id', BigInteger, Sequence('community_branch_seq'), primary_key = True),
    Column('tran_jrnl_id', BigInteger,ForeignKey('tran_jrnl.id'),doc='交易流水'),
    Column('code', String(32), doc='社区支行编号'),
    Column('branch_id', BigInteger, ForeignKey('branch.id'), doc='社区银行所属机构id'),
    Column('community_name', String(256), doc='社区银行名称'),    
    Column('status', String(32), doc='状态'),    
    Column('remark', String(256), doc='备用'),
)
""" 社区银行柜员表 """
community_teller=Table("community_teller", con.metadata,
    Column('id', BigInteger, Sequence('community_teller_seq'), primary_key = True),
    Column('teller_id', BigInteger, ForeignKey('teller.id'), doc='社区银行柜员id'),
    Column('community_name', String(256), doc='社区银行名称'),
    Column('from_date',Date,doc='岗位起效时间'),
    Column('thru_date',Date,doc='岗位终止时间'),
    Column('teller_status',String(256),doc='柜员状态'),
    Column('remark', String(256), doc='备用'),
)

""" 自助设备类型表 """
device=Table("device", con.metadata,
  Column("id", BigInteger, Sequence('device_seq'), primary_key = True),
  Column("teller_id", BigInteger, ForeignKey('teller.id'), doc='自助设备虚拟柜员id'),
  Column("device_type_code", String(64), doc='自助设备类型:自助发卡机，现金循环机'),
  Column("bank_type", String(64), doc='银行类型，用于区分普通支行和社区银行'),
  Column("bank_name", String(256), doc='对应支行的名称，社区银行填写社区银行名称'),
)

ebank_bank_message=Table('ebank_bank_message', con.metadata,
    Column('id',BigInteger, Sequence('ebank_bank_message_seq'), primary_key=True),
    Column('bank_code', String(32), doc="支付系统行号"),
    Column('bank_name', String(255), doc="行名" ),
    Column('status', String(10), doc="状态:正常，退出"),
    Column('property', String(10), doc="属性"),
    Column('clear_bank', String(32), doc="清算行号"),
    Column('group_type', String(10), doc="组类别"),
    Column('addr', String(255), doc="地址"),
    Column('post_code', String(10), doc="邮编"),
    Column('telephone', String(64), doc="电话"),
    Column('from_date', String(16), doc='起效日期'),
    Column('thru_date', String(16), doc='失效时间'),
    Column('new_type', String(10), doc='最新变更类型'),
    Column('buss_auth', String(20), doc='业务权限'),
    Column('remarks', String(255), doc='备注'),
    info={'doc':'行名行号'},
)

""" 代理人信息表 """
proxy_contact_mech = Table('proxy_contact_mech', con.metadata,
    Column('id',BigInteger, Sequence('proxy_contact_mech_seq'), primary_key=True),
    Column('cert_number', String(64), doc="代理人证件号码" ),
    Column('cert_type', String(32), doc="代理人证件类型"),
    Column('cert_name', String(128), doc="代理人姓名"),
    Column('acct_no', String(64), doc="卡/账号"),
    Column('acct_name', String(128), doc="账户名称"),
    Column('branch_name', String(256), doc="网点名称"),
    Column('fiscal_date', Date, doc='交易日期'),
    Column('tran_jrnl_id', BigInteger, ForeignKey('tran_jrnl.id'), doc="交易流水"),
    Column('cert_id', BigInteger, ForeignKey('certificate.id'), doc="客户证件信息"),
    Column('contact_mech_id', BigInteger, ForeignKey('contact_mech.id'), doc="联系方式"),
    Column('reserve_phone_no', String(128), doc="预留手机号码"),
    Column('telephone', String(128), doc="电话号码"),
    Column('remarks', String(255), doc='备注:预留字段'),
    info={'doc':'代理人信息表'},
)
#客户状态联系表
party_role_status=Table('party_role_status', con.metadata,
    Column('id', BigInteger, Sequence('party_role_status_seq'), primary_key = True),
    Column('party_role_id', BigInteger, ForeignKey('party_role.id'), doc='ID'),
    Column('status_id', BigInteger, ForeignKey('status.id'), doc='状态'),
    Column('from_date', DateTime, doc="起始时间"),
    Column('thru_date', DateTime, doc="终止时间"),
    Column('journal_id', BigInteger, ForeignKey('tran_jrnl.id'), doc="状态变更流水"),
    Column('teller_id',BigInteger,nullable=True, doc='操作柜员'),
    Column('branch_id',BigInteger,nullable=True, doc='操作机构'),
    Column('description',String(256), doc='描述'),
)

#辅助证件信息登记,原因:因为原有的证件信息表中如果再登记,需要改很多代码,为了不影响正常的有效身份证,故此登记
other_certificate = Table('other_certificate', con.metadata,
    Column('id', BigInteger, Sequence('other_certificate_seq'), doc="ID", primary_key = True),
    Column('party_id', BigInteger, ForeignKey('party.id')),
    Column('certificate_type_code',String(20),ForeignKey('certificate_type.code'),doc="证件类型"), 
    Column('certificate_number', String(32), doc="证件号码" ),
    Column('issue_office', String(100), doc="发证机关" ),
    Column('issue_date', Date, doc="签发日期", default = datetime.date.today),
    Column('expiration_date', Date, doc="到期日期"), 
    Column('image_information_id', BigInteger), ### TBD 影像信息，关联到影像数据表
    Column('description', String(255)),
    info={'doc':'辅助证件信息登记'}, 
)

if __name__ == '__main__':
    connect()
    #con.metadata.create_all()
    party_type.drop(checkfirst=True)
    party_type.create(checkfirst=True)
    
    party.drop(checkfirst=True)
    party.create(checkfirst=True)
    person.drop(checkfirst=True)
    person.create(checkfirst=True)
