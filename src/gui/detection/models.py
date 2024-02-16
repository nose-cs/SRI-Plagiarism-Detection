from django.db import models

class Documento(models.Model):
    archivo = models.FileField(upload_to='documentos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)