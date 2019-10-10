# encoding: utf-8
from __future__ import unicode_literals, absolute_import
from .models import Table
import pytest


@pytest.fixture
def item(db_session):
    row = Table()
    row.name = 'testing'
    row.description = 'testing'

    db_session.add(row)
    db_session.commit()

    return row

