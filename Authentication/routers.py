from rest_framework.routers import DefaultRouter

from .views import UserView

auth_router = DefaultRouter()
auth_router.register(r'user', UserView)