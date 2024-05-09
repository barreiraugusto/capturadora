import datetime
import logging
import re
import time

from django.db.models.signals import post_save, post_delete
from django.dispatch import Signal
from django.dispatch import receiver

from config import settings
from .datos_temp import guardar_datos

logger = logging.getLogger('capturadora')

from .conversor import Convertir
from .grabacion import Captura
from .models import GrabacionProgramada, Grabacion
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

process_started = Signal()
process_finished = Signal()

db_path = str(settings.DATABASES['default']['NAME'])

db_url = 'postgresql://postgres:$rtfm01@localhost/postgres'

jobstore = SQLAlchemyJobStore(url=db_url)

jobstores = {'default': jobstore, }

scheduler = BackgroundScheduler(jobstores=jobstores)


def iniciar_grabacion(instance):
    nueva_grabacion = Captura()
    zona_hora = datetime.timezone(datetime.timedelta(hours=-3))
    hora_arg = datetime.datetime.now(zona_hora)
    hora = str(hora_arg.hour) + "h" + str(hora_arg.minute) + "m"
    titulo_pos = f'{instance.titulo.upper()}_{hora}'
    titulo = re.sub(r'[/. ,]', '_', titulo_pos)
    guardar_datos(titulo, instance.tipo_grabacion, instance.segmento, False, instance.convertida, "00:00:00")
    process_started.send(sender=None)
    logger.debug(f'GRABAR PROGRAMADA - {titulo}')
    nueva_grabacion.para_capturar(instance)


def parar_grabacion(instance):
    nueva_grabacion = Captura()
    convertidor = Convertir()
    zona_hora = datetime.timezone(datetime.timedelta(hours=-3))
    hora_arg = datetime.datetime.now(zona_hora)
    hora = str(hora_arg.hour) + "h" + str(hora_arg.minute) + "m"
    logger.debug(f'PARAR GRABACION PROGRAMADA - {hora}')
    titulo_pos = f'{instance.titulo.upper()}_{hora}'
    titulo = re.sub(r'[/. ,]', '_', titulo_pos)
    convertir = instance.convertida
    nueva_grabacion.stop()
    process_finished.send(sender=None)
    logger.debug(f'STOP - {titulo}')
    if convertir == "True":
        convertidor.para_convertir(titulo)


def agregar_tarea(instance):
    scheduler.add_job(iniciar_grabacion, 'cron', day_of_week=instance.get_dias_semana(),
                      hour=instance.hora_inicio.hour,
                      minute=instance.hora_inicio.minute, id=f"iniciar_grabacion_{instance.id}", args=(instance,))

    scheduler.add_job(parar_grabacion, 'cron', day_of_week=instance.get_dias_semana(),
                      hour=instance.hora_fin.hour,
                      minute=instance.hora_fin.minute, id=f"parar_grabacion_{instance.id}", args=(instance,))


def eliminar_tarea(instance):
    scheduler.remove_job(f"iniciar_grabacion_{instance.id}")
    scheduler.remove_job(f"parar_grabacion_{instance.id}")


@receiver(post_save, sender=GrabacionProgramada)
def programar_tarea_nueva(instance, created, **kwargs):
    if created:
        agregar_tarea(instance)
        if not scheduler.running:
            scheduler.start()
    else:
        if instance.activa:
            for tarea_nombre in [f"iniciar_grabacion_{instance.id}", f"parar_grabacion_{instance.id}"]:
                tarea = scheduler.get_job(tarea_nombre)
                if tarea:
                    if tarea.next_run_time is None:
                        scheduler.resume_job(tarea_nombre)
                    else:
                        eliminar_tarea(instance)
                        agregar_tarea(instance)
        else:
            for tarea_nombre in [f"iniciar_grabacion_{instance.id}", f"parar_grabacion_{instance.id}"]:
                scheduler.pause_job(tarea_nombre)


@receiver(post_delete, sender=GrabacionProgramada)
def eliminar_tarea_al_eliminar_grabacion(sender, instance, **kwargs):
    eliminar_tarea(instance)


def rehacer_schedule(**kwargs):
    grabaciones_programadas_activas = GrabacionProgramada.objects.filter(activa=True)
    if not scheduler.running:
        scheduler.start()
    for job in scheduler.get_jobs():
        scheduler.remove_job(job.id)
    for grabacion in grabaciones_programadas_activas:
        programar_tarea_nueva(grabacion, True, **kwargs)


@receiver(post_save, sender=Grabacion)
def iniciar_grabacion_manual(sender, instance, created, **kwargs):
    logger.debug("DISPARA EL RECEIVER INICIAR_GRABACION()")
    nueva_grabacion = Captura()
    nueva_grabacion.para_capturar(instance)
