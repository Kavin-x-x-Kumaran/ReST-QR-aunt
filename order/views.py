"""
Views for orders.

Provides views for accommodating HTTP requests.
"""

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from REST_QR_aunt.pagination import DefaultPageNumberPagination
from .models import Order
from .serializers import (
    OrderSerializer,
    OrderKitchenSerializer,
    OrderCustomerSerializer,
)


class OrderViewSet(ModelViewSet):
    """Viewset for managing orders for Admin and kitchen staff."""

    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]
    pagination_class = DefaultPageNumberPagination
    lookup_field = "public_id"

    def get_serializer_class(self, *args, **kwargs):
        """
        Return the class to use for the serializer depending on the incoming request.
        """
        if self.request.user.is_superuser:
            return OrderSerializer
        return OrderKitchenSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.get("status")
        if status is not none:
            queryset = queryset.filter(status=status)
        return queryset


class OrderTableViewSet(ModelViewSet):
    """Viewset for managing orders for customers."""

    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCustomerSerializer
    lookup_field = "public_id"
