"""
Models required for menu functionality.

Provides Category and Item classes.
"""

from django.db import models


class Category(models.Model):
    """Represents a category of food item."""

    name = models.CharField(max_length=50)

    def __str__(self):
        """Return category name"""
        return self.name
