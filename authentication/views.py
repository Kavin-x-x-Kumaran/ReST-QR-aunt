"""
Views for authentication.

Provides views for accommodating HTTP requests.
"""

from rest_framework.viewsets import ModelViewSet

from REST_QR_aunt.permissions import IsSuperUser
from .models import User
from .serializers import UserSerializer


class UserView(ModelViewSet):
    """
    Viewset for managing users.

    Restricts access to superusers.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]
    lookup_field = "public_id"
