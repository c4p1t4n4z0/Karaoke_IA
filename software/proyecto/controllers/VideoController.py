import speech_recognition as sr
from deep_translator import GoogleTranslator
from pydub import AudioSegment
from moviepy.video.io.VideoFileClip import VideoFileClip
from gtts import gTTS
from langdetect import detect, DetectorFactory
import os
from pathlib import Path
import uuid

# Fijar el seed para la detección de idioma para obtener resultados reproducibles
DetectorFactory.seed = 0

TEMP_DIR = 'proyecto/views/static/archivostemporales/'
os.makedirs(TEMP_DIR, exist_ok=True)  # Crear el directorio si no existe

# Mapeo de idiomas compatible con googletrans (usando deep-translator)
LANGUAGES = {
    'es': 'spanish', 'en': 'english', 'fr': 'french', 'de': 'german', 'it': 'italian',
    'pt': 'portuguese', 'ru': 'russian', 'ja': 'japanese', 'ko': 'korean', 'zh': 'chinese',
    'ar': 'arabic', 'hi': 'hindi', 'tr': 'turkish', 'pl': 'polish', 'nl': 'dutch',
    'sv': 'swedish', 'no': 'norwegian', 'da': 'danish', 'fi': 'finnish', 'cs': 'czech',
    'ro': 'romanian', 'hu': 'hungarian', 'el': 'greek', 'he': 'hebrew', 'th': 'thai',
    'vi': 'vietnamese', 'id': 'indonesian', 'ms': 'malay', 'uk': 'ukrainian', 'bg': 'bulgarian',
    'hr': 'croatian', 'sk': 'slovak', 'sl': 'slovenian', 'sr': 'serbian', 'mk': 'macedonian',
    'sq': 'albanian', 'lt': 'lithuanian', 'lv': 'latvian', 'et': 'estonian', 'mt': 'maltese',
    'ga': 'irish', 'cy': 'welsh', 'is': 'icelandic', 'eu': 'basque', 'ca': 'catalan',
    'gl': 'galician', 'af': 'afrikaans', 'sw': 'swahili', 'zu': 'zulu', 'xh': 'xhosa',
    'yo': 'yoruba', 'ig': 'igbo', 'ha': 'hausa', 'am': 'amharic', 'bn': 'bengali',
    'ta': 'tamil', 'te': 'telugu', 'ml': 'malayalam', 'kn': 'kannada', 'gu': 'gujarati',
    'pa': 'punjabi', 'ur': 'urdu', 'ne': 'nepali', 'si': 'sinhala', 'my': 'myanmar',
    'km': 'khmer', 'lo': 'lao', 'ka': 'georgian', 'hy': 'armenian', 'az': 'azerbaijani',
    'kk': 'kazakh', 'ky': 'kyrgyz', 'uz': 'uzbek', 'mn': 'mongolian', 'tg': 'tajik'
}

def convertir_video_a_wav(archivo_entrada, archivo_salida):
    try:
        video_clip = VideoFileClip(archivo_entrada)
        audio = video_clip.audio
        audio.write_audiofile(archivo_salida, codec='pcm_s16le')
        print(f"Audio extraído y guardado como {archivo_salida}")
    except Exception as e:
        print(f"Error al convertir video a WAV: {e}")

def mostrar_codigos_idiomas():
    return LANGUAGES

def transcribir_y_traducir(audio_path, idioma_entrada=None, idioma_salida='es', reproducir_audio=False):
    r = sr.Recognizer()
    resultado = {}

    try:
        with sr.AudioFile(audio_path) as recurso:
            print("Leyendo archivo de audio...")
            audio = r.record(recurso)
            if idioma_entrada:
                texto = r.recognize_google(audio, language=idioma_entrada)
                print(f"Texto en {idioma_entrada}: {texto}")
            else:
                texto = r.recognize_google(audio)
                print(f"Texto transcrito: {texto}")

                # Detección del idioma si no se proporciona
                idioma_entrada = detect(texto)
                print(f"Idioma detectado: {idioma_entrada}")

            # Verificar que los idiomas sean válidos
            if idioma_entrada not in LANGUAGES:
                raise ValueError(f"Idioma de entrada no válido: {idioma_entrada}")
            if idioma_salida not in LANGUAGES:
                raise ValueError(f"Idioma de salida no válido: {idioma_salida}")

            # Traducción usando deep-translator
            translator = GoogleTranslator(source=idioma_entrada, target=idioma_salida)
            texto_traducido = translator.translate(texto)
            print(f"Texto traducido a {idioma_salida}: {texto_traducido}")

            resultado['texto'] = texto
            resultado['texto_traducido'] = texto_traducido

            # Crear archivo de audio a partir del texto traducido
            tts = gTTS(text=texto_traducido, lang=idioma_salida)
            """ audio_traduccion_filename = os.path.join(TEMP_DIR, f"traduccion_{uuid.uuid4().hex}.mp3") """
            audio_traduccion_filename = os.path.join(TEMP_DIR, f"audio_traduccion.mp3")
            tts.save(audio_traduccion_filename)
            print(f"Archivo {audio_traduccion_filename} creado")
            resultado['audio_traduccion'] = audio_traduccion_filename

    except sr.UnknownValueError:
        print("Error: No se pudo entender el audio")
    except sr.RequestError as e:
        print(f"Error: Problema en la solicitud a Google Speech Recognition: {e}")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Error inesperado: {e}")

    return resultado

def limpiar_archivos_temporales():
    try:
        Path(os.path.join(TEMP_DIR, "temporal.wav")).unlink()
        print("Archivo temporal.wav eliminado.")
    except FileNotFoundError:
        print("Archivo temporal.wav no encontrado.")

    for temp_file in Path(TEMP_DIR).glob('traduccion_*.mp3'):
        try:
            temp_file.unlink()
            print(f"Archivo {temp_file} eliminado.")
        except FileNotFoundError:
            print(f"Archivo {temp_file} no encontrado.")
