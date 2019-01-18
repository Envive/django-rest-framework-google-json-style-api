import json

from django.conf import settings

from django_rest_framework_camel_case.util import underscoreize

from rest_framework.parsers import ParseError, six

from rest_framework_google_json_style_api.settings import api_settings


class JSONParser(api_settings.PARSER_CLASS):
    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)

        try:
            data = json.loads(stream.read().decode(encoding))
            if api_settings.CAMELIZE:
                data = underscoreize(
                    data['data']['items'][0] if data['data']['items'] else {},
                    **api_settings.JSON_UNDERSCOREIZE
                )
            return data
        except ValueError as exc:
            raise ParseError('JSON parse error - %s' % six.text_type(exc))
