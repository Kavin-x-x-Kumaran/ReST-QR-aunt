"""
Routers used in dining_table.

Provides router for the TableView class.
"""

from rest_framework.routers import DefaultRouter

from .views import TableView

table_router = DefaultRouter()
table_router.register(r"tables", TableView)
