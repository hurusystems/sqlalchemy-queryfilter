from queryfilter import QueryFilter
from queryfilter.exceptions import InvalidField, InvalidDialectField
from .models import Table
from .constants import SQL
import pytest


def test_error_get_invalid_field(item):
    qry = QueryFilter(model=Table)
    with pytest.raises(InvalidField):
        qry.add('not_in_table', 'test')


def test_error_get_invalid_operator(item):
    qry = QueryFilter(model=Table)
    qry.OPERATOR_KEYWORDS += ['notin']
    qry.add('name[notin]', 'test')
    with pytest.raises(InvalidDialectField):
        qry.query()
