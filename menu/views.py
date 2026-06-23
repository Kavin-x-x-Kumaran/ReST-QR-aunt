"""
Views for menu categories and items.

Provides views for accommodating HTTP requests.
"""

from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import Category, Item
from .permissions import IsSuperUser
from .serializers import AvailabilitySerializer, CategorySerializer, ItemSerializer


class CategoryListView(generics.ListAPIView, generics.RetrieveAPIView):
    """View which permits all users to view the list of categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs.keys():
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


class CategoryAdminView(
    generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView
):
    """
    View which permits superusers to perform the following actions to categories.

    Superusers can:
    - Create a new Category.
    - Update an existing Category.
    - Delete an existing Category.
    - Retrieve a particular Category.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSuperUser]

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs.keys():
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


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


class ItemAdminView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    """
    View which permits superusers to perform the following actions to items.

    Superusers can:
    - Retrieve all Items.
    - Create a new Item.
    - Update any field of an existing Item.
    - Delete an existing Item.
    - Retrieve a particular Item.
    """

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsSuperUser]

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs.keys():
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
