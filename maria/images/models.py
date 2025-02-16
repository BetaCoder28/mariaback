from django.db import models


class Images(models.Model):
    image_path = models.TextField(max_length=255)
