from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from .permissions import IsAdmin
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import User, Level
from .serializers import UserSerializer, LevelSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdmin]


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
