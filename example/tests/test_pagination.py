from django.contrib.auth import get_user_model
from django.urls import reverse

from example.tests import TestBase
from example.views import UserViewSet

from rest_framework_google_json_style_api.pagination import (
    GoogleJsonStylePageNumberPagination
)

User = get_user_model()


class ModelViewSetTests(TestBase):

    list_url = reverse('user-list')

    def setUp(self):
        super(ModelViewSetTests, self).setUp()
        self.detail_url = reverse('user-detail', kwargs={'pk': self.scott.pk})

    def test_list_result(self):
        response = self.client.get(self.list_url)

        user_all = User.objects.all()
        expected = {
            'method': 'list',
            'params': {},
            'data': {
                'items': [
                    {
                        'firstName': user.first_name,
                        'lastName': user.last_name,
                        'email': user.email
                    } for user in user_all
                ]
            }
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_retrieve_result(self):
        response = self.client.get(self.detail_url)

        user = User.objects.get(pk=self.scott.pk)
        expected = {
            'method': 'retrieve',
            'params': {
                'pk': str(self.scott.pk)
            },
            'data': {
                'firstName': user.first_name,
                'lastName': user.last_name,
                'email': user.email
            }
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_pagination_one_result(self):
        UserViewSet.pagination_class = GoogleJsonStylePageNumberPagination
        response = self.client.get(self.list_url, {'page_size': 1})

        user = User.objects.all().order_by('pk')[0]
        expected = {
            'method': 'list',
            'params': {
                'pageSize': '1',
            },
            'data': {
                'currentItemCount': 1,
                'itemsPerPage': 1,
                'totalItems': 2,
                'pageIndex': 1,
                'totalPages': 2,
                'nextLink': "http://testserver/users?page=2&page_size=1",
                'previousLink': None,
                'items': [
                    {
                        'firstName': user.first_name,
                        'lastName': user.last_name,
                        'email': user.email
                    }
                ]
            }
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_pagination_two_result(self):
        class ExamplePagination(GoogleJsonStylePageNumberPagination):
            page_size_query_param = 'page_size'

        UserViewSet.pagination_class = ExamplePagination
        response = self.client.get(self.list_url, {'page_size': 2})

        user_all = User.objects.all().order_by('pk')
        expected = {
            'method': 'list',
            'params': {
                'pageSize': '2',
            },
            'data': {
                'currentItemCount': 2,
                'itemsPerPage': 2,
                'totalItems': 2,
                'pageIndex': 1,
                'totalPages': 1,
                'nextLink': None,
                'previousLink': None,
                'items': [
                    {
                        'firstName': user.first_name,
                        'lastName': user.last_name,
                        'email': user.email
                    } for user in user_all
                ]
            }
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)
