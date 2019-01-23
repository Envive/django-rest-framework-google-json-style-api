import json
from django.urls import reverse

from example.tests import TestBase

from example.factories import AuthorFactory, BookFactory


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
                'items': [
                    {
                        'title': self.new_title,
                        'authors': [
                            {
                                'name': self.new_author.name
                            }
                        ],
                        'comments': []
                    }
                ]
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

    def test_update_without_full_keys(self):
        post_data = {
            'data': {
                'items': [
                    {
                        'title': self.new_title,
                        'authors': [
                            {
                                'name': self.new_author.name
                            }
                        ]
                    }
                ]
            }
        }

        response = self.client.put(self.detail_url, data=post_data, format='json')

        # Bad Request. Some fields are required.
        self.assertEqual(400, response.status_code)

    def test_partial_update(self):
        post_data = {
            'data': {
                'items': [
                    {
                        'title': self.new_title,
                        'authors': [
                            {
                                'name': self.new_author.name
                            }
                        ]
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
        expected['data']['items'][0]['comments'] = []

        response = self.client.patch(self.detail_url, data=post_data, format='json')

        self.assertEqual(response.json(), expected)
        self.assertEqual(response.status_code, 200)

    def test_destroy(self):
        expected = {
            'method': 'destroy',
            'params': {
                'pk': str(self.book.pk),
            },
            'data': {
                'items': []
            }
        }

        response = self.client.delete(self.detail_url, format='json')

        self.assertEqual(json.loads(response.rendered_content), expected)
        self.assertEqual(response.status_code, 204)
