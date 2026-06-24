"""
Serializers for order.

Provides serializers for Order.
"""

from rest_framework.serializers import ModelSerializer

from .models import Order


class OrderSerializer(ModelSerializer):
    """Serializer for Model objects."""

    class Meta:
        model = Order
        fields = [
            "id",
            "item",
            "quantity",
            "instruction",
            "time",
            "status",
            "bill",
            "deleted_at",
        ]


class OrderCustomerSerializer(ModelSerializer):
    """Serializer for PATCH method, allowing customers to edit only instructions and quantity."""

    class Meta:
        model = Order
        fields = ["id", "quantity", "instruction", "deleted_at"]
