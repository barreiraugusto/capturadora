import datetime
import re
import time

from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from .conversor import Convertir
from .datos_temp import guardar_datos, obtener_dato, eliminar_datos
from .forms import DatosGrabacionForm
from .grabar import Captura
from .models import DatosGrabadora


class CapturaView(FormView):
    template_name = 'capturaweb/grabadora.html'
    form_class = DatosGrabacionForm
    success_url = reverse_lazy('capturaweb')
    grabacion = Captura()
    convertir = Convertir()
    path_temp = '/tmp/grabacion_actual'

    def get_datos_capturadora(self):
        try:
            return DatosGrabadora.objects.all()[0]
        except IndexError:
            return False

    def form_valid(self, form):
        global context
        data = form.cleaned_data
        zona_hora = datetime.timezone(datetime.timedelta(hours=-3))
        hora_arg = datetime.datetime.now(zona_hora)
        ocupada = self.grabacion.en_proceso()
        hora = str(hora_arg.hour) + "h" + str(hora_arg.minute) + "m"
        titulo_pos = f'{data.get("titulo").upper()}_{hora}'
        titulo = re.sub(r'[/. ,]', '_', titulo_pos)

        if 'rec' in self.request.POST:
            tipo_grabacion = data.get("tipo_grabacion")
            if ocupada:
                titulo = obtener_dato(self.path_temp, "titulo")
                messages.error(self.request,
                               f'La grabacion {titulo} está en curso.\n Deténgala antes de comenzar una nueva grabación')
            else:
                if tipo_grabacion == "2":
                    segmento = data.get("segmento")
                    guardar_datos(titulo, data.get("tipo_grabacion"), data.get("segmento"), False,
                                  data.get("convertida"), "00:00:00")
                    self.grabacion.para_captura_segmentada(titulo, segmento)
                elif tipo_grabacion == "1":
                    guardar_datos(titulo, "None", data.get("tipo_grabacion"), data.get("segmento"), False,
                                  data.get("convertida"))
                    self.grabacion.para_capturar(titulo)
            time.sleep(2)
            ocupada = self.grabacion.en_proceso()
            context = self.get_context_data(form=form, ocupada=ocupada, titulo=titulo)
        elif 'stop' in self.request.POST:
            convertir = data.get("convertir")
            if ocupada:
                self.grabacion.stop()
                if convertir:
                    self.convertir.para_convertir(titulo)
                eliminar_datos(self.path_temp)
            time.sleep(2)
            context = self.get_context_data(form=form)

        return render(self.request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ocupada = self.grabacion.en_proceso()
        if ocupada:
            context['ocupada'] = True
            obtener_dato(self.path_temp, 'titulo')
            initial_data = {
                'titulo': obtener_dato(self.path_temp, 'titulo'),
                'tipo_grabacion': obtener_dato(self.path_temp, 'tipo'),
                'segmento': obtener_dato(self.path_temp, 'segmento'),
                'convertida': obtener_dato(self.path_temp, 'convertir'),
            }
            form = DatosGrabacionForm(initial=initial_data)
            context['titulo'] = obtener_dato(self.path_temp, 'titulo'),
            context['form'] = form
        context['grabadora'] = self.get_datos_capturadora().nombre
        return context
