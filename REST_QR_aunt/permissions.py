"""
Common permission classes for all apps.

Provides IsSuperUser permission class.
"""

from rest_framework.permissions import IsAdminUser, BasePermission


class IsSuperUser(BasePermission):
    """Permission class for superusers."""

    def has_permission(self, request, view):
        """Returns True if the user is a superuser."""
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
            and request.user.is_superuser
        )


class IsStaffUser(IsAdminUser):
    """
    Permission class for kitchen staff.

    Inherits from IsAdminUser.
    Solely to retain clarity.
    """
    pass