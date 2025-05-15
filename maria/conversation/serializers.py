from rest_framework import serializers

from .models import Messages, Feedback


class MessagesSerializer(serializers.ModelSerializer):

    conversation_id = serializers.CharField(required=False, default="default_conversation")

    class Meta:
        model = Messages
        fields = [
            'role',
            'content',
            'conversation_id'
        ]


    
class FeedbackSerializer(serializers.ModelSerializer):
    
    conversation_id = serializers.CharField(required=False, default="default_conversation")

    class Meta:
        model = Feedback
        fields = [
            'conversation',
            'conversation_id'
        ]

