"""
Models required for order functionality.

Provides Order class.
"""

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from dining_table.models import Bill
from menu.models import Item


class Order(models.Model):
    """Represents an order given by any customer."""

    class Status(models.TextChoices):
        """Defines choices for the status attribute."""
        ORDERING = "O", "Ordering"
        WAITING = "W", "Waiting"
        DELIVERED = "D", "Delivered"

    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, related_name="orders")
    quantity = models.IntegerField(
        validators=[MaxValueValidator(20), MinValueValidator(1)], default=1
    )
    instruction = models.TextField(blank=True)
    time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=Status.choices, default="O")
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="orders")
