# Django REST Framework Google JSON Style API

## Installation

At the command line:

```
$ git clone https://github.com/Envive/django-rest-framework-google-json-style-api.git
$ cd django-rest-framework-google-json-style-api
$ python setup.py install
```

Add the render and parser to your django settings file.

```python
# ...
REST_FRAMEWORK = {
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

##
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
        "items":[
            {
                "id": 1,
                "username": "scott",
                "fullName": "Scott Chang"
            }
        ]
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

By default, the package uses the first case. To use the second case, specify it in your django settings file.

```python
GOOGLE_JSON_STYLE_API = {
    # ...
    'JSON_UNDERSCOREIZE': {
        'no_underscore_before_number': True,
    },
    # ...
}
```
