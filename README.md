# Future Tenses · EnglishPRO

App de práctica de los futuros en inglés (ESO / Bachillerato), con el mismo motor que [present-tenses](https://github.com/nuriacalvo-teacher/present-tenses) y [past-tenses](https://github.com/nuriacalvo-teacher/past-tenses).

**7 módulos × 3 niveles, con 10 ejercicios por nivel:**

1. Future with Will
2. Be Going To
3. Will vs Be Going To
4. Future Continuous (will be doing)
5. Future Perfect (will have done)
6. Present Tenses for the Future (horarios, planes acordados y presente tras *when / as soon as / until / if*)
7. Future Review

- **Level 1:** opción múltiple (hace falta un 90 % para aprobar)
- **Level 2:** rellenar huecos (80 %)
- **Level 3:** traducción del español al inglés (80 %)

Cada nivel empieza con la explicación del módulo. Los alumnos pueden entrar con su cuenta de Google y el código de clase, o como invitados (en ese caso no se guarda nada).

## Corrección de las traducciones

Se aceptan todas las respuestas correctas, no solo la del modelo:
- sinónimos (phone/mobile, film/movie, exam/test, match/game…)
- contracciones (I'll = I will, won't = will not…)
- el orden de las palabras
- otros futuros que también sean correctos en esa frase (*I'm meeting* o *I'm going to meet* para un plan acordado)
- *he* o *she* cuando la frase en español no lleva sujeto

Dentro de una respuesta, `[a|b]` significa "vale a o b" y `[a|]` que la palabra es opcional.

## ⚠️ Firebase: hay que hacer una cosa una sola vez

Esta app guarda los resultados en su propio nodo, **`future_tenses_v1`**.

En la consola de Firebase (proyecto *goya-english*): Realtime Database → **Reglas**. Duplica el bloque de `present_tenses_v2`, cambia el nombre a `future_tenses_v1` y publica.

Hasta que no lo hagas, el modo invitado funciona, pero la entrada con código de clase mostrará "Wrong class code".

## Publicarla

Settings → Pages → Deploy from a branch → `main` / root.
