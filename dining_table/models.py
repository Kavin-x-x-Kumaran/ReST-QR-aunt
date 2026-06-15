"""
Models available to customers seated at dining tables.

Provides Table and Bill classes.
"""

from django.db import models


class Table(models.Model):
    """Represents a dining table which seats customers."""

    class Status(models.TextChoices):
        ORDERING = "O", "Ordering"
        WAITING = "W", "Waiting"
        DELIVERED = "D", "Delivered"
        PAID = "P", "Paid"

    occupied = models.BooleanField(default=False)
    status = models.CharField(
        max_length=1, choices=Status.choices, null=True, blank=True
    )

    def __str__(self):
        """Return a human-readable identifier."""
        return f"Table no. {self.pk}"


class Bill(models.Model):
    """Represents a bill generated in a visit."""

    table = models.ForeignKey(Table, on_delete=models.DO_NOTHING, related_name="bills")
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a human-readable identifier."""
        return f"Bill no. {self.pk} from {self.date}"
