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

Google JSON style Guide shows a response to look like the following:

```json
{
    "data": {
        "items":[
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
    }
}
```
