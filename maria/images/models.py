from django.db import models


class Images(models.Model):
    #Image Field permite manejar la carga de imagenes
    image_path = models.ImageField(upload_to='image/')
    #upload_to indica que las imagenes se guardarán en la carpeta images del directorio de medios
