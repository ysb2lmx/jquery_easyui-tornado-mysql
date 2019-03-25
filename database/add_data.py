#encoding=utf8

import party

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
import conf


engine = create_engine(conf.DBURL, max_overflow=5)
Session = sessionmaker(bind=engine)
session = Session()

print(dir(party))
print(party)
print(type(party))
sql = party.insert().values(party_type_code='sbyang', comments='akok')
session.execute(sql)
