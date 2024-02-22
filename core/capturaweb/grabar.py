import os
import threading
import time
from datetime import date
from datetime import datetime

from core.capturaweb.models import DatosGrabadora


def get_hora():
    ahora = datetime.now()
    return f"{ahora.hour}-{ahora.minute}-{ahora.second}"


class Captura:
    def __init__(self):
        self.hoy = date.today()
        self.nombre = "Nada"
        self.segmento = 10
        self.capturarlo = False
        self.capturarlo_seg = False
        self.dia = self.hoy.strftime("%d-%m-%Y")
        self.crear_directorio_captura()
        self.th_capturar = threading.Thread(target=self.capturar)
        self.th_capturar.start()

        self.proceso = None
        self.pid = None

        self.th_capturar_segmentada = threading.Thread(target=self.captura_segmentada)
        self.th_capturar_segmentada.start()

    def get_datos_capturadora(self):
        try:
            return DatosGrabadora.objects.all()[0]
        except IndexError:
            return False

    def crear_directorio_captura(self):
        ruta_directorio = f"/media/video/Captura_{self.dia}"
        if not os.path.exists(ruta_directorio):
            os.makedirs(ruta_directorio)
            os.chmod(ruta_directorio, 0o777)
            os.makedirs(f"{ruta_directorio}/OV")
            os.chmod(f"{ruta_directorio}/OV", 0o777)

    def pid_proceso(self):  # saco el ID del proceso de ffmpeg que esta ocupando la placa DeckLink
        comando = os.popen("ps aux | grep ffmpeg | grep DeckLink").read()
        lista_comando = comando.split()
        self.pid = lista_comando[1]
        if "decklink" in lista_comando:
            return self.pid
        else:
            return False

    def en_proceso(self):  # devuelve True o False dependiendo de si el proceso esta en ejecucion o no
        proceso = self.pid_proceso()
        if proceso:
            capturando = True
        else:
            capturando = False
        return capturando

    def para_capturar(self, nombre):
        self.nombre = nombre
        self.capturarlo = True

    def para_captura_segmentada(self, nombre, segmento=60):
        self.segmento = segmento
        self.nombre = nombre
        self.capturarlo_seg = True

    def capturar(self):  # Inicia captura
        while True:
            time.sleep(.5)
            if self.capturarlo:
                capturadora = self.get_datos_capturadora()
                self.capturarlo = False
                capturando = self.en_proceso()
                try:
                    if not capturando:
                        nombre = self.nombre
                        placa = capturadora.placa
                        formato = capturadora.formato
                        direccion = capturadora.direccion_de_grabacion
                        os.system(
                            f"utils/rec.sh {nombre} {placa} {formato} {direccion}")
                    else:
                        return False
                except AttributeError:
                    pass
            else:
                pass

    def captura_segmentada(self):  # Inicia captura segmentada
        while True:
            time.sleep(.5)
            if self.capturarlo_seg:
                capturadora = self.get_datos_capturadora()
                self.capturarlo_seg = False
                capturando = self.en_proceso()
                try:
                    if not capturando:
                        nombre = self.nombre
                        segmento = self.segmento
                        placa = capturadora.placa
                        formato = capturadora.formato
                        direccion = capturadora.direccion_de_grabacion
                        os.system(
                            f"utils/rec_secuencial.sh {nombre} {segmento} {placa} {formato} {direccion}")
                    else:
                        return False
                except AttributeError:
                    pass
            else:
                pass

    def stop(self):  # Finaliza la captura matando el proceso identificado en pid_proceso
        capturando = self.en_proceso()
        pid = self.pid_proceso()
        if capturando:
            os.system(f"kill {pid}")
            os.system(f"rm /tmp/datos")
