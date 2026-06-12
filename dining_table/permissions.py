"""
Permission for dining.

Provides permission classes restricting GET, POST, DELETE to superusers.
"""

from rest_framework.permissions import BasePermission


class IsAllowedAccess(BasePermission):
    """Allows only superusers to GET, POST or DELETE."""

    def has_permission(self, request, view):
        if view.action in ["list", "retrieve", "create", "destroy"]:
            return (
                request.user
                and request.user.is_authenticated
                and request.user.is_staff
                and request.user.is_superuser
            )
        return request.user.is_authenticated
