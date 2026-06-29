"""
Views for orders.

Provides views for accommodating HTTP requests.
"""

from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from REST_QR_aunt.pagination import DefaultPageNumberPagination
from REST_QR_aunt.permissions import IsStaffUser
from .models import Order
from .serializers import (
    OrderSerializer,
    OrderKitchenSerializer,
    OrderCustomerSerializer,
)


class OrderViewSet(ModelViewSet):
    """Viewset for managing orders for Admin and kitchen staff."""

    queryset = Order.objects.all()
    permission_classes = [IsStaffUser]
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
        status = self.request.query_params.get("status")
        if status is not None:
            queryset = queryset.filter(status=status)
        return queryset
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("You cannot create a new order.")
        return super().create(request, *args, **kwargs)


class OrderTableViewSet(ModelViewSet):
    """Viewset for managing orders for customers."""

    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCustomerSerializer
    lookup_field = "public_id"

    def create(self, request, *args, **kwargs):
        if request.user.is_staff and not request.user.is_superuser:
            raise PermissionDenied("You cannot create a new order.")
        return super().create(request, *args, **kwargs)
