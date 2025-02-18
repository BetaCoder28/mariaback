from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, LevelViewSet


router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('level', LevelViewSet)

urlpatterns = router.urls