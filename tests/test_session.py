# encoding: utf-8
from __future__ import unicode_literals, absolute_import
from .models import Table

def test_a_transaction(db_session):
    row = Table()
    row.name = 'testing'

    db_session.add(row)
    db_session.commit()

    assert row.name == 'testing'
    saved = db_session.query(Table).get(1)
    assert saved.name == 'testing'

def test_transaction_doesnt_persist(db_session):
   row = db_session.query(Table).get(1)
   assert row is None
