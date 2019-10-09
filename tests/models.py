# encoding: utf-8
from __future__ import unicode_literals, absolute_import
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


BaseModel = declarative_base()


class Table(BaseModel):
    __tablename__ = 'table'
    id = Column(Integer, primary_key=True)
    name = Column(String(80))

