import subprocess
import threading
import time
from datetime import date, datetime

from core.capturaweb.models import DatosGrabadora


class Convertir:
    def __init__(self):
        self.ahora = datetime.now()
        self.hoy = date.today()
        self.hora = self.ahora.strftime("%H-%M-%S")
        self.dia = self.hoy.strftime("%d-%m-%Y")
        self.start = False
        self.archivo = "Nada"
        self.th_convertir = threading.Thread(target=self.convertir)
        self.th_convertir.start()

    def get_datos_capturadora(self):
        try:
            return DatosGrabadora.objects.all()[0]
        except IndexError:
            return False

    def para_convertir(self, archivo):
        self.archivo = archivo
        self.start = True

    def convertir(self):
        while True:
            time.sleep(.5)
            if self.start:
                self.start = False
                try:
                    self.ejecutar_ffmpeg()
                except Exception as e:
                    print(f"Error al convertir: {str(e)}")

    def ejecutar_ffmpeg(self):
        capturadora = self.get_datos_capturadora()
        input_file = f"{capturadora.directorio_de_grabacion}/Capturas_del_{self.dia}/{self.archivo}_cap.mp4"
        output_file = f"{capturadora.directorio_de_grabacion}/Capturas_del_{self.dia}/{self.archivo}_720_cap.mp4"

        ffmpeg_command = [
            "/opt/ffmpeg/bin/ffmpeg",
            "-loglevel", "error",
            "-i", input_file,
            "-b", "1000000",
            "-s", "1280x720",
            "-filter:v", "yadif=1",
            "-r", "25",
            "-profile:v", "main",
            "-pix_fmt", "yuv420p",
            "-n", output_file
        ]

        subprocess.run(ffmpeg_command, check=True)


if __name__ == '__main__':
    Convertir()
