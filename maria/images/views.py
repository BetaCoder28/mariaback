import os
from datetime import datetime

from django.http import FileResponse
from django.conf import settings
from rest_framework import permissions, viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsAdmin
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Images
from .serializers import ImagesSerializers
from user.models import User


class ImagesViewSet(viewsets.ModelViewSet):
    #Trabajará con todoso los objetos del modelo images
    queryset = Images.objects.all()
    #Asociamos el serializador al viewset
    serializer_class = ImagesSerializers 
    #permission_classes = [IsAuthenticatedOrReadOnly, IsAdmin]


    @action(detail = False, methods = ['POST'])
    def upload_image(self, request):
        user_id = request.data.get("user_id")
        
        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=user_id)
        
        image_file = request.FILES.get("image")
        if not image_file:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"image/{timestamp}_image_{user_id}.jpg"

        image = Images.objects.create(image_path=filename)
        user.image = image
        user.save()

        with open(os.path.join(settings.MEDIA_ROOT, filename), 'wb') as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        return Response({"message": "Image uploaded successfully", "image_path": image.image_path.url}, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['GET'], url_path='user/(?P<user_id>[^/.]+)')
    def get_image_by_user(self, request, user_id = None):
        user = get_object_or_404(User, id=user_id)

        if not user.image:
            return Response({"error": "User has no associated image"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"image_path": user.image.image_path.name})
    

    @action(detail=False, methods=["GET"], url_path='(?P<image_name>[^/.]+)')
    def get_image_by_name(self, request, image_path=None):
        file_path = os.path.join(settings.MEDIA_ROOT,image_path)

        if not os.path.exists(file_path):
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

        return FileResponse(open(file_path, 'rb'), content_tye="image/jpeg")
