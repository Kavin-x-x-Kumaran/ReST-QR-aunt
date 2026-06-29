"""
Serializers for menu.

Provides serializers for Category and Item.
"""

from rest_framework.serializers import ModelSerializer

from .models import Category, Item


class CategorySerializer(ModelSerializer):
    """Serializer for Category objects."""

    class Meta:
        model = Category
        fields = ["public_id", "id", "name"]


class ItemSerializer(ModelSerializer):
    """Serializer for Item objects."""

    class Meta:
        model = Item
        fields = [
            "public_id", 
            "id",
            "category",
            "name",
            "description",
            "price",
            "preparation_minutes",
            "availability",
        ]


class ItemAvailabilitySerializer(ModelSerializer):
    """Serializer for availability field of Item objects."""

    class Meta:
        model = Item
        fields = ["public_id", "id", "availability"]
