from django.contrib import admin
from .models import Lesson

class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'vocabulary', 'image', 'example', 'drag_and_drop')  # Campos que deseas mostrar en el listado
    search_fields = ('id', 'vocabulary')  # Campos que puedes usar para buscar
    list_filter = ('vocabulary',)  # Filtros para el panel de administración
    ordering = ('id',)  # Orden por defecto

admin.site.register(Lesson, LessonAdmin)
