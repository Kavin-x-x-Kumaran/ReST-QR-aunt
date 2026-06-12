"""
Routers for authentication.

Provides router for the UserView class used for user authentication.
"""

from rest_framework.routers import DefaultRouter

from .views import TableView

table_router = DefaultRouter()
table_router.register(r'user', TableView)
