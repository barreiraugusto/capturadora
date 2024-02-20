import re
from datetime import datetime, timedelta

from django.http import JsonResponse

from .datos_temp import modificar_dato, obtener_dato

def get_tiempo(archivo):
    try:
        with open('/tmp/datos', 'r') as file:
            lineas = file.readlines()
            ultima_linea = lineas[-1]
            patron = r'time= (\d+\.\d+)'
            coincidencia = re.search(patron, ultima_linea)
            if coincidencia:
                segundos = coincidencia.group(1)
                horas = float(segundos) // 3600
                minutos = (float(segundos) % 3600) // 60
                segundos = float(segundos) % 60
                tiempo = f"{int(horas):02}:{int(minutos):02}:{int(segundos):02}"
                modificar_dato("/tmp/grabacion_actual", "duracion", tiempo)
            else:
                tiempo_guardado = obtener_dato("/tmp/grabacion_actual", "duracion")
                tiempo_dt = datetime.strptime(tiempo_guardado, "%H:%M:%S")
                tiempo_dt += timedelta(seconds=1)
                modificar_dato("/tmp/grabacion_actual", "duracion", tiempo_dt)
                tiempo = tiempo_dt.strftime("%H:%M:%S")
    except FileNotFoundError as e:
        tiempo = "00:00:00"
    return JsonResponse({'tiempos': tiempo})


if __name__ == '__main__':
    pass
    # get_tiempo(os.path.join(BASE_DIR.parent, 'temp.txt'))
