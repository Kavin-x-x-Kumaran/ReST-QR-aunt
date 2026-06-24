"""
Provides the Base abstract model.
"""

import uuid
from django.db import models
from django.utils import timezone

from .managers import SoftDeleteManager


class Base(models.Model):
    """
    Abstract model that provides UUID to all child models.

    Base is the parent of all models used in the project.
    """

    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        """Return a human-readable identifier."""
        return f"Database entry: {self.public_id}"
    

class SoftDeleteModel(Base):
    """
    Abstract class that implements soft delete functionality.

    Provides `is_deleted` and `deleted_at` fields, along with soft_delete() method.
    It redefines manager to redefine the queryset.
    """
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def __str__(self):
        """Return a human-readable identifier."""
        if self.is_deleted:
            return f"Database entry: {self.public_id} has been deleted."
        else:
            return super().__str__()
        
    def delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
