"""
Permission for authentication.

Provides permission classes restricted to superusers.
"""

from rest_framework.permissions import BasePermission


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