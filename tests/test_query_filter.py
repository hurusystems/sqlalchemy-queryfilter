from queryfilter import QueryFilter
from .models import Table

SQL = 'SELECT "table".id AS table_id, "table".name AS table_name, "table".description AS table_description, "table".created_date AS table_created_date \nFROM "table" \n'


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
