from queryfilter import QueryFilter
from .models import Table
from .constants import SQL
import pytest


@pytest.fixture(params=QueryFilter.OPERATOR_KEYWORDS)
def operator(request):
    "Return valid operators registred in QueryFilter"
    return request.param


@pytest.fixture(params=['name[like]', 'name[coisa]', 'name'])
def field(request):
    "Return fields"
    return request.param


def test_null2none(item):
    qry = QueryFilter(model=Table)
    assert qry.null2none('null') == None


def test_find_operator(operator, item):
    qry = QueryFilter(model=Table)
    assert qry.find_operator(operator) == operator


def test_invalid_find_operator(item):
    qry = QueryFilter(model=Table)
    assert qry.find_operator('InvalidOperator') == None


def test_get_field(field):
    qry = QueryFilter(model=Table)
    assert qry.get_field(field) == 'name'
