"""
URL configuration for authentication app.
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]

auth_router = DefaultRouter()
auth_router.register(r"users", UserView)

urlpatterns += auth_router.urls