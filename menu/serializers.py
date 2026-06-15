"""
Serializers for menu.

Provides serializers for Category and Item.
"""

from rest_framework.serializers import ModelSerializer

from .models import Category


class CategorySerializer(ModelSerializer):
    """Serializer for Category objects."""

    class Meta:
        model = Category
        fields = ["id", "name"]
