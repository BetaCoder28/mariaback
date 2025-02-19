from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from .permissions import IsAdmin
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Images
from .serializers import ImagesSerializers


class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.object.all()
    serializer_class = ImagesSerializers
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdmin]

