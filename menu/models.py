"""
Models required for menu functionality.

Provides Category and Item classes.
"""

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    """Represents a category of food item."""

    name = models.CharField(max_length=50)

    def __str__(self):
        """Return category name"""
        return self.name


class Item(models.Model):
    """Represents a food item."""

    name = models.CharField(max_length=150)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name="items"
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    preparation_minutes = models.IntegerField(
        blank=True, validators=[MaxValueValidator(60)]
    )
    availability = models.BooleanField(default=True)
