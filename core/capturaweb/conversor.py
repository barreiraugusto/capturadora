#!/usr/bin/ python
# coding=utf-8

import os
import time
import threading
from datetime import date
from datetime import datetime


class Convertir:
    def __init__(self):
        self.ahora = datetime.now()
        self.hoy = date.today()
        self.hora = "{}-{}-{}".format(self.ahora.hour, self.ahora.minute, self.ahora.second)#time.strftime("%H-%M-%S")
        self.dia = "{}-{}-{}".format(self.hoy.day, self.hoy.month, self.hoy.year)#time.strftime("%d-%m-%y")
        self.start = False
        self.archivo = "Nada"
        self.th_convertir = threading.Thread(target=self.convertir)
        self.th_convertir.start()

    def para_convertir(self, archivo):
        self.archivo = archivo
        self.start = True

    def convertir(self):
        while True:
            time.sleep(.5)
            if self.start:
                self.start = False
                print("Convirtiendo: {0}.mp4".format(self.archivo))
                os.system("/opt/ffmpeg/bin/ffmpeg -loglevel error\
                -i '/media/video/Captura_{1}/{2}_cap.mp4'\
                -b 1000000\
                -s 1280x720\
                -filter:v yadif=1\
                -r 25\
                -profile:v main\
                -pix_fmt yuv420p\
                -n '/media/video/Captura_{1}/{2}-{0}_720_cap.mp4'".format(self.hora, self.dia, self.archivo))#-{1}-{0}

    #def empezar(self):
     #   self.start = True


if __name__ == '__main__':
    Convertir()
