"""
Views for menu categories and items.

Provides views for accommodating HTTP requests.
"""

from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from REST_QR_aunt.permissions import IsSuperUser
from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer, ItemAvailabilitySerializer


class CategoryViewSet(ModelViewSet):
    """
    Viewset for accessing Categories.

    Grants heightened access to superusers.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "public_id"

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = self.permission_classes
        else:
            permission_classes = [IsSuperUser]
        return [permission() for permission in permission_classes]


class ItemViewSet(ModelViewSet):
    """
    Viewset for accessing Items.

    Grants heightened access to superusers.
    """

    queryset = Item.objects.all()
    lookup_field = "public_id"

    def get_serializer_class(self, *args, **kwargs):
        """
        Return the class to use for the serializer depending on the incoming request.
        """
        if self.action == "partial_update" and not self.request.user.is_superuser:
            return ItemAvailabilitySerializer
        return ItemSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires
        depending on the incoming request.
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = self.permission_classes
        if self.action == "partial_update":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsSuperUser]
        return [permission() for permission in permission_classes]
