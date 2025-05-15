from django.db import models


class User(models.Model):

    email = models.EmailField(max_length=100)
    name = models.TextField(max_length=50)
    lastname = models.TextField(max_length=50)
    password = models.TextField(max_length=255)
    age = models.IntegerField()