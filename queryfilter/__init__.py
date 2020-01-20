# encoding: utf-8
from __future__ import unicode_literals, absolute_import
__version__ = (0, 2, 0)
__author__ = 'valdergallo@gmail.com'


def get_version():
    return '.'.join(map(str, __version__))

try:
    from .filter import (
        QueryFilter,
    )

    from .exceptions import (
        InvalidField,
        InvalidDialectField
    )

    from .helper import (
        paginate_request,
        query_manager,
        get_paginate_display,
        get_form_request,
        json_response
    )
except ModuleNotFoundError:
    pass
