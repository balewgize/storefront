from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    """Custom pagination with 10 objects per page."""

    page_size = 10
