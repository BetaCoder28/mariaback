from rest_framework import viewsets
from .models import Lesson
from .serializers import LessonSerializer
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        is_authenticated = request.user and request.user.is_authenticated
        if request.method in permissions.SAFE_METHODS:
            return is_authenticated
        return is_authenticated and request.user.is_staff
    

class LessonViewSet(viewsets.ModelViewSet):

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminOrReadOnly]

