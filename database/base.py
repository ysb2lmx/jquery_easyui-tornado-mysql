#encoding
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
import database.conf as conf

#engine = create_engine(conf.DBURL, max_overflow=5, echo=True)
engine = create_engine(conf.DBURL, max_overflow=5)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()
