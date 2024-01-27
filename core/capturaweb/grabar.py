import os
import threading
import time
from datetime import date
from datetime import datetime


class Captura:
    def __init__(self):
        self.ahora = datetime.now()
        self.hoy = date.today()
        self.nombre = "Nada"
        self.segmento = 10
        self.capturarlo = False
        self.capturarlo_seg = False
        self.hora = f"{self.ahora.hour}-{self.ahora.minute}-{self.ahora.second}"
        self.dia = f"{self.hoy.day}-{self.hoy.month}-{self.hoy.year}"
        self.esta = os.path.isdir(f"/media/video/Captura_{self.dia}")
        # self.pid = self.proceso.split()[1]
        if not self.esta:
            os.system(f"mkdir /media/video/Captura_{self.dia}")
            time.sleep(.5)
            os.system(f"chmod 777 /media/video/Captura_{self.dia}")
            time.sleep(1)
            os.system(f"mkdir /media/video/Captura_{self.dia}/OV")
            time.sleep(.5)
            os.system(f"chmod 777 /media/video/Captura_{self.dia}/OV")
        else:
            pass
        self.th_capturar = threading.Thread(target=self.capturar)
        self.th_capturar.start()

        self.th_capturar_segmentada = threading.Thread(target=self.captura_segmentada)
        self.th_capturar_segmentada.start()

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
                        self.hora = f"{self.ahora.hour}-{self.ahora.minute}-{self.ahora.second}"
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
                        self.hora = f"{self.ahora.hour}-{self.ahora.minute}-{self.ahora.second}"
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
        						'/media/video/Captura_{self.dia}/%04d_{self.nombre}-{self.dia}-{self.hora}_cap.mp4'")
                    else:
                        return False
                except AttributeError:
                    pass
            else:
                pass

    def stop(self):  # Finaliza la captura matando el proceso identificado en pid_proceso
        capturando = self.en_proceso()
        PID = self.pid_proceso()
        if capturando:
            os.system(f"kill {PID}")
