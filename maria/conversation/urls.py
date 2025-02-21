from rest_framework import routers

from .views import ChatView


router = routers.DefaultRouter()
router.register('chat', ChatView, basename='chat')

urlpatterns = router.urls