"""
Views for menu categories and items.

Provides views for accommodating HTTP requests.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Category
from .permissions import IsSuperUser
from .serializers import CategorySerializer


class CategoryListView(generics.ListAPIView):
    """View which permits all users to view the list of categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class CategoryAdminView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    """View which permits superusers to perform all actions to categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSuperUser]
