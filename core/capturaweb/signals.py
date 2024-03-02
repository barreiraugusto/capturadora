import datetime
import logging
import re

from django.db.models.signals import post_save, post_migrate
from django.dispatch import Signal
from django.dispatch import receiver

from config import settings
from .datos_temp import guardar_datos

logger = logging.getLogger('capturadora')

from .conversor import Convertir
from .grabar import Captura
from .models import GrabacionProgramada
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

process_started = Signal()
process_finished = Signal()

db_path = str(settings.DATABASES['default']['NAME'])

jobstore = {
    'default': SQLAlchemyJobStore(url=f'sqlite:///{db_path}')
}

scheduler = BackgroundScheduler(jobstores=jobstore)


def iniciar_grabacion(instance):
    nueva_grabacion = Captura()
    zona_hora = datetime.timezone(datetime.timedelta(hours=-3))
    hora_arg = datetime.datetime.now(zona_hora)
    hora = str(hora_arg.hour) + "h" + str(hora_arg.minute) + "m"
    titulo_pos = f'{instance.titulo.upper()}_{hora}'
    titulo = re.sub(r'[/. ,]', '_', titulo_pos)
    guardar_datos(titulo, instance.tipo_grabacion, instance.segmento, False,
                  instance.convertida, "00:00:00")
    process_started.send(sender=None)
    if instance.tipo_grabacion == 2:
        segmento = instance.segmento
        logger.debug(f'GRABAR SEGMENTADA - {titulo}')
        nueva_grabacion.para_captura_segmentada(titulo, segmento)
    elif instance.tipo_grabacion == 1:
        logger.debug(f'GRABAR - {titulo}')
        nueva_grabacion.para_capturar(titulo)


def parar_grabacion(instance):
    nueva_grabacion = Captura()
    convertidor = Convertir()
    zona_hora = datetime.timezone(datetime.timedelta(hours=-3))
    hora_arg = datetime.datetime.now(zona_hora)
    hora = str(hora_arg.hour) + "h" + str(hora_arg.minute) + "m"
    titulo_pos = f'{instance.titulo.upper()}_{hora}'
    titulo = re.sub(r'[/. ,]', '_', titulo_pos)
    convertir = instance.convertida
    nueva_grabacion.stop()
    process_finished.send(sender=None)
    logger.debug(f'STOP - {titulo}')
    if convertir == "True":
        convertidor.para_convertir(titulo)


@receiver(post_save, sender=GrabacionProgramada)
def programar_tarea_nueva(instance, created, **kwargs):
    print(f"Programar tera nueva {instance} <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    if created:
        scheduler.add_job(iniciar_grabacion, 'cron', day_of_week=instance.get_dias_semana(),
                          hour=instance.hora_inicio.hour,
                          minute=instance.hora_inicio.minute, id=f"iniciar_grabacion_{instance.id}", args=(instance,))

        scheduler.add_job(parar_grabacion, 'cron', day_of_week=instance.get_dias_semana(),
                          hour=instance.hora_fin.hour,
                          minute=instance.hora_fin.minute, id=f"parar_grabacion_{instance.id}", args=(instance,))

        if not scheduler.running:
            scheduler.start()


@receiver(post_migrate)
def rehacer_schedule(**kwargs):
    grabaciones_programadas = GrabacionProgramada.objects.all()

    if not scheduler.running:
        scheduler.start()

    for job in scheduler.get_jobs():
        scheduler.remove_job(job.id)

    for grabacion in grabaciones_programadas:
        programar_tarea_nueva(grabacion, True, **kwargs)
