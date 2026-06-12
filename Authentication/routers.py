"""
Routers for Authentication.

Provides router for the UserView class used for user authentication.
"""

from rest_framework.routers import DefaultRouter

from .views import UserView

auth_router = DefaultRouter()
auth_router.register("user", UserView)
