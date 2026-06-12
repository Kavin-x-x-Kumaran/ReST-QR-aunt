"""
Models for Authentication.

Provides User class as a child of AbstractUser without any additional fields. Useful for future customization.
"""
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Represents User in the system.

    Currently identical to AbstractUser and reserved for future customization.
    """

    pass
