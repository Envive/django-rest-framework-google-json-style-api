from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, 'GOOGLE_JSON_STYLE_API', {})

DEFAULTS = {
    'RENDERER_CLASS': 'rest_framework.renderers.JSONRenderer',
    'PARSER_CLASS': 'rest_framework.parsers.JSONParser',
    'CAMELIZE': True,
    'JSON_UNDERSCOREIZE': {
        'no_underscore_before_number': False,
    },
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = (
    'RENDERER_CLASS',
    'PARSER_CLASS'
)

api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)
