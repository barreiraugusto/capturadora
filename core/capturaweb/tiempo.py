import os
import re

from config.settings import BASE_DIR


def get_tiempo(archivo):
    with open(archivo, 'r') as file:
        lineas = file.readlines()
        ultima_linea = lineas[-1]
        patron = r'time= (\d+\.\d+)'
        coincidencia = re.search(patron, ultima_linea)
        if coincidencia:
            return coincidencia.group(1)
        else:
            return None

    # with open(archivo, 'r') as registro:
    #     tiempos = []
    #     for linea in registro:
    #         match = re.search(r'time= (\d+\.\d+)', linea)
    #         if match:
    #             if match:
    #                 time_value = match.group(1)
    #                 tiempos.append(time_value)
    #             return tiempos


if __name__ == '__main__':
    get_tiempo(os.path.join(BASE_DIR.parent, 'temp.txt'))
