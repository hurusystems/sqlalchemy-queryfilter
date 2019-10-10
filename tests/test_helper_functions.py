from queryfilter import (
    QueryFilter,
    paginate_request,
    query_manager,
    get_paginate_display,
)
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


@pytest.fixture
def mock_request():
    return type("Mock", (object,), {"view_args": {}, "args": {}})


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


def test_get_valid_field(field):
    qry = QueryFilter(model=Table, valid_fields=['name', 'description'])
    assert qry.get_field(field) == 'name'


def test_paginate_request(item, mock_request):
    qs = query_manager(arguments={"name": "testing"}, model=Table)
    mock_request.args = {"display_length": 20}
    assert get_paginate_display(qs, mock_request) == 20


def test_paginate_request_unlimited(item, mock_request):
    qs = query_manager(arguments={"name": "testing"}, model=Table)
    mock_request.args = {'unlimited': 1}
    assert get_paginate_display(qs, mock_request) == 1


def test_paginate_request_code(item, mock_request):
    qs = query_manager(arguments={"name": "testing"}, model=Table)
    mock_request.view_args = {'code': 20}
    assert get_paginate_display(qs, mock_request) == 1


def test_paginate_request(mock_request):
    assert paginate_request(mock_request) == {
        'start': 1,
        'length': 20
        }


def test_paginate_request_display_length(mock_request):
    mock_request.args = {'display_start': 2, 'display_length': 20}
    assert paginate_request(mock_request) == {
        'start': 1,
        'length': 20
    }


def test_paginate_request_display_length_up(mock_request):
    mock_request.args = {'display_start': 15, 'display_length': 10}
    assert paginate_request(mock_request) == {
        'start': 2,
        'length': 10
    }
