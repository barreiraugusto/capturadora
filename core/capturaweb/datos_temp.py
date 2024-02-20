import json
import os


def guardar_datos(titulo, tipo, segmento, finalizada, convertir, duracion):
    video_data = {
        'titulo': titulo,
        'tipo': tipo,
        'segmento': str(segmento),
        'finalizada': finalizada,
        'convertir': convertir,
        'duracion': duracion.strftime('%H:%M:%S')
    }

    with open('/tmp/grabacion_actual', '+w') as temp_file:
        json.dump(video_data, temp_file, indent=2)
    video_file_path = temp_file.name
    return video_file_path



def obtener_dato(video_file_path, parametro):
    try:
        with open(video_file_path, 'r') as temp_file:
            video_data = json.load(temp_file)
            return video_data.get(parametro, None)
    except FileNotFoundError:
        return None


def modificar_dato(video_file_path, parametro, nuevo_valor):
    try:
        with open(video_file_path, 'r') as temp_file:
            video_data = json.load(temp_file)
        video_data[parametro] = nuevo_valor
        with open(video_file_path, 'w') as temp_file:
            json.dump(video_data, temp_file, indent=2)
        return True
    except FileNotFoundError:
        return False


def eliminar_datos(video_file_path):
    try:
        os.remove(video_file_path)
    except FileNotFoundError as error:
        print(error)
