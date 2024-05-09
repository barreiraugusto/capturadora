import os
import threading
import time
import re
import logging
from datetime import date
from datetime import datetime

from core.capturaweb.models import DatosGrabadora

logger = logging.getLogger('capturadora')


def get_hora():
    ahora = datetime.now()
    return f"{ahora.hour}-{ahora.minute}-{ahora.second}"


class Captura:
    def __init__(self):
        self.nueva_captura = None
        self.hoy = date.today()
        self.titulo = None
        self.segmento = 10
        self.capturarlo = False
        self.capturarlo_seg = False
        self.dia = self.hoy.strftime("%d-%m-%Y")
        self.crear_directorio_captura()

        self.th_capturar = threading.Thread(target=self.capturar)
        self.th_capturar.start()

        self.proceso = None
        self.pid = None

    def get_datos_capturadora(self):
        try:
            return DatosGrabadora.objects.all()[0]
        except IndexError:
            return False

    def crear_directorio_captura(self):
        try:
            capturadora = self.get_datos_capturadora()
            directorio = capturadora.directorio_de_grabacion
            ruta_directorio = f"{directorio}/Capturas_del_{self.dia}"
            if not os.path.exists(ruta_directorio):
                os.makedirs(ruta_directorio)
                os.chmod(ruta_directorio, 0o777)
        except Exception as e:
            logger.debug(f'ERROR AL CREAR DIRECTORIO DE CAPTURA - {e}')
            return False

    def pid_proceso(self):  # saco el ID del proceso de ffmpeg que está ocupando la placa DeckLink
        comando = os.popen("ps aux | grep ffmpeg | grep DeckLink").read()
        lista_comando = comando.split()
        self.pid = lista_comando[1]
        if "decklink" in lista_comando:
            logger.debug(f'PID - {self.pid}')
            return self.pid
        else:
            logger.debug(f'PID - False')
            return False

    def para_capturar(self, nueva_captura):
        self.nueva_captura = nueva_captura
        self.capturarlo = True
        logger.debug(f"PARA_CAPTURAR {nueva_captura}")

    def capturar(self):
        while True:
            time.sleep(.5)
            if self.capturarlo:
                self.crear_directorio_captura()
                capturadora = self.get_datos_capturadora()
                self.capturarlo = False
                capturando = self.pid_proceso()
                hora_arg = datetime.now()
                hora = str(hora_arg.hour) + "h" + str(hora_arg.minute) + "m"
                try:
                    if not capturando:
                        titulo_pos = f'{self.nueva_captura.titulo.upper()}_{hora}'
                        titulo = re.sub(r'[/. ,]', '_', titulo_pos)
                        placa = capturadora.placa
                        formato = capturadora.formato
                        direccion = capturadora.directorio_de_grabacion
                        tipo = self.nueva_captura.tipo_grabacion
                        if tipo == 1:
                            os.system(f"utils/rec.sh {titulo} {placa} {formato} {direccion}")
                        elif tipo == 2:
                            segmento = self.segmento
                            os.system(f"utils/rec_secuencial.sh {titulo} {segmento} {placa} {formato} {direccion}")
                    else:
                        return False
                except AttributeError as e:
                    logger.debug(f"ERROR EN CAPTURAR() - {e}")
            else:
                pass

    def stop(self):  # Finaliza la captura matando el proceso identificado en pid_proceso
        pid = self.pid_proceso()
        if pid:
            os.system(f"kill {pid}")
            os.system(f"rm /tmp/datos")
