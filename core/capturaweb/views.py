import datetime
import os

from django.http import StreamingHttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from .forms import DatosGrabacionForm
from .conversor import Convertir
from .grabar import Captura
from .tiempo import get_tiempo
from config.settings import BASE_DIR

import threading


class CapturaView(View):

    template_name = 'capturaweb/grabadora.html'
    form_class = DatosGrabacionForm
    success_url = reverse_lazy('capturaweb')
    grabacion = Captura()
    convertir = Convertir()

    def get(self, request):
        archivo = os.path.join(BASE_DIR, 'cuenta.txt')
        tiempos = get_tiempo(archivo)
        return JsonResponse({'tiempos': tiempos})

#     def form_valid(self, form):
#         data = form.cleaned_data
#         zona_hora = datetime.timezone(datetime.timedelta(hours=-3))
#         hora_arg = datetime.datetime.now(zona_hora)
#         ocupada = self.grabacion.en_proceso()
#         hora = str(hora_arg.hour) + "h" + str(hora_arg.minute) + "m"  # time.strftime("%H%M")
#         # ruta_temp = "/var/www/html/capturadora/capturadora/plantillas/temp.txt"
#         ruta_temp = "/home/augusto/Documentos/CODIGOS/CAPTURADORA/temp.txt"
#         leer_nombre_archivo = open(ruta_temp, "r")
#         nombre_archivo = leer_nombre_archivo.read()
#         get_tiempo(os.path.join(BASE_DIR, 'material.txt'))
#         if 'rec' in self.request.POST:
#             tipo_grabacion = data.get("tipo_grabacion")
#             if ocupada:
#                 nombre_archivo = leer_nombre_archivo.read()
#                 leer_nombre_archivo.close()
#             else:
#                 if tipo_grabacion == "2":
#                     ocupada = True
#                     nombre_archivo = data.get("nombre") + "_" + hora
#                     leer_nombre_archivo = open(ruta_temp, "w+")
#                     leer_nombre_archivo.write("{0}".format(nombre_archivo))
#                     leer_nombre_archivo.close()
#                     segmento = data.get("segmento_de")
#                     self.grabacion.para_captura_segmentada(nombre_archivo, segmento)
#                 elif tipo_grabacion == "1":
#                     ocupada = True
#                     data = form.cleaned_data
#                     nombre_archivo = data.get("nombre") + "_" + hora
#                     leer_nombre_archivo = open(ruta_temp, "w+")
#                     leer_nombre_archivo.write("{0}".format(nombre_archivo))
#                     leer_nombre_archivo.close()
#                     self.grabacion.para_capturar(nombre_archivo)
#         elif 'stop' in self.request.POST:
#             convertir_sino = data.get("convertir")
#             # nombre_archivo = from_data.get("nombre")
#             if ocupada:
#                 ocupada = False
#                 self.grabacion.stop()
#                 leer_nombre_archivo = open(ruta_temp, "w+")
#                 leer_nombre_archivo.close()
#                 if convertir_sino == "1":
#                     self.convertir.para_convertir(nombre_archivo)
#
#
# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['title'] = 'Cargar de Alumnos'
#     context['path_csv'] = 'EJEMPLO-INTEGRANTES.csv'
#     context['anterior'] = 'Alumnos'
#     context['url_general'] = reverse_lazy('alumnos_list')
#     context['action'] = 'edit'
#     context['btn_accion'] = 'Cargar'
#     context['list_url'] = reverse_lazy('organizacion')
#     return context
