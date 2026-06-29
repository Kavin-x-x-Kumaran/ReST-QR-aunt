"""
Serializers for order.

Provides serializers for Order.
"""

from django.utils import timezone
from rest_framework.serializers import ModelSerializer

from .models import Order


class OrderSerializer(ModelSerializer):
    """Serializer for Order objects."""

    class Meta:
        model = Order
        fields = [
            "public_id",
            "id",
            "item",
            "quantity",
            "instruction",
            "time",
            "status",
            "bill",
        ]


class OrderCustomerSerializer(ModelSerializer):
    """
    Serializer for Order objects, allowing customers to edit only instructions and quantity.

    Field "time" updates automatically for each update.
    """

    class Meta(OrderSerializer.Meta):
        read_only_fields = ["public_id", "id", "item", "time", "status", "bill"]

    def update(self, instance, validated_data):
        validated_data["time"] = timezone.now()
        return super().update(instance, validated_data)


class OrderKitchenSerializer(ModelSerializer):
    """Serializer for Order objects, allowing kitchen staff to edit only status."""

    class Meta(OrderSerializer.Meta):
        read_only_fields = [
            "public_id",
            "id",
            "item",
            "quantity",
            "instruction",
            "time",
            "bill",
        ]
