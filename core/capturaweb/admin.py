from django.contrib import admin

from core.capturaweb.models import Grabacion


class GrabacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'duracion', 'convertida', 'tipo_grabacion']


admin.site.register(Grabacion, GrabacionAdmin)
