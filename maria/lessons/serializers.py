from rest_framework import serializers
from .models import Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('id',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        # Genera la URL absoluta para la imagen
        if instance.image:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        else:
            representation['image'] = None
        
        return representation