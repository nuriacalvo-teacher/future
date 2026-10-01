#!/bin/bash
#
#  Escuchar las voces antes de grabar  ·  para Mac
#
#  Haz DOBLE CLIC en este archivo desde el Finder.
#
#  Graba unas frases del video con las voces elegidas (narradora, quiz y
#  castellano), para oirlas antes. Tarda menos de un minuto y no
#  cambia nada de las paginas: si no te convencen, no has perdido nada.
#

set -u
cd "$(dirname "$0")/.." || exit 1
. "tools/_entorno.sh"

echo "======================================================"
echo "   Muestra de las voces del video"
echo "======================================================"
echo

preparar_entorno || exit 1

echo
".venv-audio/bin/python" tools/build_video.py --demo
ESTADO=$?

if [ $ESTADO -ne 0 ]; then
  echo
  echo "No he podido grabar la muestra. Los mensajes de arriba dicen por que."
  pausa
  exit $ESTADO
fi

echo
if [ -f video/audio/muestra-voces.mp3 ]; then
  echo "Abriendo la muestra..."
  open video/audio/muestra-voces.mp3 2>/dev/null || open -R video/audio/muestra-voces.mp3 2>/dev/null || true
  echo
  echo "Si te convencen, cierra esto y haz doble clic en GRABAR-AUDIOS.command"
  echo "para grabar el video entero."
fi
pausa
