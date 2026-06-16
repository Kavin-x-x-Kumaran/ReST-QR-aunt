"""
URL configuration for menu app.
"""

from django.urls import path

from .views import (
    CategoryAdminView,
    CategoryListView,
    ItemAdminView,
    ItemListView,
    ItemStaffView,
)

urlpatterns = [
    path("categories/", CategoryListView.as_view()),
    path("items/", ItemListView.as_view()),
    path("kitchen/items/<int:pk>/", ItemStaffView.as_view()),
    path("admin/categories/", CategoryAdminView.as_view()),
    path("admin/categories/<int:pk>/", CategoryAdminView.as_view()),
    path("admin/items/", ItemAdminView.as_view()),
    path("admin/items/<int:pk>/", ItemAdminView.as_view()),
]
