from django.db import models


class Messages(models.Model):
    role = models.CharField(max_length=9)
    content = models.TextField()
    topic = models.TextField(max_length=50, default="if user dont ask anything, introduce yourself")
    conversation_id = models.CharField(max_length=100, default='default_conversation')


class Feedback(models.Model):
    conversation = models.TextField()
    conversation_id = models.CharField(max_length=100, default='default_conversation')