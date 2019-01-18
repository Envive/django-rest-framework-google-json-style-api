from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response


class GoogleJsonStylePageNumberPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    page_size = 10
    max_page_size = 100

    def get_paginated_response(self, data):

        return Response(
            OrderedDict([
                ('current_item_count', len(data)),
                ('items_per_page', self.page.paginator.per_page),
                ('total_items', self.page.paginator.count),
                ('page_index', self.page.number),
                ('total_pages', self.page.paginator.num_pages),
                ('next_link', self.get_next_link()),
                ('previous_link', self.get_previous_link()),
                ('results', data),
            ])
        )
