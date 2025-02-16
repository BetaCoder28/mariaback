from django.db import models


class Topic(models.Model):
    title = models.TextField(max_length=255)
    content = models.JSONField()
    image_rul = models.TextField(max_length=255)


