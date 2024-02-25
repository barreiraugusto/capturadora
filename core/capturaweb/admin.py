from django.contrib import admin

from core.capturaweb.models import Grabacion, DatosGrabadora, GrabacionProgramada


class GrabacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'duracion', 'convertida', 'tipo_grabacion']


class DatosGrabadoraAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'placa', 'formato', 'directorio_de_grabacion']


class GrabacionProgramadaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes',
                    'sabado', 'domingo', 'hora_inicio', 'hora_fin']


admin.site.register(Grabacion, GrabacionAdmin)
admin.site.register(DatosGrabadora, DatosGrabadoraAdmin)
admin.site.register(GrabacionProgramada, GrabacionProgramadaAdmin)
