"""
Pagination for the project.

Provides DefaultPageNumberPagination which defines the PageNumberPaginator's page size.
"""

from rest_framework.pagination import PageNumberPagination

from .settings import PAGINATION_PAGE_SIZE


class DefaultPageNumberPagination(PageNumberPagination):
    """Inherits PageNumberPagination and redefines page_size for customization."""
    
    page_size = PAGINATION_PAGE_SIZE