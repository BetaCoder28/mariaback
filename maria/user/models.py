from django.db import models
from images.models import Images


class Level(models.Model):
    level = models.TextField(max_length=15)
    description = models.TextField(max_length=255)


class User(models.Model):
    name = models.TextField(max_length=50)
    lastname = models.TextField(max_length=50)
    email = models.EmailField(max_length=255)
    user_password = models.TextField(max_length=255)
    level = models.OneToOneField(Level,null=True, blank=True, related_name="user", on_delete=models.SET_NULL)
    image = models.OneToOneField(Images, null=True, blank=True, on_delete=models.SET_NULL, related_name="user")




