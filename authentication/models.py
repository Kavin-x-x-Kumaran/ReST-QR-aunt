"""
Models for authentication.

Provides User class as a child of AbstractUser with optional attribute table_id
"""

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from dining_table.models import Table
from REST_QR_aunt.models import SoftDeleteModel
from .managers import CustomUserManager


class User(SoftDeleteModel, AbstractUser):
    """
    Represents User in the system.

    Users with is_staff=False represent dining tables and have a corresponding table_id
    """
    
    objects = CustomUserManager()
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        """Return a human-readable identifier."""
        if not self.is_deleted:
            return f"User: {self.username}"
        else:
            return super().__str__()

    class Meta(AbstractUser.Meta):
        pass

    def clean(self):
        if self.is_staff or self.is_superuser:
            if self.table is not None:
                raise ValidationError("Staff user cannot have an associated table.")
        elif self.table is None:
            raise ValidationError("Table user must have a valid table associated with it.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)