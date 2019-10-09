# encoding: utf-8
from __future__ import unicode_literals, absolute_import
__version__ = (0, 1, 0)
__author__ = 'valdergallo@gmail.com'


def get_version():
    return '.'.join(map(str, __version__))


from .filter import (
    QueryFilter,
    paginate_request,
    query_manager,
    get_paginate_display
)

from .exceptions import (
    InvalidField,
    InvalidDialectField
)
