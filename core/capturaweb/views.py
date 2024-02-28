import datetime
import re
import time

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, CreateView, UpdateView, DeleteView
from django.views.generic import ListView

from .conversor import Convertir
from .datos_temp import guardar_datos, obtener_dato, eliminar_datos
from .forms import DatosGrabacionForm, ProgramarGrabacionForm
from .grabar import Captura
from .models import DatosGrabadora
from .models import GrabacionProgramada


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
                    guardar_datos(titulo, data.get("tipo_grabacion"), data.get("segmento"), False,
                                  data.get("convertida"), "00:00:00")
                    self.grabacion.para_capturar(titulo)
            time.sleep(2)
            ocupada = self.grabacion.en_proceso()
            context = self.get_context_data(form=form, ocupada=ocupada, titulo=titulo)
        elif 'stop' in self.request.POST:
            convertir = data.get("convertida")
            if ocupada:
                self.grabacion.stop()
                if convertir == "True":
                    titulo = obtener_dato(self.path_temp, "titulo")
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
        context['grabaciones_programadas'] = GrabacionProgramada.objects.all()
        return context


class GrabacionesProgramadasListView(ListView):
    template_name = 'capturaweb/grabaciones_programadas.html'
    model = GrabacionProgramada
    success_url = reverse_lazy('capturaweb')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anterior'] = 'Inicio'
        context['url_general'] = reverse_lazy('capturaweb')
        context['comentario'] = 'Programe una grabacion automatica'
        context['title_table'] = 'Programadas'
        context['segment'] = 'alumnos'
        context['btn_accion'] = 'Guardar'
        context['title'] = 'Programar'
        return context


@require_http_methods(["GET"])
def stream_view(request):
    # Suponiendo que tu servidor de transmisión es localhost y el puerto es 1935
    # Ajusta esto según tu configuración
    stream_url = "rtmp://192.168.2.62:1935/live"
    return HttpResponse(stream_url, content_type="video/mp4")


class ProgramarGrabacion(CreateView):
    model = GrabacionProgramada
    form_class = ProgramarGrabacionForm
    template_name = 'capturaweb/agregar_grabacion.html'
    success_url = reverse_lazy('grabaciones_programadas')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        errors = form.errors['__all__'] if '__all__' in form.errors else None
        return self.render_to_response(self.get_context_data(errors=errors))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anterior'] = 'Grabaciones Programadas'
        context['url_general'] = reverse_lazy('grabaciones_programadas')
        context['comentario'] = 'Programe una grabacion automatica'
        context['title_table'] = 'Programadas'
        context['segment'] = 'alumnos'
        context['btn_accion'] = 'Guardar'
        context['title'] = 'Programar'
        return context


class UpdateGrabacionView(UpdateView):
    model = GrabacionProgramada
    form_class = ProgramarGrabacionForm
    template_name = 'capturaweb/update_grabacion.html'
    success_url = reverse_lazy('capturaweb')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        errors = form.errors['__all__'] if '__all__' in form.errors else None
        return self.render_to_response(self.get_context_data(errors=errors))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anterior'] = 'Inicio'
        context['url_general'] = reverse_lazy('capturaweb')
        context['comentario'] = 'Programe una grabacion automatica'
        context['title_table'] = 'Programadas'
        context['segment'] = 'alumnos'
        context['btn_accion'] = 'Guardar'
        return context


class BorrarGrabacionView(DeleteView):
    model = GrabacionProgramada
    template_name = 'capturaweb/borrar_grabacion.html'
    success_url = reverse_lazy('capturaweb')

    def get_grabacion(self):
        return GrabacionProgramada.objects.get(id=self.object.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comentario'] = f'Se eliminara la grabacion!'
        context['mensaje'] = f'Decea borrar la grabacion {self.get_grabacion()}'
        context['anterior'] = 'Inicio'
        context['url_general'] = reverse_lazy('capturaweb')
        context['btn_accion'] = 'Guardar'
        return context


class GrabacionesProgramadasSchedulerListView(ListView):
    model = GrabacionProgramada
    template_name = 'capturaweb/scheduler.html'  # Nombre de tu plantilla donde se mostrarán las grabaciones programadas
    context_object_name = 'grabaciones'

    def get_queryset(self):
        # Aquí puedes obtener las grabaciones programadas del scheduler
        # Puedes acceder a la instancia de BackgroundScheduler a través de tu módulo
        # Si estás usando el mismo módulo donde tienes el scheduler, simplemente importa el scheduler desde allí
        # Si el scheduler está definido en un módulo diferente, importa el scheduler desde ese módulo
        # Por ejemplo, si el scheduler está definido en 'signals.py', puedes importarlo así:
        from .signals import scheduler

        # Obtén todos los trabajos programados del scheduler
        jobs = scheduler.get_jobs()

        # Si quieres acceder a la información de las grabaciones programadas
        # Puedes filtrar los trabajos basados en su id o algún otro atributo
        grabaciones_programadas = []
        for job in jobs:
            if job.id.startswith('iniciar_grabacion_') or job.id.startswith('parar_grabacion_'):
                grabaciones_programadas.append(job)

        return grabaciones_programadas

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context
