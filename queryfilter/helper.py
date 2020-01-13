from .filter import QueryFilter


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


def get_form_request(request):
    "Get form data from JSON or Body"
    if request.is_json:
        post_parser = request.json
    else:
        post_parser = dict(request.form)
    return post_parser
