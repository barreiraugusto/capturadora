from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('control_repetidoras')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Notifica el estado de los bit de bajada de cada equipo
    'notificacion_de_funcionamieto': {
        'task': 'core.graficas.tasks.get_datos_actuales',
        'schedule': crontab(minute='*/1'),
    },
    # Leer el archivo a_estado de cada localidad
    'notificacion_de_problemas': {
        'task': 'core.graficas.tasks.notificar_problemas',
        'schedule': crontab(minute=0, hour=8),
    },
}

app.conf.update(
    result_expires=3600,
)