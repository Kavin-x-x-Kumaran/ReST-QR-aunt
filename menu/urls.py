"""
URL configuration for menu app.
"""

from django.urls import path, include

from .views import CategoryAdminView, CategoryListView

urlpatterns = [
    path("categories/", CategoryListView.as_view()),
    path("admin/categories/", CategoryAdminView.as_view()),
    path("admin/categories/<int:pk>/", CategoryAdminView.as_view()),
]