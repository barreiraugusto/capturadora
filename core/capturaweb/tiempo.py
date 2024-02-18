import re

from django.http import JsonResponse


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
            else:
                tiempo = "00:00:00"
    except FileNotFoundError as e:
        tiempo = "00:00:00"
    return JsonResponse({'tiempos': tiempo})


if __name__ == '__main__':
    pass
    # get_tiempo(os.path.join(BASE_DIR.parent, 'temp.txt'))
