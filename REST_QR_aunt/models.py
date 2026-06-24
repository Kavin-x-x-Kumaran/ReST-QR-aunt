"""
Provides the Base abstract model.
"""

import uuid
from django.db import models


class Base(models.Model):
    """
    Abstract model that provides UUID to all child models.

    Base is the parent of all models used in the project.
    """

    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        """Return a human-readable identifier."""
        return f"Database entry: {self.public_id}"
