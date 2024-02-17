from django.db import models

class Documento(models.Model):
    name = models.TextField()
    file = models.FileField(upload_to='documentos/')
    upload_date = models.DateTimeField(auto_now_add=True)