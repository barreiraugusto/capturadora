from django.db import models


class Grabacion(models.Model):
    titulo = models.CharField(max_length=100)
    duracion = models.DurationField(default=0)
    convertida = models.BooleanField(verbose_name="Convertir", default=False)
    tipo_grabacion = models.IntegerField(verbose_name="Tipo", default=1)

    def __str__(self):
        return self.titulo
