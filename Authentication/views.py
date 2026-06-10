from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet
from .serializers import *

class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_staff and
            request.user.is_superuser
        )
    
    
class UserView(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]
