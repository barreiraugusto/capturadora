from django.db import models


class Grabacion(models.Model):
    titulo = models.CharField(max_length=100)
    duracion = models.DurationField(default=0)
    convertida = models.BooleanField(verbose_name="Convertir", default=False)
    tipo_grabacion = models.IntegerField(verbose_name="Tipo", default=1)

    def __str__(self):
        return self.titulo


class DatosGrabadora(models.Model):
    nombre = models.CharField(verbose_name="Nombre de la capturadora", max_length=100)
    placa = models.CharField(verbose_name="Modelo de la placa", max_length=100)
    formato = models.CharField(verbose_name="Formato de grabacion", max_length=2)
    directorio_de_grabacion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
