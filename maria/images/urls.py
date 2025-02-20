from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from .views import ImagesViewSet


router = routers.DefaultRouter()
router.register('images', ImagesViewSet)

urlpatterns = router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

