"""
URL configuration for order app.
"""

from rest_framework.routers import DefaultRouter

from .views import OrderViewSet

# from django.urls import path

# from .views import OrderView

urlpatterns = []
router = DefaultRouter()
router.register(r"orders", OrderViewSet)
urlpatterns += router.urls
