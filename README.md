# Django REST Framework Google JSON Style API

[![Build Status](https://travis-ci.com/Envive/django-rest-framework-google-json-style-api.svg?branch=master)](https://travis-ci.com/Envive/django-rest-framework-google-json-style-api) 
[![codecov.io](https://codecov.io/github/envive/django-rest-framework-google-json-style-api/coverage.svg?branch=master)](https://codecov.io/github/envive/django-rest-framework-google-json-style-api)
[![PyPI version](https://badge.fury.io/py/django-rest-framework-google-json-style-api.svg)](https://badge.fury.io/py/django-rest-framework-google-json-style-api)

## Format specification
- https://google.github.io/styleguide/jsoncstyleguide.xml

## Installation

At the command line:

```
$ pip install django-rest-framework-google-json-style-api
```

Add the render and parser to your django settings file.

```python
# ...
REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework_google_json_style_api.pagination.GoogleJsonStylePageNumberPagination',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_google_json_style_api.renderers.JSONRenderer',
        # Any other renders
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_google_json_style_api.parsers.JSONParser',
        # Any other parsers
    ),
}
# ...
```

## Goals
By default, Django REST Framework will produce a response like:

```json
{
    "id": 1,
    "username": "scott",
    "full_name": "Scott Chang"
}
```

and

```json
[
    {
        "id": 1,
        "username": "scott",
        "full_name": "Scott Chang"
    },
    {
        "id": 2,
        "username": "pocheng",
        "full_name": "Pocheng Huang"
    }
]
```

Google JSON Style Guide shows a response to look like the following:

```json
{
    "data": {
        "id": 1,
        "username": "scott",
        "fullName": "Scott Chang"
    }
}
```

and

```json
{
    "data": {
        "items":[
            {
                "id": 1,
                "username": "scott",
                "fullName": "Scott Chang"
            },
            {
                "id": 2,
                "username": "pocheng",
                "fullName": "Pocheng Huang"
            }
        ]
    }
}
```

Google JSON Style Guide uses camel case for field names. So, by default the package uses camel case.
If you want to use underscores, you must specify it in your django settings file.

```python
GOOGLE_JSON_STYLE_API = {
    # ...
    'CAMELIZE': False
    # ...
}
```

## Pagination
```json
{
    "method": "list",
    "params": {
        "page": "1",
        "pageSize": "2"
    },
    "data": {
        "currentItemCount": 2,
        "itemsPerPage": 2,
        "totalItems": 200,
        "pageIndex": 1,
        "totalPages": 100,
        "nextLink": "http://example.com/api/v1/?page=2&page_size=2",
        "previousLink": null,
        "items": [
            {
                "id": 1,
                "username": "scott",
                "fullName": "Scott Chang"
            },
            {
                "id": 2,
                "username": "pocheng",
                "fullName": "Pocheng Huang"
            }
        ]
    }
}
```

## Attach meta to data object

#### Example
Let's add the count of items in the data object.

```python
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    # ...

    def list(self, request, *args, **kwargs):
        response = super(AuthorViewSet, self).list(request, *args, **kwargs)
        response.data = {
            'meta': {
                # Add meta data in here
                'num_items': self.queryset.count(),
            },
            # Keep original data in results
            'results': response.data
        }
```

#### Response

```json
{
    "data": {
        "numItems": 2,
        "items":[
            {
                "id": 1,
                "username": "scott",
                "fullName": "Scott Chang"
            },
            {
                "id": 2,
                "username": "pocheng",
                "fullName": "Pocheng Huang"
            }
        ]
    }
}
```


## Underscoreize Options
There are two conventions of snake case.

### Case 1 (default)
```
v2Counter -> v_2_counter
fooBar2 -> foo_bar_2
```

### Case 2
```
v2Counter -> v2_counter
fooBar2 -> foo_bar2
```

By default, the package uses the first case. To use the second case, specify it in your django settings file. The setting only works when you use camel case(default).

```python
GOOGLE_JSON_STYLE_API = {
    # ...
    'JSON_UNDERSCOREIZE': {
        'no_underscore_before_number': True,
    },
    # ...
}
```
