from queryfilter import QueryFilter
from .models import Table
from .constants import SQL


def test_queryfilter_by_name(item):
    qry = QueryFilter(model=Table)
    qry.add('name', 'test')

    sql_expected = SQL + 'WHERE "table".name LIKE ?'

    assert qry.sql == sql_expected


def test_queryfilter_by_name_and_desciption(item):
    qry = QueryFilter(model=Table)
    qry.add('name', 'test')
    qry.add('description', 'test')

    sql_expected = SQL + \
        'WHERE "table".name LIKE ? AND "table".description LIKE ?'

    assert qry.sql == sql_expected


def test_queryfilter_by_name_or_description(item):
    qry = QueryFilter(model=Table)
    qry.add('name[orlike]', 'test')
    qry.add('description[orlike]', 'test')

    sql_expected = SQL + \
        'WHERE ("table".name LIKE ? OR "table".description LIKE ?)'

    assert qry.sql == sql_expected


def test_queryfilter_by_month(item):
    qry = QueryFilter(model=Table)
    qry.add('created_date[month]', '1')

    sql_expected = SQL + \
        "WHERE CAST(STRFTIME('%m', \"table\".created_date) AS INTEGER) = ?"

    assert qry.sql == sql_expected


def test_queryfilter_by_year(item):
    qry = QueryFilter(model=Table)
    qry.add('created_date[year]', '1')

    sql_expected = SQL + \
        "WHERE CAST(STRFTIME('%Y', \"table\".created_date) AS INTEGER) = ?"

    assert qry.sql == sql_expected


def test_queryfilter_by_lt(item):
    qry = QueryFilter(model=Table)
    qry.add('created_date[lt]', '1999-09-09')

    sql_expected = SQL + \
        "WHERE \"table\".created_date < ?"

    assert qry.sql == sql_expected


def test_queryfilter_by_lte(item):
    qry = QueryFilter(model=Table)
    qry.add('created_date[lte]', '1999-09-09')

    sql_expected = SQL + \
        "WHERE \"table\".created_date <= ?"

    assert qry.sql == sql_expected


def test_queryfilter_by_gt(item):
    qry = QueryFilter(model=Table)
    qry.add('created_date[gt]', '1999-09-09')

    sql_expected = SQL + \
        "WHERE \"table\".created_date > ?"

    assert qry.sql == sql_expected


def test_queryfilter_by_gte(item):
    qry = QueryFilter(model=Table)
    qry.add('created_date[gte]', '1999-09-09')

    sql_expected = SQL + \
        "WHERE \"table\".created_date >= ?"

    assert qry.sql == sql_expected


def test_queryfilter_by_like(item):
    qry = QueryFilter(model=Table)
    qry.add('created_date[like]', '1999-09-09')

    sql_expected = SQL + \
        "WHERE \"table\".created_date LIKE ?"

    assert qry.sql == sql_expected


def test_queryfilter_by_ilike(item):
    qry = QueryFilter(model=Table)
    qry.add('name[ilike]', '1999-09-09')

    sql_expected = SQL + \
        "WHERE lower(\"table\".name) LIKE lower(?)"

    assert qry.sql == sql_expected


def test_queryfilter_by_equal(item):
    qry = QueryFilter(model=Table)
    qry.add('name[equal]', '1999-09-09')

    sql_expected = SQL + \
        "WHERE \"table\".name = ?"

    assert qry.sql == sql_expected


def test_queryfilter_by_isnot(item):
    qry = QueryFilter(model=Table)
    qry.add('name[isnot]', None)

    sql_expected = SQL + \
        "WHERE \"table\".name IS NOT NULL"

    assert qry.sql == sql_expected


def test_queryfilter_by_is_(item):
    qry = QueryFilter(model=Table)
    qry.add('name[is_]', None)

    sql_expected = SQL + \
        "WHERE \"table\".name IS NULL"

    assert qry.sql == sql_expected


def test_queryfilter_by_is_none(item):
    qry = QueryFilter(model=Table)
    qry.add('name', 'none')

    sql_expected = SQL + \
        "WHERE \"table\".name IS NULL"

    assert qry.sql == sql_expected


def test_queryfilter_by_is_null(item):
    qry = QueryFilter(model=Table)
    qry.add('name', 'null')

    sql_expected = SQL + \
        "WHERE \"table\".name IS NULL"

    assert qry.sql == sql_expected


def test_queryfilter_by_in_(item):
    qry = QueryFilter(model=Table)
    qry.add('name[in_]', 'ab')

    sql_expected = SQL + \
        "WHERE \"table\".name IN (?, ?)"

    assert qry.sql == sql_expected


def test_queryfilter_by_notin_(item):
    qry = QueryFilter(model=Table)
    qry.add('name[notin_]', 'ab')

    sql_expected = SQL + \
        "WHERE \"table\".name NOT IN (?, ?)"

    assert qry.sql == sql_expected


def test_queryfilter_order_by_defalt_asc(item):
    qry = QueryFilter(model=Table)
    qry.add('sort_field', 'name')

    sql_expected = SQL[:-1] + \
        "ORDER BY \"table\".name ASC"

    assert qry.sql == sql_expected


def test_queryfilter_order_by_asc(item):
    qry = QueryFilter(model=Table)
    qry.add('sort_field', 'name')
    qry.add('sort_direction', 'asc')

    sql_expected = SQL[:-1] + \
        "ORDER BY \"table\".name ASC"

    assert qry.sql == sql_expected


def test_queryfilter_order_by_desc(item):
    qry = QueryFilter(model=Table)
    qry.add('sort_field', 'name')
    qry.add('sort_direction', 'desc')

    sql_expected = SQL[:-1] + \
        "ORDER BY \"table\".name DESC"

    assert qry.sql == sql_expected
