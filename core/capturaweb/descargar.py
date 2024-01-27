import yt_dlp
import re

url = input("Ingresa la URL del video en YouTube: ")

opcion = input("\nVideo y audio: V\nSolo audio: A\n")

while not re.match(r'^[VvAa]$', opcion):
    print("La opción seleccionada no es válida.\n")
    opcion = input("Video y audio: V\nSolo audio: A\n")



URLS = [url]

if opcion == "V" or "v":
    ydl_opts = {'format': 'bestvideo*+bestaudio/best',}
elif opcion == "A" or "a":
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URLS)
