from rest_framework import routers
from django.urls import path

from .views import UserViewSet
from .login import LoginView


router = routers.DefaultRouter()
router.register('user', UserViewSet, basename='user')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
] + router.urls