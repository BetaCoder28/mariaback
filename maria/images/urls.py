from rest_framework import routers
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import ImagesViewSet, show_image


router = routers.DefaultRouter()
router.register('images', ImagesViewSet)

urlpatterns = [
    path('sources/media/<str:image_name>', show_image, name='show_image'),
] + router.urls



