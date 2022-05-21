from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class UtilsPageNumberPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'pagesize'
    page_size = 10
    max_page_size = 500

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page', self.page.number),
            ('pagesize', self.page.paginator.per_page),
            ('pages', self.page.paginator.num_pages),
            ('data', data)
        ]))
