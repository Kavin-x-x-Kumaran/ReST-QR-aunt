"""
URL configuration for authentication app.
"""

from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .routers import auth_router

urlpatterns = [
    path("", include(auth_router.urls)),
    path("token/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]
