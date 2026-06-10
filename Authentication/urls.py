from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .routers import *

from .views import *

urlpatterns = [
    path('user/<int:pk>/', include(auth_router.urls)),
    path('token/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]