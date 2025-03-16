from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import UserSerializer
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':  # Permitir acceso público solo al registro
            return [AllowAny()]
        return [IsAuthenticated()] 
    