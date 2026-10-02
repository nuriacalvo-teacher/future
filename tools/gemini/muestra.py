#!/usr/bin/env python3
"""Muestra de narracion con las voces de Gemini (las de NotebookLM).

Graba el capitulo 1 de dos maneras, con varias parejas de voces:

  A · una sola narradora, el guion de siempre pero con intencion en cada frase
  B · profesora + alumno, en dialogo

y deja un MP3 por pareja en tools/gemini/salida/ para escucharlos y elegir.

Necesita la clave GEMINI_API_KEY (secreto del repositorio). No usa librerias
externas; para pasar el audio a MP3 usa ffmpeg.
"""

import base64
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "salida")
API = "https://generativelanguage.googleapis.com/v1beta"
KEY = os.environ.get("GEMINI_API_KEY", "").strip()

MODEL = "gemini-3.8-flash-tts"
LEGACY_MODEL = "gemini-2.5-flash-preview-tts"     # plan B si el modelo nuevo falla

# Parejas de voces (profesora, alumno). Si la biblioteca ampliada devuelve
# voces britanicas, se usan primero; estas son las de reserva.
PAIRS = [
    ("Sulafat", "Puck"),      # calida / animado
    ("Kore", "Leda"),         # firme / juvenil
    ("Aoede", "Fenrir"),      # desenfadada / entusiasta
]
BRITISH = "Speak with a natural British English accent (Southern England). "

# ---------------------------------------------------------------------------
# Guion del capitulo 1
# ---------------------------------------------------------------------------
# A: el texto actual de la pagina, frase a frase, con una intencion.
NARRADORA = [
    ("Chapter one: will.", "bright, enthusiastic, announcing a new chapter"),
    ("The form is easy: will, plus the infinitive without to. It's the same for every person. "
     "In the negative, we say won't.", "clear, reassuring teacher, stressing the key words"),
    ("We use will for predictions and opinions, especially after I think, I'm sure, or probably. "
     "I think it will rain tomorrow.", "engaging teacher; the example sentence acted out naturally"),
    ("We also use it for decisions we make at the moment of speaking. The phone's ringing! "
     "Don't worry, I'll answer it.", "lively; act out the example with real surprise"),
    ("And for offers and promises. That bag looks heavy. I'll carry it for you. "
     "I promise I won't tell anyone.", "warm and kind"),
    ("Careful! Never say: I will to go, or: she will goes. Just say: she will go.",
     "playfully serious warning, then encouraging"),
]

# B: profesora (T) y alumno (S).
DIALOGO = [
    ("T", "Chapter one: will!", "bright, enthusiastic, announcing a new chapter"),
    ("T", "The form is easy: will, plus the infinitive without to. It's the same for every person.",
     "clear, reassuring teacher"),
    ("S", "So... I will, you will, she will?", "curious teenage student, checking"),
    ("T", "Exactly! And in the negative, we say won't.", "encouraging, pleased"),
    ("T", "We use will for predictions and opinions, especially after I think, I'm sure, or probably.",
     "engaging teacher"),
    ("S", "Hmm... I think it will rain tomorrow.", "thoughtful, trying it out"),
    ("T", "Perfect!", "delighted"),
    ("T", "We also use it for decisions we make at the moment of speaking.", "engaging teacher"),
    ("S", "Oh! The phone's ringing!", "surprised, acting a little scene"),
    ("T", "Don't worry, I'll answer it!", "quick and helpful, acting the scene"),
    ("T", "And for offers and promises.", "warm"),
    ("S", "Ugh, this bag looks really heavy...", "struggling, a bit tired"),
    ("T", "I'll carry it for you. And I promise I won't tell anyone!", "kind, a little playful"),
    ("S", "Got it! So... she will goes?", "confident but making a mistake"),
    ("T", "Careful! Never say: she will goes, or: I will to go. Just say: she will go.",
     "playfully alarmed, then clear and encouraging"),
    ("S", "She will go. Easy!", "cheerful, proud"),
]


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
def call(method, path, body=None, params=None, tries=5):
    url = API + path
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    data = json.dumps(body).encode() if body is not None else None
    for n in range(tries):
        req = urllib.request.Request(url, data=data, method=method, headers={
            "x-goog-api-key": KEY, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:800]
            if e.code in (429, 500, 503) and n < tries - 1:
                wait = 20 * (n + 1)
                print("    (%d, reintento en %d s) %s" % (e.code, wait, msg[:200]))
                time.sleep(wait)
                continue
            raise RuntimeError("HTTP %d en %s: %s" % (e.code, path, msg))
    raise RuntimeError("sin respuesta")


def find_audio(obj):
    """Devuelve el ultimo bloque de audio (base64) de la respuesta, venga en el
    formato nuevo ({type: audio, data}) o en el antiguo (inlineData)."""
    found = []

    def walk(o):
        if isinstance(o, dict):
            if o.get("type") == "audio" and isinstance(o.get("data"), str):
                found.append(o["data"])
            inl = o.get("inlineData") or o.get("inline_data")
            if isinstance(inl, dict) and isinstance(inl.get("data"), str):
                found.append(inl["data"])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(obj)
    if not found:
        raise RuntimeError("la respuesta no trae audio: %s" % json.dumps(obj)[:600])
    return base64.b64decode(found[-1])


# ---------------------------------------------------------------------------
# Voces britanicas de la biblioteca ampliada (si existe)
# ---------------------------------------------------------------------------
def british_voices():
    try:
        r = call("GET", "/voices", params={"language_code": "en-GB", "accent": "British",
                                            "page_size": 200}, tries=2)
    except Exception as e:                                   # noqa: BLE001
        print("  No se ha podido consultar la biblioteca de voces: %s" % str(e)[:300])
        return []
    voices = r.get("voices") or r.get("items") or []
    print("  Voces britanicas en la biblioteca: %d" % len(voices))
    for v in voices[:40]:
        print("   ", json.dumps(v, ensure_ascii=False)[:300])
    return voices


def voice_id(v):
    for k in ("voice", "voice_id", "voiceId", "id", "name"):
        if isinstance(v.get(k), str):
            return v[k].split("/")[-1]
    return None


def pick_pairs(voices):
    fem = [v for v in voices if str(v.get("gender", "")).lower() == "female"]
    mal = [v for v in voices if str(v.get("gender", "")).lower() == "male"]
    pairs = []
    for f, m in zip(fem, mal):
        a, b = voice_id(f), voice_id(m)
        if a and b:
            pairs.append((a, b))
        if len(pairs) == 2:
            break
    return pairs


# ---------------------------------------------------------------------------
# Sintesis
# ---------------------------------------------------------------------------
def synth_new(turns, voices, british):
    """turns: [(speaker, texto, estilo)]; voices: {speaker: voz}."""
    content = []
    for who, text, style in turns:
        meta = {"type": "speech_metadata", "style": (BRITISH if british else "") + style}
        if len(voices) > 1:
            meta["speaker"] = who
        content.append({"type": "text", "text": text, "annotations": [meta]})
    if len(voices) > 1:
        cfg = {"mode": "conversational",
               "speakers": [{"speaker": s, "voice": v} for s, v in voices.items()]}
    else:
        cfg = [{"voice": list(voices.values())[0]}]
    body = {"model": MODEL,
            "input": [{"type": "user_input", "content": content}],
            "response_format": {"type": "audio"},
            "generation_config": {"speech_config": cfg}}
    return find_audio(call("POST", "/interactions", body))


def synth_legacy(turns, voices, british):
    names = {"T": "Teacher", "S": "Student"}
    lines = []
    for who, text, style in turns:
        tag = names.get(who, "Teacher") if len(voices) > 1 else "Narrator"
        lines.append("%s (%s): %s" % (tag, style, text))
    head = ("Read this English lesson for teenage students of English. "
            + (BRITISH if british else "")
            + "Follow the delivery notes in brackets, but do not read them aloud.\n\n")
    if len(voices) > 1:
        speech = {"multiSpeakerVoiceConfig": {"speakerVoiceConfigs": [
            {"speaker": names[s], "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": v}}}
            for s, v in voices.items()]}}
    else:
        speech = {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": list(voices.values())[0]}}}
    body = {"contents": [{"parts": [{"text": head + "\n".join(lines)}]}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": speech}}
    return find_audio(call("POST", "/models/%s:generateContent" % LEGACY_MODEL, body))


STATE = {"legacy": False}


def synth(turns, voices, british):
    if not STATE["legacy"]:
        try:
            return synth_new(turns, voices, british)
        except Exception as e:                               # noqa: BLE001
            print("  El modelo %s ha fallado (%s). Pruebo con %s." % (MODEL, str(e)[:400], LEGACY_MODEL))
            STATE["legacy"] = True
    return synth_legacy(turns, voices, british)


def to_mp3(audio, dest):
    """El audio llega como WAV o como PCM 24 kHz 16 bit mono sin cabecera."""
    raw = dest + ".in"
    with open(raw, "wb") as fh:
        fh.write(audio)
    fmt = [] if audio[:4] == b"RIFF" else ["-f", "s16le", "-ar", "24000", "-ac", "1"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + fmt + ["-i", raw,
                    "-ar", "24000", "-ac", "1", "-b:a", "64k", dest], check=True)
    os.remove(raw)


def say_label(text, voice):
    return synth([("T", text, "neutral, short announcement")], {"T": voice}, True)


def main():
    if not KEY:
        sys.exit("Falta la clave GEMINI_API_KEY.")
    os.makedirs(OUT, exist_ok=True)
    pairs = pick_pairs(british_voices())
    british = []
    for p in pairs:
        british.append((p, False))           # ya son britanicas: no hace falta pedir acento
    for p in PAIRS:
        british.append((p, True))
    todo = british[:3]
    print("  Parejas: %s" % ", ".join("%s+%s" % p for p, _ in todo))

    resumen = []
    for n, ((prof, alum), pedir_acento) in enumerate(todo, 1):
        nombre = "%d-%s-y-%s" % (n, prof, alum)
        print("[%d/%d] %s" % (n, len(todo), nombre))
        piezas = []
        try:
            piezas.append(say_label("Version A. One narrator.", prof))
            piezas.append(synth([("T", t, s) for t, s in NARRADORA], {"T": prof}, pedir_acento))
            piezas.append(say_label("Version B. Teacher and student.", prof))
            piezas.append(synth(DIALOGO, {"T": prof, "S": alum}, pedir_acento))
        except Exception as e:                               # noqa: BLE001
            print("  ERROR: %s" % str(e)[:800])
            continue
        partes = []
        for k, p in enumerate(piezas):
            f = os.path.join(OUT, "%s-%d.mp3" % (nombre, k))
            to_mp3(p, f)
            partes.append(f)
        lista = os.path.join(OUT, "lista.txt")
        silencio = os.path.join(OUT, "silencio.mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                        "anullsrc=r=24000:cl=mono", "-t", "1.2", "-b:a", "64k", silencio], check=True)
        with open(lista, "w") as fh:
            for f in partes:
                fh.write("file '%s'\nfile '%s'\n" % (f, silencio))
        final = os.path.join(OUT, nombre + ".mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                        "-i", lista, "-c", "copy", final], check=True)
        for f in partes + [lista, silencio]:
            os.remove(f)
        resumen.append(nombre)
        print("  -> %s" % final)
        time.sleep(5)
    if not resumen:
        sys.exit("No se ha podido grabar ninguna muestra. Mira los mensajes de arriba.")
    print("\nModelo usado: %s" % (LEGACY_MODEL if STATE["legacy"] else MODEL))
    with open(os.path.join(OUT, "LEEME.txt"), "w") as fh:
        fh.write("Cada MP3 es una pareja de voces (profesora y alumno).\n"
                 "Primero la version A (una narradora) y luego la B (profesora + alumno).\n\n"
                 + "\n".join(resumen) + "\n")


if __name__ == "__main__":
    main()
