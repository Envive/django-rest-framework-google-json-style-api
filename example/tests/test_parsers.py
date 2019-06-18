import json
from io import BytesIO

import pytest
from django.test import TestCase
from rest_framework.exceptions import ParseError

from example.tests.utils import override_setting
from rest_framework_google_json_style_api.parsers import JSONParser


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
                'itemKey': 'value',
                'attrKey': 'attr'
            }
        }

        self.string = json.dumps(data)

    @override_setting(CAMELIZE=True)
    def test_parse_with_camelize(self):
        stream = BytesIO(self.string.encode('utf-8'))
        data = self.parser.parse(stream, None, self.parser_context)

        self.assertEqual(data['item_key'], 'value')
        self.assertEqual(data['attr_key'], 'attr')

    @override_setting(CAMELIZE=False)
    def test_parse_without_camelize(self):
        stream = BytesIO(self.string.encode('utf-8'))
        data = self.parser.parse(stream, None, self.parser_context)

        self.assertEqual(data['itemKey'], 'value')
        self.assertEqual(data['attrKey'], 'attr')

    def test_parse_error(self):
        with pytest.raises(ParseError):
            string = 'Error'
            stream = BytesIO(string.encode('utf-8'))
            self.parser.parse(stream, None, self.parser_context)

    def test_key_error(self):
        with pytest.raises(ParseError):
            string = json.dumps({'key': 'value'})
            stream = BytesIO(string.encode('utf-8'))
            self.parser.parse(stream, None, self.parser_context)
