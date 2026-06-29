"""
URL configuration for menu app.
"""

# from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ItemViewSet

urlpatterns = []

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'items', ItemViewSet)
urlpatterns += router.urls