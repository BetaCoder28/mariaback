from rest_framework import routers
from django.urls import path

from .views import ChatView, FeedbackView


router = routers.DefaultRouter()
router.register('chat', ChatView, basename='chat')
router.register('feedback', FeedbackView, basename='feedback')

urlpatterns = [
     path('chat/audio/<str:filename>/', ChatView.as_view({'get': 'get_audio'}), name='get_audio')
] + router.urls