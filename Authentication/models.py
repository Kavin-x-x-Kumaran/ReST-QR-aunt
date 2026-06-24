"""
Models for authentication.

Provides User class as a child of AbstractUser with optional attribute table_id
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

from dining_table.models import Table
from REST_QR_aunt.models import Base


class User(Base, AbstractUser):
    """
    Represents User in the system.

    Users with is_staff=False represent dining tables and have a corresponding table_id
    """

    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        """Return a human-readable identifier."""
        return self.username

    class Meta(AbstractUser.Meta):
        pass
