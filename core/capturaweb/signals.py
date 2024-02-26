import datetime
import inspect
import logging
import re

from django.db.models.signals import post_save
from django.dispatch import receiver

from .datos_temp import guardar_datos

logger = logging.getLogger('capturadora')

from .conversor import Convertir
from .grabar import Captura
from .models import GrabacionProgramada
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

# Configura el almacenamiento en una base de datos SQLite
jobstore = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
scheduler = BackgroundScheduler(jobstores=jobstore)


@receiver(post_save, sender=GrabacionProgramada)
def programar_tarea_nueva(sender, instance, created, **kwargs):
    if created:
        nueva_grabacion = Captura()
        convertidor = Convertir()
        zona_hora = datetime.timezone(datetime.timedelta(hours=-3))
        hora_arg = datetime.datetime.now(zona_hora)
        hora = str(hora_arg.hour) + "h" + str(hora_arg.minute) + "m"
        titulo_pos = f'{instance.titulo.upper()}_{hora}'
        titulo = re.sub(r'[/. ,]', '_', titulo_pos)

        def inicar_grabacion():
            guardar_datos(titulo, instance.tipo_grabacion, instance.segmento, False,
                          instance.convertida, "00:00:00")
            if instance.tipo_grabacion == 2:
                segmento = instance.segmanto
                nueva_grabacion.para_captura_segmentada(titulo, segmento)
            elif instance.tipo_grabacion == 1:
                logger.debug(f'GRABAR - {titulo}')
                nueva_grabacion.para_capturar(titulo)

        def parar_grabacion():
            convertir = instance.convertida
            nueva_grabacion.stop()
            logger.debug(f'STOP - {titulo}')
            if convertir == "True":
                convertidor.para_convertir(titulo)

        scheduler.add_job('capturaweb:iniciar_grabacion', 'cron', day_of_week=instance.get_dias_semana(),
                          hour=instance.hora_inicio.hour,
                          minute=instance.hora_inicio.minute, id=f"iniciar_grabacion_{instance.id}")

        scheduler.add_job('capturaweb:parar_grabacion', 'cron', day_of_week=instance.get_dias_semana(),
                          hour=instance.hora_fin.hour,
                          minute=instance.hora_fin.minute, id=f"parar_grabacion_{instance.id}")

        if not scheduler.running:
            scheduler.start()
