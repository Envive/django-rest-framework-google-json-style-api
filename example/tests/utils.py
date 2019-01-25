from functools import wraps

from rest_framework_google_json_style_api.settings import api_settings


class override_setting(object):
    def __init__(self, *args, **kwargs):
        self.options = kwargs
        self.original = dict()

    def enable(self):
        for key, value in self.options.items():
            self.original[key] = getattr(api_settings, key, None)
            setattr(api_settings, key, value)

    def disable(self):
        for key, value in self.original.items():
            if value:
                setattr(api_settings, key, value)

    def __enter__(self):
        self.enable()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disable()

    def decorate_callable(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return inner

    def __call__(self, func):
        return self.decorate_callable(func)
