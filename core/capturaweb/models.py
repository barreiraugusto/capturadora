from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


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


class GrabacionProgramada(models.Model):
    titulo = models.CharField(max_length=100)
    convertida = models.BooleanField(verbose_name="Convertir", default=False)
    tipo_grabacion = models.IntegerField(verbose_name="Tipo", default=1)
    # fecha = models.DateField()
    lunes = models.BooleanField("Lunes", default=None)
    martes = models.BooleanField("Martes", default=None)
    miercoles = models.BooleanField("Miercoles", default=None)
    jueves = models.BooleanField("Jueves", default=None)
    viernes = models.BooleanField("Viernes", default=None)
    sabado = models.BooleanField("Sabado", default=None)
    domingo = models.BooleanField("Domingo", default=None)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.titulo} - {self.hora_inicio} a {self.hora_fin}"

    def clean(self):
        super(GrabacionProgramada, self).clean()
        consulta_superposiciones = Q()
        dias_semana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']

        for dia in dias_semana:
            if getattr(self, dia):
                consulta_superposiciones |= Q(
                    **{dia: True, 'hora_inicio__lt': self.hora_fin, 'hora_fin__gt': self.hora_inicio})

        superposiciones = GrabacionProgramada.objects.filter(consulta_superposiciones).exclude(id=self.id)

        if superposiciones.exists():
            grabaciones_superpuestas = list(superposiciones)
            mensaje = 'La grabación se superpone con las siguientes grabaciones programadas:\n'
            for grabacion in grabaciones_superpuestas:
                mensaje += f'- {grabacion.titulo} ({grabacion.hora_inicio}-{grabacion.hora_fin})\n'
            raise ValidationError(mensaje)

    # def clean(self):
    #     superposiciones = []
    #     grabaciones = GrabacionProgramada.objects.filter(fecha=self.fecha)
    #     hora_actual_utc = timezone.now()
    #     hora_actual_argentina = hora_actual_utc.astimezone(timezone.get_current_timezone())
    #
    #     for grabacion in grabaciones:
    #         if not (self.hora_inicio >= grabacion.hora_fin or self.hora_fin <= grabacion.hora_inicio):
    #             superposiciones.append(grabacion)
    #
    #     if superposiciones:
    #         superposiciones_str = "\n, ".join(str(grabacion) for grabacion in superposiciones)
    #         raise ValidationError(
    #             f"La grabación se superpone con la(s) siguiente(s) grabación(es):{superposiciones_str}.")
    #
    #     if self.hora_inicio >= self.hora_fin:
    #         raise ValidationError("La hora de inicio debe ser anterior a la hora de finalización.")
    #
    #     if self.hora_inicio <= hora_actual_argentina.time():
    #         print(timezone.now().time())
    #         raise ValidationError(
    #             "La hora de inicio no puede ser anterior a la hora actual.")
