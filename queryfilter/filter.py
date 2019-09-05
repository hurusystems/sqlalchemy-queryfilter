# -*- coding: utf-8 -*-
from __future__ import absolute_import

import re
from sqlalchemy import and_, or_, asc, desc
from .exceptions import InvalidDialectField, InvalidField
import dateutil.parser as parser


class QueryFilter(object):
    __version__ = "0.0.1"

    FILTER_MARK = r'\[(.*?)\]'
    OPERATOR_KEYWORDS = ['like', 'ilike', 'gt', 'gte', 'lt', 'lte', 'equal', 'is_', 'isnot', 'in_', 'notin','any']
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
        self.regex_link = "^(" + '|'.join(self.LINKS_KEYWORDS) + ")"
        self.regex_filter = "(" + '|'.join(self.OPERATOR_KEYWORDS) + ")$"
        self.queries = []

    def get_version(self):
        return self.__version__

    def null2none(self, value):
        """SQL translate values"""
        if value == 'null':
            return None
        return value

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
        _filter = re.findall(
            self.regex_filter, search_text) or [self.DEFAULT_OPERATOR]
        return {'op': _filter[0], 'link': _link[0], 'field': table_field}

    def add(self, table_field, value):
        if table_field == self.ORDER_BY_KEYWORD:
            model_field = hasattr(self.model, value)
            if not model_field:
                raise InvalidField('Invalid table field (%s) in order_by' % value)
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

        qry['value'] = self.null2none(value)
        qry['field'] = model_field

        # ignore query without values
        if qry['value'] or (not qry['value'] and qry['op'] != self.DEFAULT_OPERATOR):
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
            if not item['value'] and item['op'] in ['ilike', 'like']:
                item['op'] = 'is_'
                item['value'] = None
            elif item['op'] in ['ilike', 'like']:
                item['value'] += '%'

            if item['op'] not in invalid_operators and hasattr(item['field'], item['op']):
                func_operator = getattr(item['field'], item['op'])
            elif item['op'] == 'gt':
                func_operator = lambda x: item['field'] > x
            elif item['op'] == 'gte':
                func_operator = lambda x: item['field'] >= x
            elif item['op'] == 'lt':
                func_operator = lambda x: item['field'] < x
            elif item['op'] == 'lte':
                func_operator = lambda x: item['field'] <= x
            elif item['op'] == 'equal':
                func_operator = lambda x: item['field'] == x
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


def paginate_request(request):
    display_length = int(request.args.get('display_length', 20))
    display_start = (int(request.args.get(
        'display_start', 0)) // display_length) + 1

    return {'start': display_start, 'length': display_length}



def query_manager(arguments, model=None):
    # TODO: use JSON API to search elements
    # https://flask-restless.readthedocs.io/en/latest/filtering.html
    # query = QueryStringManager(eval(json_filter), ServiceOrder)
    # qs = compute_schema(ServiceOrderSchema, query, dict(), query.include)
    qry = QueryFilter(model=model)

    if arguments:
        for table_field, value in arguments.items():
            if qry.get_field(table_field) not in qry.FIELDS:
                continue
            qry.add(table_field, value)

    return qry.query


def get_paginate_display(qs, request):
    "Return the total filtered"
    code = request.view_args.get('code')
    unlimited = request.args.get('unlimited')
    display_length = int(request.args.get('display_length', 20))

    if unlimited:
        return qs.count()
    elif code:
        return 1
    return display_length
