# Queryfilter

Queryfilter is a small ORM to read arguments URL and make SQL
query

### TO Install

> pip install git+https://git.in.hurusystems.com/huru/huru_sqlalchemy_queryfilter.git#egg=queryfilter

### HOW TO USE

```python
from queryfilter import query_manager, get_paginate_display

so_schema = MyModelSchema(many=True)


def view(request):
    qs = query_manager(arguments=request.args, model=MyModel)

    result = so_schema.dump(orders)

    # default content for datatables js
    content = {
        'filtered': get_paginate_display(qs, request),
        'total': qs.count(),
        'results': result
    }
    return jsonify(content)
```
### Filters

By default queryfilter will check if ModelField has filter implemented by SQLAlchemy,
if not they will search in commum filter

(available filters)
- **notin_**: default filter used with SQLAlchemy
- **lte**: Lower than Equal
- **gte**: Greater than Equal
- **like**: default filter used with SQLAlchemy
- **ilike**: default filter used with SQLAlchemy
- **gt**: Greater than
- **lt**: Lower than
- **month**: Filter (date, datetime, timestamp) by month
- **year**: Filter (date, datetime, timestamp) by year
- **equal**: default filter used with SQLAlchemy
- **is_**: default filter used with SQLAlchemy
- **isnot**: default filter used with SQLAlchemy
- **in_**: default filter used with SQLAlchemy
- **any**: default filter used with SQLAlchemy

##### All possible filter

-> https://docs.sqlalchemy.org/en/13/orm/internals.html?highlight=notin_#sqlalchemy.orm.attributes.QueryableAttribute

### Coverage

![](./docs/coverage.png)
