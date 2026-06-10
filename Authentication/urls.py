from django.urls import path, include
from .routers import *

from .views import *

urlpatterns = [
    path('user/<int:pk>/', include(auth_router.urls))
]