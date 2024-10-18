from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 12

    def get_paginated_response(self, data):
        total_pages = math.ceil(self.page.paginator.count / self.page_size)

        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'total_pages': total_pages,
            'results': data
        })
