# encoding: utf-8
from __future__ import unicode_literals, absolute_import

import re
from sqlalchemy import and_, or_, asc, desc, extract
from .exceptions import InvalidDialectField, InvalidField
import dateutil.parser as parser


class QueryFilter(object):
    FILTER_MARK = r'\[(.*?)\]'
    OPERATOR_KEYWORDS = ['notin_', 'lte', 'gte', 'like', 'ilike', 'gt',  'lt', 'month', 'year',
                          'equal', 'is_', 'isnot', 'in_', 'any']
    LINKS_KEYWORDS = ['or', 'and']
    DEFAULT_LINK = 'and'
    DEFAULT_OPERATOR = 'like'
    ORDER_BY = []
    ORDER_BY_KEYWORD = 'sort_field'
    ORDER_BY_SORT_DIRECTION = 'sort_direction'
    MODEL = None
    FIELDS = None

    def __init__(self, model, valid_fields=None):
        if not valid_fields:
            self.FIELDS = model.__table__.columns.keys()
        else:
            self.FIELDS = valid_fields

        # accept order_by in fields
        self.FIELDS += [self.ORDER_BY_KEYWORD, self.ORDER_BY_SORT_DIRECTION]
        self.ORDER_BY = []  # default order_by
        self.SORT_DIRECTION = []  # default SORT_DIRECTION
        self.model = model
        self.regex_link = '|'.join(self.LINKS_KEYWORDS)
        self.queries = []

    def null2none(self, value):
        """SQL translate values"""
        if value == 'null':
            return None
        return value

    def find_operator(self, value):
        try:
            i = self.OPERATOR_KEYWORDS.index(value)
            return self.OPERATOR_KEYWORDS[i]
        except ValueError:
            return

    def get_field(self, table_field):
        """remove query from table field name"""
        return table_field.split('[')[0]

    def parse_field(self, table_field):
        search_text = re.findall(self.FILTER_MARK, table_field)

        table_field = self.get_field(table_field)

        if not search_text:
            return {'op': self.DEFAULT_OPERATOR, 'link': self.DEFAULT_LINK, 'field': table_field}

        search_text = search_text[0]

        _link = re.findall(self.regex_link, search_text) or [self.DEFAULT_LINK]
        _filter = self.find_operator(search_text) or self.DEFAULT_OPERATOR

        return {'op': _filter, 'link': _link[0], 'field': table_field}

    def add(self, table_field, value):
        if table_field == self.ORDER_BY_KEYWORD:
            model_field = hasattr(self.model, value)
            if not model_field:
                raise InvalidField(
                    'Invalid table field (%s) in order_by' % value)
            self.ORDER_BY.append(value)
            # save order by and dont chanche queries
            return

        if table_field == self.ORDER_BY_SORT_DIRECTION:
            if value == 'desc':
                self.SORT_DIRECTION.append(desc)
            else:
                self.SORT_DIRECTION.append(asc)
            return

        qry = self.parse_field(table_field)
        model_field = getattr(self.model, qry['field'], None)

        if not model_field:
            raise InvalidField('Invalid table field (%s)' % qry['field'])

        qry['value'] = value
        qry['field'] = model_field

        # ignore query without values
        if qry['value'] or (not qry['value'] and qry['op'] != self.DEFAULT_OPERATOR):
            qry['value'] = self.null2none(value)
            self.queries.append(qry)

    def get_order_by(self):
        if not self.SORT_DIRECTION and not self.ORDER_BY:
            return []

        if not self.SORT_DIRECTION and self.ORDER_BY:
            self.SORT_DIRECTION.append(asc)

        return [i[0](i[1]) for i in zip(self.SORT_DIRECTION, self.ORDER_BY)]

    @property
    def query(self):
        and_query = []
        or_query = []
        invalid_operators = ['gt', 'gte', 'lt', 'lte', 'equal']

        for item in self.queries:
            # print('DEBUG ITEM ', item)

            if (not item['value'] or item['value'].lower() == 'none' or item['value'].lower() == 'null') and item['op'] in ['ilike', 'like']:
                item['op'] = 'is_'
                item['value'] = None
            elif item['op'] in ['ilike', 'like']:
                item['value'] = '%{v}%'.format(v=item['value'])

            if item['op'] not in invalid_operators and hasattr(item['field'], item['op']):
                # get default operator from sqlalchemy (in_, is_)
                func_operator = getattr(item['field'], item['op'])
            elif item['op'] == 'gt':
                def func_operator(x): return item['field'] > x
            elif item['op'] == 'gte':
                def func_operator(x): return item['field'] >= x
            elif item['op'] == 'lt':
                def func_operator(x): return item['field'] < x
            elif item['op'] == 'lte':
                def func_operator(x): return item['field'] <= x
            elif item['op'] == 'equal':
                def func_operator(x): return item['field'] == x
            elif item['op'] == 'month':
                def func_operator(x): return extract('month', item['field']) == x
            elif item['op'] == 'year':
                def func_operator(x): return extract(
                    'year', item['field']) == x
            else:
                func_operator = None

            if not func_operator:
                raise InvalidDialectField(
                    "Invalid SqlAlchemy Dialects operation: (%s) for field (%s)" % (item['op'], item['field']))

            if item['link'] == 'and':
                and_query.append(func_operator(item['value']))
            if item['link'] == 'or':
                or_query.append(func_operator(item['value']))

        qr = self.model.query.filter(
            and_(*and_query), or_(*or_query)).order_by(*self.get_order_by())

        return qr

    @property
    def sql(self):
        query_str = self.query
        return str(query_str)

