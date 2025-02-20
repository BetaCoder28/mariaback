from rest_framework import serializers

from .models import User, Level
from images.models import Images
from images.serializers import ImagesSerializers


class UserSerializer(serializers.ModelSerializer):

    image = ImagesSerializers(required=False)
    level = serializers.CharField(source='level.level', read_only=True)

    class Meta:
        model = User
        fields = [
            'name',
            'lastname',
            'email',
            'user_password',
            'level',
            'image'
        ]
    

    def get_image(self,obj):
        if obj.image:
            return obj.image.image_path.name #Retornar ruta relativa
        
        return None


    #crear un usuario con una imagen asociada en una sola solicitud.
    def create(self, validated_data):
        image_data = validated_data.pop('image', None)
        user = User.objects.create(**validated_data)

        if image_data:
            image = Images.objects.create(**image_data)
            user.image = image
            user.save()

        return user


class LevelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Level
        fields = [
            'level',
            'description'
        ]

