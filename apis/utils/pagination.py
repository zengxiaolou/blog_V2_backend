from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'size'
