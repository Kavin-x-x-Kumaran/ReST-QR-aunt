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
        fields = ["id", "occupied", "status"]


class BillSerializer(ModelSerializer):
    """Serializer for Bill objects."""

    class Meta:
        model = Bill
        fields = ["id", "table", "date"]
