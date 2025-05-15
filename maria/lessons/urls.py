from rest_framework import routers
from .views import LessonViewSet


router = routers.DefaultRouter()
router.register('lessons', LessonViewSet, basename='lesson')

urlpatterns = router.urls