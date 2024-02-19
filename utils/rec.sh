#!/bin/bash
exten="_cap.mp4"
d=$(date +"%d-%m-%Y")
dh=$(date +"%d-%m-%Y_%H%M%S")

if [ -z "$1" ]; then
    echo "Error: Debe proporcionar el nombre del archivo de video como argumento."
    exit 1
else
    s="$1"
fi

if [ ! "$s" ]; then
    n="$4/Captura_"$d"/"$dh"_cap.mp4"
else
    n="$4/Captura_"$d"/"$s"_cap.mp4"
fi

/opt/ffmpeg/bin/ffmpeg -vsync passthrough -r 25 -f decklink -i "$2"@"$3" \
 -pix_fmt yuv420p \
 -crf 20 \
 -b:a 256k \
 -g 25 \
 -flags +ildct+ilme -top 1 \
 -x264opts tff \
 -profile:v main -level 4.0 \
 -preset ultrafast \
 -vstats_file /tmp/datos \
 -y \
 "$n"

