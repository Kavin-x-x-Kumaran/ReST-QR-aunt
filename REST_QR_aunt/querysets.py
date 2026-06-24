"""
Provides SoftDeleteQueryset
"""

from django.db import models
from django.utils import timezone


class SoftDeleteQueryset(models.QuerySet):
    """
    Redefines delete() method to implement soft delete.
    """

    def delete(self):
        return super().update(is_deleted=True, deleted_at=timezone.now())
