from rest_framework import routers
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import ImagesViewSet, ShowImage


router = routers.DefaultRouter()
router.register('images', ImagesViewSet)

urlpatterns = [
    path('sources/media/<str:image_name>', ShowImage.as_view(), name='show_image'),
] + router.urls



