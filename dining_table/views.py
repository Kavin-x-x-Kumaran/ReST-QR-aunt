"""
Views for dining tables.

Provides views for accommodating HTTP requests.
"""

from rest_framework.viewsets import ModelViewSet

from .models import Table
from .permissions import IsAllowedAccess
from .serializers import TableSerializer


class TableView(ModelViewSet):
    """
    Viewset for managing users.

    Restricts access to superusers.
    """
    
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAllowedAccess]
