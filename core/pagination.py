from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'count'
    max_page_size = 100
    page_query_param = 'page'
