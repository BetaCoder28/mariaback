from django.db import models


class Lesson(models.Model):

    vocabulary = models.JSONField()
    image = models.ImageField()
    example = models.TextField()
    drag_and_drop = models.JSONField() 
    