from rest_framework import serializers

from .models import User, Level
from images.models import Images
from images.serializers import ImagesSerializers


class UserSerializer(serializers.ModelSerializer):

    image = ImagesSerializers(required=False)
    level = serializers.CharField(source='level.level')

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'lastname',
            'email',
            'user_password',
            'level',
            'image'
        ]


    def create(self, validated_data):
        image_data = validated_data.pop('image', None)
        level_data = validated_data.pop('level', {})
        level_value = level_data.get('level','A0')

        level_instace, _ = Level.objects.get_or_create(level = level_value)

        user = User.objects.create(level=level_instace,**validated_data)

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

