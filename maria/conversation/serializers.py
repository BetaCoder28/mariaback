from rest_framework import serializers

from .models import Messages, Feedback


class MessagesSerializer(serializers.ModelSerializer):

    topic = serializers.CharField(max_length=50, required=False, default='if user dont ask anything, introduce yourself')
    conversation_id = serializers.CharField(required=False, default="default_conversation")


    class Meta:
        model = Messages
        fields = [
            'role',
            'content',
            'topic',
            'conversation_id'
        ]

    def __init__(self, *args, **kwargs):
        method = kwargs.pop('method', None)
        super().__init__(*args, **kwargs)

        if method == 'GET':
            self.fields.pop('topic')

    
class FeedbackSerializer(serializers.ModelSerializer):
    
    conversation_id = serializers.CharField(required=False, default="default_conversation")

    class Meta:
        model = Feedback
        fields = [
            'conversation',
            'conversation_id'
        ]

