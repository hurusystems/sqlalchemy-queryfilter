# encoding: utf-8
from __future__ import unicode_literals, absolute_import
from app import db


class Table(db.Model):
    __tablename__ = 'table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))
    created_date = db.Column(db.DateTime, default=db.func.now())
