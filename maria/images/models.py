from django.db import models
import os
from datetime import datetime


def image_upload_path(instance, filename):
    """Genera un nombre de archivo con la fecha y hora."""
    ext = filename.split('.')[-1]  # Obtener la extensión del archivo
    new_filename = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + "_" + filename
    return os.path.join('sources/media/', new_filename)


class Images(models.Model):
    #Image Field permite manejar la carga de imagenes
    image_path = models.ImageField(upload_to=image_upload_path)
    #upload_to indica que las imagenes se guardarán en la carpeta images del directorio de medios
