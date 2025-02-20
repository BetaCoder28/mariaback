from rest_framework import serializers

from .models import Images


class ImagesSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Images
        fields = ['image_path']

