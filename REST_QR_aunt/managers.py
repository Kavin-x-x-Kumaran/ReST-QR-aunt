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

    def get_by_natural_key(self, username):
        if hasattr(self.model, "normalize_username"):
            username = self.model.normalize_username(username)
        return self.get(**{self.model.USERNAME_FIELD: username})