import json

import pytest
from django.urls import reverse

from example.factories import AuthorFactory, BookFactory
from example.tests import TestBase
from example.tests.utils import override_setting


class TestModelViewSet(TestBase):
    def setUp(self):
        self.author = AuthorFactory()
        self.new_author = AuthorFactory()
        self.book = BookFactory(authors=(self.author,))
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})
        self.new_title = 'New title'

    def test_update(self):
        post_data = {
            'data': {
                'title': self.new_title,
                'authors': [
                    {
                        'name': self.new_author.name,
                        'authorType': {
                            'name': self.new_author.author_type.name,
                        }
                    }
                ],
                'comments': []
            }
        }

        expected = {
            'method': 'update',
            'params': {
                'pk': str(self.book.pk),
            },
            'data': post_data['data']
        }

        response = self.client.put(self.detail_url, data=post_data, format='json')

        self.assertEqual(response.json(), expected)
        self.assertEqual(response.status_code, 200)

    @override_setting(CAMELIZE=False)
    def test_update_without_full_keys(self):
        post_data = {
            'data': {
                'authors': [
                    {
                        'name': self.new_author.name
                    }
                ]
            }
        }
        expected = {
            'error': {
                'code': 400,
                'message': 'This field is required.',
                'errors': [
                    {
                        'domain': 'title',
                        'reason': 'required',
                        'message': 'This field is required.'
                    },
                    {
                        'domain': 'authors.author_type',
                        'reason': 'required',
                        'message': 'This field is required.'
                    },
                    {
                        'domain': 'comments',
                        'reason': 'required',
                        'message': 'This field is required.'
                    },
                ]
            }
        }

        response = self.client.put(self.detail_url, data=post_data, format='json')

        # Bad Request. Some fields are required.
        self.assertEqual(400, response.status_code)
        self.assertEqual(response.json(), expected)

    def test_partial_update(self):
        post_data = {
            'data': {
                'title': self.new_title,
                'authors': [
                    {
                        'name': self.new_author.name,
                        'authorType': {
                            'name': self.new_author.author_type.name,
                        }
                    }
                ]
            }
        }
        expected = {
            'method': 'partial_update',
            'params': {
                'pk': str(self.book.pk),
            },
            'data': post_data['data']
        }
        expected['data']['comments'] = []

        response = self.client.patch(self.detail_url, data=post_data, format='json')

        self.assertEqual(response.json(), expected)
        self.assertEqual(response.status_code, 200)

    def test_destroy(self):
        expected = {
            'method': 'destroy',
            'params': {
                'pk': str(self.book.pk),
            },
            'data': {}
        }

        response = self.client.delete(self.detail_url, format='json')

        self.assertEqual(json.loads(response.rendered_content), expected)
        self.assertEqual(response.status_code, 204)

    def test_parser_error(self):
        post_data = {
            'key': 'value',
        }
        expected = {
            'error': {
                'code': 400,
                'message': "JSON parse error - 'data'",
                'errors': [
                    {
                        'domain': 'global',
                        'reason': 'parse_error',
                        'message': "JSON parse error - 'data'"
                    }
                ]
            }
        }

        response = self.client.put(self.detail_url, data=post_data, format='json')

        self.assertEqual(response.json(), expected)
        self.assertEqual(response.status_code, 400)

    def test_no_status_code(self):
        with pytest.raises(AttributeError):
            self.client.get('/no_status', format='json')
