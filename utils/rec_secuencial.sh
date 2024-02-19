#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Error: Debe proporcionar el nombre del archivo de video como primer argumento y el tiempo de segmentación en milisegundos como segundo argumento."
    exit 1
fi

s="${1// /_}"
tiempo="$2"

directorio="/media/video/Captura_$(date +"%d-%m-%Y")"

mkdir -p "$directorio"

if [ -z "$s" ]; then
    n="$directorio/%04d_$(date +"%d-%m-%Y_%H%M%S")_cap.mp4"
else
    n="$directorio/$s/%04d_${s}_$(date +"%H%M%S")_cap.mp4"
    mkdir -p "$directorio/$s"
fi

/opt/ffmpeg/bin/ffmpeg -vsync passthrough -r 25 -f decklink -i "$3"@"$4" \
 -pix_fmt yuv420p \
 -crf 20 \
 -b:a 256k \
 -g 25 \
 -flags +ildct+ilme -top 1 \
 -x264opts tff \
 -profile:v main -level 4.0 \
 -preset ultrafast \
 -f segment \
 -reset_timestamps 1 \
 -segment_time "$tiempo" \
 -y \
 "$n" \
 -vstats_file /tmp/datos
