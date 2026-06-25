"""
Views for menu categories and items.

Provides views for accommodating HTTP requests.
"""

from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from REST_QR_aunt.permissions import IsSuperUser
from .models import Category, Item
from .serializers import AvailabilitySerializer, CategorySerializer, ItemSerializer


class CategoryListView(generics.ListAPIView, generics.RetrieveAPIView):
    """View which permits all users to view the list of categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs.keys():
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


class CategoryAdminView(ModelViewSet):
    """
    View which permits superusers to create, retrieve, list, update, and delete Categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSuperUser]


class ItemListView(generics.ListAPIView, generics.RetrieveAPIView):
    """View which permits all users to view the list of items."""

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs.keys():
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


class ItemStaffView(generics.UpdateAPIView):
    """View which permits only staff to update availability of an Item."""

    queryset = Item.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAdminUser]


class ItemAdminView(ModelViewSet):
    """
    View which permits superusers to create, retrieve, list, update, and delete Items.
    """

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsSuperUser]
