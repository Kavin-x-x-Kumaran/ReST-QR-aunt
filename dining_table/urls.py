"""
URL configuration for dining_table app.
"""

from django.urls import path, include

from .routers import table_router

urlpatterns = [
    path('', include(table_router.urls))
]