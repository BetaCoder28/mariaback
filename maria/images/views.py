import os
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.generic.base import TemplateView
from rest_framework import permissions, viewsets, status
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

    def create(self, request, *args, **kwargs):
        """Sobreescribir create para manejar la subida de archivos"""
        file = request.FILES.get('image_path')  # Obtener el archivo de la solicitud
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        image_instance = Images.objects.create(image_path=file)
        serializer = self.get_serializer(image_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShowImage(TemplateView):

    def show_image(request):
        """Vista que muestra una imagen desde una URL"""
        image_url = request.GET.get('image', '')  # Obtener la URL de la imagen de los parámetros
        if not image_url:
            return HttpResponse("No image provided", status=400)

        return render(request, 'show_image.html', {'image_url': image_url})
