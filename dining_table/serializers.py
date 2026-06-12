"""
Serializers for dining_table.

Provides serializers for dining_table.
"""

from rest_framework.serializers import ModelSerializer

from .models import Table

class TableSerializer(ModelSerializer):
    """Serializer for Table objects."""

    class Meta:
        model = Table
        fields = ["id", "occupied", "status"]
