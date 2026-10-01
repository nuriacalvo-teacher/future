# Narración del vídeo-lección

El vídeo-lección está en `video/index.html` y se abre en
**https://nuriacalvo-teacher.github.io/future/video/**.

## El problema

Si el vídeo se narra con la voz del propio navegador, suena distinto en cada
aparato:

| Dispositivo | Qué voz sale de fábrica | Cómo suena |
|---|---|---|
| Mac con Chrome o Edge | voces de Google / Microsoft | bien |
| Mac con Safari | voz **compacta** de Apple | metálica |
| iPhone / iPad | voz **compacta** de Apple | metálica |
| Android | Google TTS | bien |
| Windows | voces de Microsoft | de correcto a muy bien |
| Linux / Vitalinux | normalmente **ninguna** | no narra |

Con la narración **grabada** suena igual en todas partes. La voz del navegador
queda solo como respaldo.

## Qué hay ya grabado

`video/audio/` tiene **64 clips MP3** (24 kHz, mono, unos 7 minutos en total) y
`manifest.json`:

- `s0_0.mp3` … `s9_2.mp3`: cada frase de cada capítulo (voz **Sonia**).
- `q0.mp3` … `q5.mp3`: las preguntas del quiz (voz **Ryan**).
- `q0_ok.mp3`, `q0_no.mp3`…: lo que dice al acertar o fallar cada pregunta.
- En las dos frases que mencionan **"IES Goya, Zaragoza"**, ese trozo lo dice
  **Elvira** (voz española), para que se pronuncie bien.
- `manifest.json`: índice con el fichero, la duración y **el texto** de cada
  clip, y las voces usadas.

**No hace falta grabar nada para usar el vídeo.** Esto es solo para cuando
cambies el guion o las voces.

## Si cambias el guion

Las frases están en `video/index.html`, en el bloque `var LESSON = { … }`
(cerca del final). `scenes` son los capítulos, frase a frase; `quiz` son las
preguntas.

El índice guarda **el texto de cada clip**. Si cambias una frase y no vuelves
a grabar, esa frase nota que su grabación ya no corresponde y se dice con la
voz del navegador, en vez de decir algo que ya no toca. Las demás siguen con
su grabación.

Para ponerla al día, vuelve a grabar (ver abajo): **solo se rehacen los clips
que han cambiado**.

## Elegir otras voces

### 1 · Comparar todas las voces

- **Online:** pestaña **Actions** → *Grabar la narración del vídeo* →
  **Run workflow**, marcando **comparativa** → **Run workflow**. Cuando
  termine (un par de minutos), entra en la ejecución y descarga
  *voces-para-escuchar* (abajo del todo).
- **En el Mac:** doble clic en `tools/COMPARAR-VOCES.command`.

Es un MP3 en el que todas las voces británicas e irlandesas leen la misma
frase, cada una diciendo antes su nombre.

### 2 · Escribir tu elección

En `tools/voces.txt`:

```
voz_narradora = en-GB-SoniaNeural     # explica la lección
voz_quiz      = en-GB-RyanNeural      # lee las preguntas del quiz
voz_es        = es-ES-ElviraNeural    # dice "IES Goya, Zaragoza"
```

Si te equivocas escribiendo un nombre, el programa avisa antes de grabar y te
lista las válidas.

### 3 · Oír tu elección antes de grabarlo todo

**Run workflow** marcando **muestra**, o doble clic en
`tools/ESCUCHAR-VOCES.command`. Graba unas pocas frases. No toca la página.

## Cómo grabar

### Opción A · online, sin instalar nada

1. Pestaña **Actions** del repositorio.
2. A la izquierda, *Grabar la narración del vídeo*.
3. Botón **Run workflow** → otra vez **Run workflow** (sin marcar nada).
4. Tarda unos cinco minutos y sube los audios él solo.

> **Solo la primera vez**, si falla al subir: **Settings → Actions → General →
> Workflow permissions → Read and write permissions → Save**.

### Opción B · en el Mac, con doble clic

**Code** → **Download ZIP**, descomprimir y doble clic en
`tools/GRABAR-AUDIOS.command`. Si macOS lo bloquea: **Ajustes del Sistema →
Privacidad y seguridad → Abrir igualmente**.

### Opción C · desde el terminal

```bash
python3 -m venv .venv-audio
.venv-audio/bin/pip install edge-tts
.venv-audio/bin/python tools/build_video.py
git add video/audio && git commit -m "Narración grabada" && git push
```

Opciones: `--force` (regrabar todo), `--only s1_2 q0` (solo esos clips),
`--demo`, `--audition`, `--list-voices`.

## Qué hace la página con la voz del navegador (respaldo)

Solo se usa si no hay grabación, o para una frase cuyo texto ha cambiado. Con
las mismas reglas que BRIT, `battles` y `ad`:

- Las voces se identifican por **voiceURI**, nunca por el nombre (en iOS la
  compacta y la mejorada se llaman las dos "Daniel").
- Las voces "de broma" de Apple se filtran también por voiceURI, porque en un
  Mac en español cambian de nombre ("Jester" → "Bufón").
- En Apple, velocidad **1.0** y el tono **sin tocar**.
- El truco de pause()+resume() cada 9 s es **solo** para Chrome de escritorio.
- Hay un selector de voz en la portada, que **desaparece** cuando hay
  grabación.
- Si no hay grabación ni ninguna voz instalada (Vitalinux), avisa y el vídeo
  sigue con los subtítulos. Con grabación, en Vitalinux suena normal.
- Sin `manifest.json`, todo funciona con la voz del navegador.
