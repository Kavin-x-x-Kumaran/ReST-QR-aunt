from django.contrib.auth.models import UserManager

from REST_QR_aunt.querysets import SoftDeleteQueryset

class CustomUserManager(UserManager):
    def get_queryset(self):
        return SoftDeleteQueryset(
            self.model,
            using=self._db,
        ).filter(is_deleted=False)
