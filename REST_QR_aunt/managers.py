"""
Provides SoftDeleteManager
"""

from django.db import models

from .querysets import SoftDeleteQueryset


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQueryset(
            self.model,
            using=self.db,
        ).filter(is_deleted=False)