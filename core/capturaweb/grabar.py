import os
import subprocess
import threading
import time
from datetime import date
from datetime import datetime


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

    def crear_directorio_captura(self):
        ruta_directorio = f"/media/video/Captura_{self.dia}"
        if not os.path.exists(ruta_directorio):
            os.makedirs(ruta_directorio)
            os.chmod(ruta_directorio, 0o777)
            os.makedirs(f"{ruta_directorio}/OV")
            os.chmod(f"{ruta_directorio}/OV", 0o777)

    def pid_proceso(self):  # saco el ID del proceso de ffmpeg que esta ocupando la placa DeckLink
        # comando = os.popen("ps aux | grep ffmpeg | grep DeckLink").read()
        script = "gen_tiempo.sh"
        try:
            self.pid = int(subprocess.check_output(["pgrep", "-f", script]))
            print(self.pid)
            return self.pid
        except subprocess.CalledProcessError:
        # resultado = os.popen("ps aux | grep get_tiempo | grep /bin/bash").read()
        # lista_comando = resultado.split()
        # print(f'Lista ==== {lista_comando}')
        # self.pid = lista_comando[1]
        # if "decklink" in lista_comando:
        # if "gen_tiempo" in lista_comando:
        #     return self.pid
        # else:
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
        self.proceso = subprocess.Popen(['/home/augusto/Documentos/CODIGOS/gen_tiempo.sh'])
        # self.capturarlo = True

    def para_captura_segmentada(self, nombre, segmento=10):
        self.segmento = segmento
        self.nombre = nombre
        self.capturarlo_seg = True

    def capturar(self):  # Inicia captura
        while True:
            time.sleep(.5)
            if self.capturarlo:
                self.capturarlo = False
                capturando = self.en_proceso()
                try:
                    if not capturando:
                        os.system(f"/opt/ffmpeg/bin/ffmpeg -vsync passthrough -r 25 -f decklink -i 'DeckLink SDI 4K@8'\
                                 -pix_fmt yuv420p\
                                 -crf 20\
                                 -b:a 256k\
                                 -g 25\
                                 -flags +ildct+ilme -top 1\
                                 -x264opts tff\
                                 -profile:v main -level 4.0\
                                 -preset ultrafast\
                                 -y\
                                 '/media/video/Captura_{self.dia}/{self.nombre}_cap.mp4'")
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
                self.capturarlo_seg = False
                segmento_min = round(int(self.segmento) / 0.016666667)
                capturando = self.en_proceso()
                try:
                    if not capturando:
                        hora = get_hora()
                        os.system(f"/opt/ffmpeg/bin/ffmpeg -vsync passthrough -r 25 -f decklink -i 'DeckLink SDI 4K@8'\
        						-strict -2 \
        						-vcodec libx264 \
        						-crf 20 \
        						-pix_fmt yuv420p \
        						-tune fastdecode \
        						-preset ultrafast \
        						-g 25 \
        						-flags +ildct+ilme -top 1 \
        						-x264opts tff \
        						-b:a 256k \
        						-f segment \
        						-reset_timestamps 1 \
        						-segment_time {segmento_min} \
        						'/media/video/Captura_{self.dia}/%04d_{self.nombre}-{self.dia}-{hora}_cap.mp4'")
                    else:
                        return False
                except AttributeError:
                    pass
            else:
                pass

    def stop(self):  # Finaliza la captura matando el proceso identificado en pid_proceso
        # print('stop')
        # capturando = self.en_proceso()
        pid = self.pid_proceso()
        # if capturando:
        os.system(f"kill {pid}")
        os.system(f" rm /home/augusto/Documentos/CODIGOS/CAPTURADORA/capturadora/cuenta.txt")
