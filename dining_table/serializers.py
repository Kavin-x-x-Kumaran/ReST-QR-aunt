"""
Serializers for dining_table.

Provides serializers for Bill and Table.
"""

from rest_framework.serializers import ModelSerializer

from .models import Bill, Table


class TableSerializer(ModelSerializer):
    """Serializer for Table objects."""

    class Meta:
        model = Table
        fields = ["public_id", "id", "occupied", "status"]
        read_only_fields = ["public_id", "id"]


class BillSerializer(ModelSerializer):
    """Serializer for Bill objects."""

    class Meta:
        model = Bill
        fields = ["public_id", "id", "table", "active", "date"]
        read_only_fields = ["public_id", "id"]
