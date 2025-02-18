from rest_framework import serializers

from .models import User, Level


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'name',
            'lastname',
            'email',
            'user_password',
            'level',
        ]


class LevelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Level
        fields = [
            'level',
            'description'
        ]

