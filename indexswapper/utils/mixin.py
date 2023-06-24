from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PaginationConfig(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data,
        })


class CourseIndexQueryParamsMixin:
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        'code': ['icontains'],
        'name': ['icontains'],
        'index': ['exact'],
        'pending_count': ['lt', 'gt'],
    }
    ordering_fields = ['code', 'name', 'index', 'pending_count']
    pagination_class = PaginationConfig
    # TODO - consider implement full-text search indexing too (need PostgreSQL)


class SwapRequestQueryParamsMixin:
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'status': ['exact'],
    }
