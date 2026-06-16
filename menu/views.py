"""
Views for menu categories and items.

Provides views for accommodating HTTP requests.
"""

from rest_framework import generics

from .models import Category, Item
from .permissions import IsStaff, IsSuperUser
from .serializers import AvailabilitySerializer, CategorySerializer, ItemSerializer


class CategoryListView(generics.ListCreateAPIView, generics.RetrieveAPIView):
    """View which permits all users to view the list of categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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


class ItemListView(generics.ListAPIView, generics.RetrieveAPIView):
    """View which permits all users to view the list of items."""

    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemStaffView(generics.UpdateAPIView):
    """View which permits only staff to update availability of an Item."""

    queryset = Item.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [IsStaff]


class ItemAdminView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    """
    View which permits superusers to perform the following actions to items.

    Superusers can:
    - Create a new Item.
    - Update any field of an existing Item.
    - Delete an existing Item.
    - Retrieve a particular Item.
    """

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsSuperUser]
