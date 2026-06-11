from rest_framework.viewsets import ModelViewSet

from .models import User
from .permissions import IsSuperUser
from .serializers import UserSerializer


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]
