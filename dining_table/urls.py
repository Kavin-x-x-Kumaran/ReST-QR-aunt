"""
URL configuration for dining_table app.
"""

from django.urls import path, include

from .routers import table_router
from .views import BillView

urlpatterns = [
    path("", include(table_router.urls)),
    path("<int:table_id>/bills/", BillView.as_view()),  # For get, patch, post
    path("bills/<int:bill_id>/", BillView.as_view()),  # For delete, get (admin only)
]
