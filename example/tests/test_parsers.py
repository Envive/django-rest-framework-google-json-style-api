import json
from io import BytesIO

from django.test import TestCase

from rest_framework_google_json_style_api.parsers import JSONParser
from rest_framework_google_json_style_api.settings import api_settings


class TestJSONParser(TestCase):

    def setUp(self):
        class MockRequest(object):

            def __init__(self):
                self.method = 'GET'

        request = MockRequest()
        self.parser_context = {'request': request, 'kwargs': {}, 'view': 'UserViewSet'}
        self.parser = JSONParser()

        data = {
            'method': 'create',
            'params': {},
            'data': {
                'items': [
                    {
                        'itemKey': 'value',
                        'attrKey': 'attr'
                    }
                ]
            }
        }

        self.string = json.dumps(data)

    def test_parse_with_camelize(self):
        api_settings.CAMELIZE = True
        stream = BytesIO(self.string.encode('utf-8'))
        data = self.parser.parse(stream, None, self.parser_context)

        self.assertEqual(data['item_key'], 'value')
        self.assertEqual(data['attr_key'], 'attr')

    def test_parse_without_camelize(self):
        api_settings.CAMELIZE = False
        stream = BytesIO(self.string.encode('utf-8'))
        data = self.parser.parse(stream, None, self.parser_context)

        self.assertEqual(data['itemKey'], 'value')
        self.assertEqual(data['attrKey'], 'attr')
