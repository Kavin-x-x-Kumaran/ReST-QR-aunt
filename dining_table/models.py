"""
Models representing customers seated at dining tables.

Provides Table and Bill classes.
"""

from django.db import models
from django.db.models import Q

from REST_QR_aunt.models import SoftDeleteModel


class Table(SoftDeleteModel):
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
        if not self.is_deleted:
            return f"Table no. {self.pk}"
        return super().__str__()


class Bill(SoftDeleteModel):
    """Represents a bill generated in a visit."""

    table = models.ForeignKey(Table, on_delete=models.DO_NOTHING, related_name="bills")
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a human-readable identifier."""
        if not self.is_deleted:
            return f"Bill no. {self.pk} from {self.date}"
        return super().__str__()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["table"],
                condition=Q(active=True),
                name="unique_active_bill_per_table",
            )
        ]
