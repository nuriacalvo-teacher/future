# Carpeta de audio del vídeo

La narración grabada de `video/index.html`: 64 clips MP3 (24 kHz, mono) y
`manifest.json`, que guarda el fichero, la duración y **el texto** de cada clip.

La página busca `manifest.json` al arrancar. **Si esta carpeta está vacía no
pasa nada**: se usa la voz del navegador.

Se graba desde la pestaña **Actions** → *Grabar la narración del vídeo* →
**Run workflow**, o con doble clic en `tools/GRABAR-AUDIOS.command`.
Ver `tools/README.md`.
