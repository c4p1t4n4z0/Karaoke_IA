import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import threading
import queue
import os


recognizer = sr.Recognizer()  # Inicializa el reconocedor de voz
voice_queue = queue.Queue()  # Cola para manejar las traducciones a voz

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

# Función para obtener los idiomas disponibles
def get_available_languages():
    return LANGUAGES

# Función que se ejecuta en un hilo separado para procesar la cola de voz
def voice_worker():
    while True:
        text = voice_queue.get()
        if text is None:
            break
        tts = gTTS(text, lang='en')  # Ajusta el idioma según tus necesidades
        audio_path = os.path.join('temporales', 'translation_current.mp3')
        tts.save(audio_path)
        # os.system(f"mpg123 {audio_path}")  # Comentado si no es necesario
        voice_queue.task_done()

# Inicializa y arranca el hilo del trabajador de voz
voice_thread = threading.Thread(target=voice_worker)
voice_thread.daemon = True
voice_thread.start()

# Función para reconocer y traducir el audio
def recognize_and_translate(source_lang, target_lang, shared_data):
    error_message = None

    # Función interna para capturar audio en un hilo separado
    def capture_audio_thread(shared_data):
        nonlocal error_message

        with sr.Microphone() as source:
            print("Speak now...")
            while shared_data["capture_audio"]:
                try:
                    # Captura el audio del micrófono
                    audio = recognizer.listen(source, timeout=5)

                    if audio is not None:
                        # Reconoce el texto en el audio
                        text = recognizer.recognize_google(audio, language=source_lang)
                        shared_data['recognized_texts'].append(text)

                        # Traduce el texto reconocido usando deep-translator
                        translator = GoogleTranslator(source=source_lang, target=target_lang)
                        translation = translator.translate(text)
                        shared_data['translation_texts'].append(translation)
                        print("You said: {}".format(text))
                        print("Translation: {}".format(translation))

                        # Verificar y crear la carpeta 'temporales' si no existe
                        if not os.path.exists('temporales'):
                            os.makedirs('temporales')

                        # Guardar la traducción como archivo de audio
                        audio_filename = f'translation_{len(shared_data["translation_texts"])}.mp3'
                        audio_path = os.path.join('temporales', audio_filename)
                        translation_audio = gTTS(translation, lang=target_lang)  # Crear el archivo de audio aquí
                        translation_audio.save(audio_path)

                        # Verificar si el archivo de audio se ha guardado correctamente
                        if not os.path.exists(audio_path):
                            print("El archivo de audio no se ha guardado correctamente.")
                        else:
                            print("El archivo de audio se ha guardado correctamente en", audio_path)
                            shared_data['audio_path'] = audio_filename
                            shared_data['audio_processed'].append(audio_path)  # Añadir a los procesados

                        # Enqueue the translation for speaking
                        if shared_data.get("speak_translations", False):
                            voice_queue.put(translation)

                except sr.UnknownValueError:
                    print("Sorry! Could not understand audio.")
                except sr.RequestError as e:
                    print("Error with the request; {0}".format(e))
                except Exception as e:
                    print("Error: {0}".format(e))

    return capture_audio_thread, error_message
