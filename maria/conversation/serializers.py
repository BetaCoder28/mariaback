from rest_framework import serializers

from .models import Messages


class MessagesSerializer(serializers.ModelSerializer):

    topic = serializers.CharField(max_length=50, required=False, default='introduce yourself')

    class Meta:
        model = Messages
        fields = [
            'role',
            'content',
            'topic'
        ]

    def __init__(self, *args, **kwargs):
        method = kwargs.pop('method', None)
        super().__init__(*args, **kwargs)

        if method == 'GET':
            self.fields.pop('topic')

    

