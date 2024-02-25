from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models.signals import post_save
from django.dispatch import receiver

import logging

from .datos_temp import guardar_datos

logger = logging.getLogger('capturadora')


from .conversor import Convertir
from .grabar import Captura
from .models import GrabacionProgramada

scheduler = BackgroundScheduler()


@receiver(post_save, sender=GrabacionProgramada)
def programar_tarea_nueva(sender, instance, created, **kwargs):
    if created:
        nueva_grabacion = Captura()
        convertidor = Convertir()

        def inicar_grabacion():
            guardar_datos(instance.titulo, instance.tipo_grabacion, instance.segmento, False,
                          instance.convertida, "00:00:00")
            if instance.tipo_grabacion == 2:
                segmento = instance.segmanto
                nueva_grabacion.para_captura_segmentada(instance.titulo, segmento)
            elif instance.tipo_grabacion == 1:
                logger.debug(f'GRABAR - {instance.titulo}')
                nueva_grabacion.para_capturar(instance.titulo)

        def parar_grabacion():
            convertir = instance.convertida
            nueva_grabacion.stop()
            logger.debug(f'STOP - {instance.titulo}')
            if convertir == "True":
                titulo = instance.titulo
                convertidor.para_convertir(titulo)

        scheduler.add_job(inicar_grabacion, 'cron', day_of_week=instance.get_dias_semana(),
                          hour=instance.hora_inicio.hour,
                          minute=instance.hora_inicio.minute, id=f"iniciar_grabacion_{instance.id}")

        scheduler.add_job(parar_grabacion, 'cron', day_of_week=instance.get_dias_semana(),
                          hour=instance.hora_fin.hour,
                          minute=instance.hora_fin.minute, id=f"parar_grabacion_{instance.id}")

        if not scheduler.running:
            scheduler.start()
