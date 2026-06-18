"""
Views for authentication.

Provides views for accommodating HTTP requests.
"""

from rest_framework.viewsets import ModelViewSet

from .models import User
from .permissions import IsSuperUser
from .serializers import UserSerializer


class UserView(ModelViewSet):
    """
    Viewset for managing users.

    Restricts access to superusers.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]
