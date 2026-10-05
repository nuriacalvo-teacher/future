# Prompt para crear un vídeo-lección nuevo a partir de otra app

Copia el texto de abajo en un chat nuevo de Claude Code, cambiando lo que va
entre corchetes. La sesión necesita acceso a los dos repositorios
(`nuriacalvo-teacher/future` y el de la app nueva) y el secreto
`GEMINI_API_KEY` guardado en el repositorio de la app nueva
(Settings → Secrets and variables → Actions).

---

```
Quiero un vídeo-lección narrado para mi app de gramática inglesa
[NOMBRE], en el repositorio nuriacalvo-teacher/[REPO], igual que el de
referencia: https://nuriacalvo-teacher.github.io/future/video/
(código en nuriacalvo-teacher/future, carpetas video/ y tools/).
Contenido y ejercicios: los de la app [REPO] (index.html o lo que
corresponda). Tema: [TEMA, p. ej. "past simple vs present perfect"].
Alumnos de ESO y Bachillerato; yo soy la profesora (Nuria Calvo, IES Goya,
Zaragoza).

Hazlo directamente, sin muestras previas ni preguntas, salvo que algo sea
imposible. Ahorra tokens: no investigues lo que ya está resuelto en future,
no leas ficheros enteros si no hace falta y respóndeme en español, breve.

1. PLANTILLA. Copia de future a [REPO]: video/index.html (como plantilla),
   tools/build_video.py, tools/gemini/grabar.py, tools/README.md,
   .github/workflows/grabar-gemini.yml y .gitignore (las líneas de audio).
   Lee primero tools/README.md de future: explica el formato del guion y
   cómo se graba. No copies los MP3 de future.

2. GUION. Escribe el guion nuevo en el bloque var LESSON de
   video/index.html:
   - Diálogo profesora + alumno ("Texto" = profesora, "S: Texto" = alumno,
     "[estilo] Texto" = cómo decirlo). El alumno pregunta, prueba ejemplos
     y comete los errores típicos del tema; la profesora le corrige.
     Profesora enérgica y firme, nunca adormilada.
   - Capítulo de introducción (con los créditos de la profesora), un
     capítulo por cada punto gramatical de la app, uno de errores típicos,
     el aviso del quiz y el cierre que manda a practicar con los
     ejercicios de la app.
   - Quiz de 6 preguntas sacadas de los ejercicios de la app. Comprueba
     que before + opción + after forma una frase con sentido para LAS TRES
     opciones (en future la opción "rains" con after " rain." formaba
     "It rains rain").
   - Rehaz el HTML de cada escena (los data-b de las animaciones) con el
     contenido nuevo, manteniendo el diseño, colores y tipografía de
     future. LABELS, QUIZ_SCENE y LAST tienen que cuadrar con las escenas.
   - Cambia los enlaces a nuriacalvo-teacher.github.io/future/ (botón
     "Exercises" y botón final de practicar) por los de la app nueva.

3. VOCES. Quiero acento británico si es posible. En future se usó
   Kore (profesora) + Puck (alumno) con "British accent" en el estilo,
   y sonaron americanas. Antes de grabar, haz UNA llamada barata (no de
   síntesis) a GET https://generativelanguage.googleapis.com/v1beta/voices
   desde un workflow con la clave, probando los filtros language_code=en-GB
   y accent=British, e imprime la respuesta cruda en el log (en future
   devolvió 0 voces: puede que el filtro o el nombre del campo fueran
   otros). Si hay voces británicas, elige una mujer adulta para la
   profesora y un chico joven para el alumno y ponlas en VOZ_PROFESORA y
   VOZ_ALUMNO de grabar.py. Si no hay, usa Kore + Puck sin preguntarme.

4. GRABACIÓN. Con el workflow "Grabar la narracion con Gemini" (cuota
   gratuita: 10 peticiones al día y 3 por minuto). Ajusta GRUPOS en
   grabar.py para no pasar de 10 grupos: un capítulo por grupo, juntando
   los cortos; el quiz en un grupo y las respuestas del alumno en otro.
   El programa ya corta con Whisper, comprueba palabra por palabra, exige
   exactitud en las respuestas del quiz (Gemini corrige los errores
   deliberados) y repite al día siguiente solo lo que falla. Si se acaba la
   cuota, programa con send_later la continuación para el día siguiente a
   las 07:20 UTC.

5. COMPROBACIÓN, sin gastar cuota:
   - Que la página y grabar.py generan los mismos textos para todos los
     clips (en future se hizo con un script de node que extrae allClips()
     de la página y lo compara con clips_del_grupo de grabar.py).
   - Antes de grabar con Gemini, una pasada completa con edge-tts en lugar
     de Gemini para probar el corte.
   - Tras grabar: transcribir todos los clips (Whisper medium.en para los
     dudosos) y revisar los errores deliberados palabra por palabra.
   - Reproducir el vídeo entero en Chromium (Playwright, playbackRate alto)
     respondiendo el quiz con aciertos y fallos, sin errores de JavaScript.

6. ENTREGA. Trabaja en una rama, y al terminar pásame un montaje corto
   (un capítulo + una pregunta del quiz con fallo) para escucharlo. Si
   doy el visto bueno, abre la pull request a main.
```
