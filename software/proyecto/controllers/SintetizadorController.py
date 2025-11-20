"""
Controlador para el módulo de Sintetizador de Voz
Procesa música para reemplazar la voz original con una voz clonada del usuario

Proceso:
1. Separación de stems (voz / instrumental)
2. Generación de la letra / alineamiento de la melodía
3. Clonación / síntesis de tu voz
4. Mezcla final

Versión: Opción Gratis (Local)
- Separación: Spleeter
- Letra: Whisper
- Clonación: Coqui TTS (XTTS)
- Mezcla: Pydub
"""

import os
from pathlib import Path
import uuid
import warnings
warnings.filterwarnings('ignore')

# Importar configuración para acceder a API keys
from config import DevConfig

# Directorio temporal para archivos del sintetizador
# Usar ruta absoluta basada en el directorio del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMP_DIR = os.path.join(BASE_DIR, 'proyecto', 'views', 'static', 'archivostemporales', 'sintetizador')
os.makedirs(TEMP_DIR, exist_ok=True)

def separar_stems(audio_path, output_dir=None):
    """
    Paso 1: Separar el audio en stems (voz e instrumental)
    Usa Spleeter (gratis, local)
    
    Args:
        audio_path: Ruta al archivo de audio original
        output_dir: Directorio donde guardar los stems separados
    
    Returns:
        dict: {
            'voz_path': ruta al archivo de voz separada,
            'instrumental_path': ruta al archivo instrumental,
            'status': 'success' o 'error',
            'message': mensaje descriptivo
        }
    """
    if output_dir is None:
        output_dir = TEMP_DIR
    
    try:
        from spleeter.separator import Separator
        from spleeter.audio.adapter import AudioAdapter
        
        # Generar nombres únicos para los archivos
        unique_id = uuid.uuid4().hex[:8]
        base_output = os.path.join(output_dir, f"separated_{unique_id}")
        os.makedirs(base_output, exist_ok=True)
        
        # Inicializar Spleeter con modelo de 2 stems (voz e instrumental)
        print("Inicializando Spleeter...")
        separator = Separator('spleeter:2stems-16kHz')
        
        # Separar el audio
        print(f"Separando stems de: {audio_path}")
        separator.separate_to_file(audio_path, base_output)
        
        # Spleeter guarda los archivos en una subcarpeta con el nombre del archivo
        audio_filename = os.path.splitext(os.path.basename(audio_path))[0]
        separated_folder = os.path.join(base_output, audio_filename)
        
        # Rutas esperadas de Spleeter
        voz_path = os.path.join(separated_folder, "vocals.wav")
        instrumental_path = os.path.join(separated_folder, "accompaniment.wav")
        
        # Verificar que los archivos se crearon
        if not os.path.exists(voz_path) or not os.path.exists(instrumental_path):
            # Intentar con nombres alternativos
            files = os.listdir(separated_folder)
            for file in files:
                if 'vocal' in file.lower():
                    voz_path = os.path.join(separated_folder, file)
                elif 'accompaniment' in file.lower() or 'instrumental' in file.lower():
                    instrumental_path = os.path.join(separated_folder, file)
        
        if os.path.exists(voz_path) and os.path.exists(instrumental_path):
            return {
                'voz_path': voz_path,
                'instrumental_path': instrumental_path,
                'status': 'success',
                'message': 'Separación de stems completada exitosamente'
            }
        else:
            return {
                'voz_path': None,
                'instrumental_path': None,
                'status': 'error',
                'message': 'No se pudieron encontrar los archivos separados'
            }
            
    except ImportError:
        return {
            'voz_path': None,
            'instrumental_path': None,
            'status': 'error',
            'message': 'Spleeter no está instalado. Ejecuta: pip install spleeter'
        }
    except Exception as e:
        return {
            'voz_path': None,
            'instrumental_path': None,
            'status': 'error',
            'message': f'Error en separación de stems: {str(e)}'
        }

def traducir_letra_con_openai(texto, idioma_origen='es', idioma_destino='en', api_key=None):
    """
    Traducir letra usando OpenAI GPT (ChatGPT)
    Puede traducir a cualquier idioma usando la misma API key
    
    Args:
        texto: Texto a traducir
        idioma_origen: Idioma original del texto (código ISO)
        idioma_destino: Idioma al que se quiere traducir (código ISO)
        api_key: API key de OpenAI
    
    Returns:
        dict: {
            'texto_traducido': texto traducido,
            'status': 'success' o 'error',
            'message': mensaje descriptivo
        }
    """
    try:
        from openai import OpenAI
        
        if not api_key:
            api_key = DevConfig.OPENAI_API_KEY
        
        if not api_key or api_key == "sk-tu-api-key-aqui" or api_key == "":
            return {
                'texto_traducido': texto,
                'status': 'error',
                'message': 'OPENAI_API_KEY no está configurada. No se puede traducir.'
            }
        
        client = OpenAI(api_key=api_key)
        
        # Mapear códigos ISO a nombres de idiomas para el prompt
        nombres_idiomas = {
            'es': 'español', 'en': 'inglés', 'fr': 'francés', 'de': 'alemán',
            'it': 'italiano', 'pt': 'portugués', 'ja': 'japonés', 'ko': 'coreano',
            'zh': 'chino', 'ru': 'ruso', 'ar': 'árabe', 'hi': 'hindi',
            'tr': 'turco', 'pl': 'polaco', 'nl': 'holandés', 'sv': 'sueco',
            'no': 'noruego', 'da': 'danés', 'fi': 'finés', 'cs': 'checo',
            'ro': 'rumano', 'hu': 'húngaro', 'el': 'griego', 'he': 'hebreo',
            'th': 'tailandés', 'vi': 'vietnamita', 'id': 'indonesio', 'uk': 'ucraniano'
        }
        
        idioma_orig_nombre = nombres_idiomas.get(idioma_origen.lower(), idioma_origen)
        idioma_dest_nombre = nombres_idiomas.get(idioma_destino.lower(), idioma_destino)
        
        print(f"🌍 Traduciendo letra usando OpenAI GPT...")
        print(f"   Idioma origen: {idioma_orig_nombre} ({idioma_origen})")
        print(f"   Idioma destino: {idioma_dest_nombre} ({idioma_destino})")
        print(f"   Texto: {texto[:100]}...")
        
        # Crear prompt para traducción
        prompt = f"""Traduce el siguiente texto de {idioma_orig_nombre} a {idioma_dest_nombre}.
Mantén el formato original (saltos de línea, estrofas, etc.).
Si es una canción, intenta mantener la rima y el ritmo cuando sea posible.

Texto a traducir:
{texto}

Traducción:"""
        
        # Usar GPT-3.5-turbo para traducción (más económico que GPT-4)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un traductor profesional especializado en traducir letras de canciones manteniendo el sentido y cuando sea posible, la rima y el ritmo."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Baja temperatura para traducciones más precisas y consistentes
            max_tokens=2000  # Ajustar según la longitud del texto
        )
        
        texto_traducido = response.choices[0].message.content.strip()
        
        if texto_traducido:
            print(f"✅ Traducción completada con OpenAI GPT")
            print(f"   Texto traducido: {len(texto_traducido)} caracteres")
            
            return {
                'texto_traducido': texto_traducido,
                'status': 'success',
                'message': f'Letra traducida exitosamente de {idioma_orig_nombre} a {idioma_dest_nombre} usando OpenAI GPT'
            }
        else:
            return {
                'texto_traducido': texto,
                'status': 'error',
                'message': 'No se pudo traducir la letra con OpenAI GPT'
            }
            
    except ImportError:
        return {
            'texto_traducido': texto,
            'status': 'error',
            'message': 'Librería openai no está instalada. Ejecuta: pip install openai'
        }
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error al traducir con OpenAI GPT: {str(e)}")
        print(f"Traceback: {error_trace}")
        return {
            'texto_traducido': texto,
            'status': 'error',
            'message': f'Error al traducir: {str(e)}'
        }

def generar_letra(texto_letra=None, audio_path=None, idioma='es', traducir_a=None):
    """
    Paso 2: Generar o extraer letra y alinearla con la melodía
    Usa OpenAI Whisper API si está configurada (más rápida y precisa), 
    o Whisper local como fallback (gratis pero más lento)
    
    Si se especifica traducir_a, traduce la letra extraída usando OpenAI GPT
    
    Prioridad:
    1. OpenAI Whisper API (si OPENAI_API_KEY está configurada)
    2. Whisper local (fallback)
    3. Traducción con OpenAI GPT (si traducir_a está especificado)
    
    Args:
        texto_letra: Texto de la letra proporcionado por el usuario (opcional)
        audio_path: Ruta al audio para extraer letra automáticamente (opcional)
        idioma: Idioma de la letra original (código ISO, ej: 'es', 'en')
        traducir_a: Idioma al que traducir la letra (código ISO, ej: 'en', 'fr'). Si es None, no traduce
    
    Returns:
        dict: {
            'letra': texto de la letra (traducido si traducir_a está especificado),
            'letra_original': texto original antes de traducir (si se tradujo),
            'alineamiento': datos de alineamiento temporal,
            'status': 'success' o 'error',
            'message': mensaje descriptivo
        }
    """
    try:
        # Si ya se proporcionó la letra, usarla directamente
        if texto_letra and texto_letra.strip():
            letra_resultado = texto_letra.strip()
            letra_original = letra_resultado
            
            # Si se solicita traducción, traducir la letra proporcionada
            if traducir_a and traducir_a != idioma:
                print(f"🌍 Traduciendo letra proporcionada de {idioma} a {traducir_a}...")
                resultado_traduccion = traducir_letra_con_openai(letra_resultado, idioma, traducir_a)
                if resultado_traduccion['status'] == 'success':
                    letra_resultado = resultado_traduccion['texto_traducido']
            
            return {
                'letra': letra_resultado,
                'letra_original': letra_original,
                'alineamiento': {},
                'status': 'success',
                'message': 'Letra proporcionada por el usuario' + (f' (traducida a {traducir_a})' if traducir_a and traducir_a != idioma else '')
            }
        
        # Si no hay letra pero hay audio, extraerla
        if audio_path and os.path.exists(audio_path):
            # Verificar si tenemos API key de OpenAI configurada
            openai_api_key = DevConfig.OPENAI_API_KEY
            
            # Extraer letra (transcripción)
            if openai_api_key and openai_api_key != "sk-tu-api-key-aqui" and openai_api_key != "":
                # Usar OpenAI Whisper API (más rápida y precisa)
                print(f"🚀 Usando OpenAI Whisper API para transcribir: {audio_path}")
                resultado = _generar_letra_openai_api(audio_path, idioma, openai_api_key)
            else:
                # Usar Whisper local (fallback)
                print(f"📦 Usando Whisper local para transcribir: {audio_path}")
                print(f"💡 Tip: Agrega OPENAI_API_KEY en .env para usar API de OpenAI (más rápida y precisa)")
                resultado = _generar_letra_whisper_local(audio_path, idioma)
            
            # Si la transcripción fue exitosa y se solicita traducción, traducir
            if resultado['status'] == 'success' and traducir_a:
                letra_extraida = resultado['letra']
                letra_original = letra_extraida
                
                # Usar el idioma detectado en la transcripción si está disponible
                idioma_detectado = resultado.get('alineamiento', {}).get('language', idioma)
                
                # Solo traducir si el idioma destino es diferente al idioma origen
                if traducir_a != idioma_detectado and traducir_a != idioma:
                    print(f"🌍 Traduciendo letra extraída de {idioma_detectado} a {traducir_a}...")
                    resultado_traduccion = traducir_letra_con_openai(letra_extraida, idioma_detectado, traducir_a)
                    
                    if resultado_traduccion['status'] == 'success':
                        resultado['letra'] = resultado_traduccion['texto_traducido']
                        resultado['letra_original'] = letra_original
                        resultado['message'] += f' y traducida a {traducir_a}'
                        print(f"✅ Traducción completada: {idioma_detectado} → {traducir_a}")
                    else:
                        # Si falla la traducción, usar la letra original
                        print(f"⚠️  La traducción falló, usando letra original")
                        print(f"   Mensaje de error: {resultado_traduccion.get('message', 'Error desconocido')}")
                else:
                    print(f"💡 No es necesario traducir: el idioma destino ({traducir_a}) es igual al idioma origen ({idioma_detectado})")
            
            return resultado
        
        # Si no hay letra ni audio, error
        return {
            'letra': '',
            'alineamiento': {},
            'status': 'error',
            'message': 'No se proporcionó letra ni audio para extraerla'
        }
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error al extraer letra: {str(e)}")
        print(f"Traceback: {error_trace}")
        return {
            'letra': texto_letra or '',
            'alineamiento': {},
            'status': 'error',
            'message': f'Error al extraer letra: {str(e)}'
        }

def _generar_letra_openai_api(audio_path, idioma='es', api_key=None):
    """
    Extraer letra del audio usando OpenAI Whisper API
    Más rápida y precisa que Whisper local, pero requiere API key
    
    Args:
        audio_path: Ruta al archivo de audio
        idioma: Idioma del audio (código ISO)
        api_key: API key de OpenAI
    
    Returns:
        dict: Resultado de la transcripción
    """
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key)
        
        print(f"🎤 Transcribiendo con OpenAI Whisper API...")
        print(f"   Idioma: {idioma}")
        print(f"   Audio: {audio_path}")
        
        # Abrir el archivo de audio
        with open(audio_path, 'rb') as audio_file:
            # Mapear idioma a código de OpenAI
            # OpenAI acepta códigos ISO 639-1
            language_map = {
                'es': 'es',  # Español
                'en': 'en',  # Inglés
                'fr': 'fr',  # Francés
                'de': 'de',  # Alemán
                'it': 'it',  # Italiano
                'pt': 'pt',  # Portugués
                'ja': 'ja',  # Japonés
                'ko': 'ko',  # Coreano
                'zh': 'zh',  # Chino
            }
            openai_lang = language_map.get(idioma.lower(), None)
            
            # Transcribir usando OpenAI Whisper API
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=openai_lang if openai_lang else None,  # Si es None, Whisper detecta automáticamente
                response_format="verbose_json"  # Para obtener información adicional como timestamps
            )
        
        letra_extraida = transcript.text.strip()
        
        if letra_extraida:
            # Extraer información de alineamiento si está disponible
            segments = []
            try:
                # Intentar obtener segments si están disponibles
                if hasattr(transcript, 'segments') and transcript.segments:
                    for seg in transcript.segments:
                        try:
                            # TranscriptionSegment es un objeto Pydantic, usar acceso a atributos
                            seg_dict = {
                                'start': getattr(seg, 'start', None) or (seg.start if hasattr(seg, 'start') else 0),
                                'end': getattr(seg, 'end', None) or (seg.end if hasattr(seg, 'end') else 0),
                                'text': getattr(seg, 'text', None) or (seg.text if hasattr(seg, 'text') else '')
                            }
                            segments.append(seg_dict)
                        except AttributeError:
                            # Si es un diccionario en lugar de objeto Pydantic
                            try:
                                seg_dict = {
                                    'start': seg.get('start', 0) if isinstance(seg, dict) else 0,
                                    'end': seg.get('end', 0) if isinstance(seg, dict) else 0,
                                    'text': seg.get('text', '') if isinstance(seg, dict) else ''
                                }
                                segments.append(seg_dict)
                            except Exception:
                                # Si no podemos extraer segmentos, continuar sin ellos
                                pass
            except Exception as seg_error:
                # Si no podemos obtener segments, no es crítico, continuar sin ellos
                print(f"⚠️  No se pudieron extraer segments de alineamiento: {str(seg_error)}")
                segments = []
            
            # Obtener el idioma detectado
            detected_language = getattr(transcript, 'language', None) or idioma
            
            print(f"✅ Transcripción completada con OpenAI Whisper API")
            print(f"   Letra extraída: {len(letra_extraida)} caracteres")
            if detected_language:
                print(f"   Idioma detectado: {detected_language}")
            
            return {
                'letra': letra_extraida,
                'alineamiento': {
                    'segments': segments,
                    'language': detected_language
                },
                'status': 'success',
                'message': 'Letra extraída exitosamente con OpenAI Whisper API'
            }
        else:
            return {
                'letra': '',
                'alineamiento': {},
                'status': 'error',
                'message': 'No se pudo extraer letra del audio con OpenAI Whisper API'
            }
            
    except ImportError:
        print("⚠️  Librería openai no está instalada, usando Whisper local...")
        return _generar_letra_whisper_local(audio_path, idioma)
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error con OpenAI Whisper API: {str(e)}")
        print(f"🔄 Cambiando a Whisper local...")
        print(f"Traceback: {error_trace}")
        # Fallback a Whisper local si falla la API
        return _generar_letra_whisper_local(audio_path, idioma)

def _generar_letra_whisper_local(audio_path, idioma='es'):
    """
    Extraer letra del audio usando Whisper local
    Gratis pero más lento que la API
    
    Args:
        audio_path: Ruta al archivo de audio
        idioma: Idioma del audio (código ISO)
    
    Returns:
        dict: Resultado de la transcripción
    """
    try:
        import whisper
        
        print(f"📦 Cargando modelo Whisper local...")
        
        # Cargar modelo Whisper (base es un buen balance entre velocidad y calidad)
        # Modelos disponibles: tiny, base, small, medium, large
        model = whisper.load_model("base")
        
        # Mapear idioma a código de Whisper si es necesario
        language_map = {
            'es': 'spanish',
            'en': 'english',
            'fr': 'french',
            'de': 'german',
            'it': 'italian',
            'pt': 'portuguese'
        }
        whisper_lang = language_map.get(idioma.lower(), None)
        
        print(f"🎤 Transcribiendo con Whisper local...")
        print(f"   Idioma: {whisper_lang or 'auto-detectado'}")
        
        result = model.transcribe(
            audio_path,
            language=whisper_lang,
            task="transcribe"
        )
        
        letra_extraida = result["text"].strip()
        
        if letra_extraida:
            print(f"✅ Transcripción completada con Whisper local")
            print(f"   Letra extraída: {len(letra_extraida)} caracteres")
            
            return {
                'letra': letra_extraida,
                'letra_original': letra_extraida,  # Guardar original por si se traduce después
                'alineamiento': {
                    'segments': result.get('segments', []),
                    'language': result.get('language', idioma)
                },
                'status': 'success',
                'message': 'Letra extraída exitosamente con Whisper local'
            }
        else:
            return {
                'letra': '',
                'alineamiento': {},
                'status': 'error',
                'message': 'No se pudo extraer letra del audio con Whisper local'
            }
            
    except ImportError:
        return {
            'letra': '',
            'alineamiento': {},
            'status': 'error',
            'message': 'Whisper no está instalado. Ejecuta: pip install openai-whisper o configura OPENAI_API_KEY para usar la API'
        }
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error con Whisper local: {str(e)}")
        print(f"Traceback: {error_trace}")
        return {
            'letra': '',
            'alineamiento': {},
            'status': 'error',
            'message': f'Error al extraer letra con Whisper local: {str(e)}'
        }

def clonar_voz(texto, voz_referencia_path, output_path=None, voice_id_existente=None):
    """
    Paso 3: Clonar la voz del usuario y sintetizar la letra
    Intenta usar APIs externas (Resemble.ai, ElevenLabs) si hay API KEY configurada
    Si no, usa Coqui TTS con XTTS (gratis, local pero más pesado)
    
    Prioridad:
    1. Resemble.ai (si está configurado)
    2. ElevenLabs (si está configurado)
    3. Coqui TTS local (fallback)
    
    Args:
        texto: Texto a sintetizar con la voz clonada
        voz_referencia_path: Ruta al audio de referencia de la voz a clonar
        output_path: Ruta donde guardar el audio generado
        voice_id_existente: (Opcional) Voice ID de una voz ya creada
    
    Returns:
        dict: {
            'audio_path': ruta al audio generado,
            'status': 'success' o 'error',
            'message': mensaje descriptivo
        }
    """
    if output_path is None:
        unique_id = uuid.uuid4().hex[:8]
        output_path = os.path.join(TEMP_DIR, f"voz_clonada_{unique_id}.wav")
    
    # Verificar APIs disponibles (prioridad: Resemble.ai > ElevenLabs > Local)
    resemble_api_key = DevConfig.RESEMBLE_API_KEY
    elevenlabs_api_key = DevConfig.ELEVENLABS_API_KEY
    elevenlabs_voice_id = DevConfig.ELEVENLABS_VOICE_ID
    
    # Prioridad 1: Resemble.ai
    if resemble_api_key:
        print("🎤 Usando Resemble.ai API...")
        return _clonar_voz_resemble(texto, voz_referencia_path, output_path, resemble_api_key)
    
    # Prioridad 2: ElevenLabs
    if elevenlabs_api_key:
        print("🚀 Usando ElevenLabs API (más liviano y rápido)...")
        # Si hay un Voice ID configurado o se proporciona uno, usarlo directamente
        voice_id_a_usar = voice_id_existente or elevenlabs_voice_id
        if voice_id_a_usar:
            print(f"📌 Usando voz existente (Voice ID: {voice_id_a_usar})")
            return _usar_voz_existente_elevenlabs(texto, voice_id_a_usar, output_path, elevenlabs_api_key)
        # Si no hay Voice ID, intentar crear una nueva voz
        return _clonar_voz_elevenlabs(texto, voz_referencia_path, output_path, elevenlabs_api_key)
    
    # Si no hay API key configurada, retornar error
    print("❌ ERROR: No hay API KEY configurada para clonación de voz")
    print("💡 Para usar clonación de voz, necesitas configurar una API KEY:")
    print("   - ELEVENLABS_API_KEY (recomendado): https://elevenlabs.io/")
    print("   - RESEMBLE_API_KEY (alternativa): https://www.resemble.ai/")
    print("💡 También puedes usar voces predefinidas de ElevenLabs para pruebas")
    return {
        'audio_path': None,
        'status': 'error',
        'message': 'No hay API KEY configurada. Agrega ELEVENLABS_API_KEY o RESEMBLE_API_KEY en el archivo .env'
    }

def _clonar_voz_resemble(texto, voz_referencia_path, output_path, api_key):
    """
    Clonar voz usando Resemble.ai API
    Resemble.ai requiere crear un proyecto y luego clonar la voz
    
    Args:
        texto: Texto a sintetizar con la voz clonada
        voz_referencia_path: Ruta al audio de referencia de la voz a clonar
        output_path: Ruta donde guardar el audio generado
        api_key: API key de Resemble.ai
    
    Returns:
        dict: Resultado de la clonación y síntesis
    """
    try:
        import requests
        import base64
        import time
        
        # URL base de la API de Resemble.ai
        API_BASE_URL = "https://app.resemble.ai/api/v2"
        headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json"
        }
        
        print(f"🎤 Clonando voz con Resemble.ai API...")
        print(f"Texto a sintetizar: {texto[:50]}...")
        print(f"Voz de referencia: {voz_referencia_path}")
        
        # Normalizar rutas
        voz_referencia_path = os.path.normpath(voz_referencia_path)
        output_path = os.path.normpath(output_path)
        
        # Verificar que el archivo de referencia existe
        if not os.path.exists(voz_referencia_path):
            return {
                'audio_path': None,
                'status': 'error',
                'message': f'Archivo de voz de referencia no encontrado: {voz_referencia_path}'
            }
        
        print(f"✅ Archivo de referencia verificado: {voz_referencia_path}")
        
        # Paso 1: Obtener o crear un proyecto
        print("📁 Obteniendo proyecto de Resemble.ai...")
        # Resemble.ai requiere el parámetro page (debe ser >= 1)
        projects_response = requests.get(f"{API_BASE_URL}/projects?page=1", headers=headers)
        
        project_uuid = None
        
        if projects_response.status_code == 200:
            response_data = projects_response.json()
            projects = response_data.get('items', [])
            if projects:
                project_uuid = projects[0].get('uuid')
                print(f"✅ Usando proyecto existente: {project_uuid}")
            else:
                # No hay proyectos, crear uno nuevo
                print("📝 No se encontraron proyectos, creando uno nuevo...")
                project_data = {
                    "name": "Karaoke Synthesizer",
                    "description": "Proyecto para sintetizador de karaoke"
                }
                create_project_response = requests.post(f"{API_BASE_URL}/projects", json=project_data, headers=headers)
                if create_project_response.status_code in [200, 201]:
                    create_response_data = create_project_response.json()
                    # Resemble.ai puede devolver success:true con item dentro
                    if create_response_data.get('success') and create_response_data.get('item'):
                        project_uuid = create_response_data.get('item', {}).get('uuid')
                        print(f"✅ Proyecto creado exitosamente: {project_uuid}")
                    elif create_response_data.get('uuid'):
                        project_uuid = create_response_data.get('uuid')
                        print(f"✅ Proyecto creado exitosamente: {project_uuid}")
                    else:
                        return {
                            'audio_path': None,
                            'status': 'error',
                            'message': f'Error: No se pudo obtener UUID del proyecto creado. Respuesta: {create_response_data}'
                        }
                else:
                    return {
                        'audio_path': None,
                        'status': 'error',
                        'message': f'Error al crear proyecto (status {create_project_response.status_code}): {create_project_response.text}'
                    }
        else:
            # Error al obtener proyectos, intentar crear uno nuevo
            print(f"⚠️ Error al obtener proyectos (status {projects_response.status_code}): {projects_response.text}")
            print("📝 Intentando crear un nuevo proyecto...")
            project_data = {
                "name": "Karaoke Synthesizer",
                "description": "Proyecto para sintetizador de karaoke"
            }
            create_project_response = requests.post(f"{API_BASE_URL}/projects", json=project_data, headers=headers)
            if create_project_response.status_code in [200, 201]:
                create_response_data = create_project_response.json()
                # Resemble.ai puede devolver success:true con item dentro
                if create_response_data.get('success') and create_response_data.get('item'):
                    project_uuid = create_response_data.get('item', {}).get('uuid')
                    print(f"✅ Proyecto creado exitosamente: {project_uuid}")
                elif create_response_data.get('uuid'):
                    project_uuid = create_response_data.get('uuid')
                    print(f"✅ Proyecto creado exitosamente: {project_uuid}")
                else:
                    return {
                        'audio_path': None,
                        'status': 'error',
                        'message': f'Error: No se pudo obtener UUID del proyecto creado. Respuesta: {create_response_data}'
                    }
            else:
                return {
                    'audio_path': None,
                    'status': 'error',
                    'message': f'Error al crear proyecto (status {create_project_response.status_code}): {create_project_response.text}'
                }
        
        if not project_uuid:
            return {
                'audio_path': None,
                'status': 'error',
                'message': 'Error: No se pudo obtener o crear un proyecto en Resemble.ai'
            }
        
        # Paso 2: Leer el archivo de audio y convertirlo a base64
        print("📤 Subiendo audio de referencia para clonar voz...")
        with open(voz_referencia_path, 'rb') as audio_file:
            audio_data = audio_file.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        # Paso 3: Crear/clonar la voz
        voice_name = f"temp_voice_{uuid.uuid4().hex[:8]}"
        create_voice_data = {
            "name": voice_name,
            "project_uuid": project_uuid
        }
        
        # Resemble.ai requiere subir el audio en un formato específico
        # Primero creamos la voz, luego subimos el audio
        create_voice_response = requests.post(
            f"{API_BASE_URL}/projects/{project_uuid}/voices",
            json=create_voice_data,
            headers=headers
        )
        
        if create_voice_response.status_code not in [200, 201]:
            # Intentar método alternativo: usar voz existente o crear directamente con audio
            print("⚠️ Método directo falló, intentando método alternativo...")
            # Resemble.ai puede requerir subir el audio primero
            # Intentar crear voz con audio directamente
            try:
                # Leer archivo como multipart/form-data
                files = {
                    'file': (os.path.basename(voz_referencia_path), open(voz_referencia_path, 'rb'), 'audio/wav')
                }
                voice_headers = {
                    "Authorization": f"Token {api_key}"
                }
                upload_response = requests.post(
                    f"{API_BASE_URL}/projects/{project_uuid}/voices",
                    files=files,
                    data={'name': voice_name},
                    headers=voice_headers
                )
                
                if upload_response.status_code in [200, 201]:
                    # Verificar que la respuesta sea JSON, no HTML
                    try:
                        voice_data = upload_response.json()
                        voice_uuid = voice_data.get('item', {}).get('uuid') or voice_data.get('uuid')
                        if voice_uuid:
                            print(f"✅ Voz creada: {voice_uuid}")
                        else:
                            raise Exception("No se pudo obtener voice_uuid de la respuesta")
                    except ValueError:
                        # La respuesta no es JSON, probablemente HTML (error 404)
                        raise Exception(f"Resemble.ai devolvió HTML en lugar de JSON. Endpoint puede estar incorrecto. Respuesta: {upload_response.text[:200]}")
                else:
                    # Verificar si la respuesta es HTML (error 404)
                    if upload_response.text.strip().startswith('<!DOCTYPE') or upload_response.text.strip().startswith('<html'):
                        raise Exception(f"Resemble.ai devolvió página HTML (404). El endpoint puede estar incorrecto o la API key no tiene permisos.")
                    raise Exception(f"Error al crear voz (status {upload_response.status_code}): {upload_response.text[:200]}")
            except Exception as upload_error:
                error_message = str(upload_error)
                print(f"❌ Error al crear voz en Resemble.ai: {error_message}")
                print(f"💡 Verifica que tu RESEMBLE_API_KEY sea correcta y tenga los permisos necesarios")
                return {
                    'audio_path': None,
                    'status': 'error',
                    'message': f'Error al crear voz en Resemble.ai: {error_message}. Verifica tu API key y permisos.'
                }
        else:
            voice_data = create_voice_response.json()
            voice_uuid = voice_data.get('item', {}).get('uuid') or voice_data.get('uuid')
            print(f"✅ Voz creada: {voice_uuid}")
            
            # Subir audio a la voz creada
            try:
                files = {
                    'file': (os.path.basename(voz_referencia_path), open(voz_referencia_path, 'rb'), 'audio/wav')
                }
                voice_headers = {
                    "Authorization": f"Token {api_key}"
                }
                upload_response = requests.post(
                    f"{API_BASE_URL}/projects/{project_uuid}/voices/{voice_uuid}/clips",
                    files=files,
                    headers=voice_headers
                )
                if upload_response.status_code not in [200, 201]:
                    print(f"⚠️ Advertencia: No se pudo subir audio de referencia: {upload_response.text}")
            except Exception as upload_error:
                print(f"⚠️ Advertencia: Error al subir audio: {str(upload_error)}")
        
        # Paso 4: Generar audio con la voz clonada
        print("🎵 Generando audio con voz clonada...")
        clip_data = {
            "project_uuid": project_uuid,
            "voice_uuid": voice_uuid,
            "body": texto
        }
        
        create_clip_response = requests.post(
            f"{API_BASE_URL}/projects/{project_uuid}/clips",
            json=clip_data,
            headers=headers
        )
        
        if create_clip_response.status_code not in [200, 201]:
            return {
                'audio_path': None,
                'status': 'error',
                'message': f'Error al generar audio: {create_clip_response.text}'
            }
        
        clip_data_response = create_clip_response.json()
        clip_uuid = clip_data_response.get('item', {}).get('uuid') or clip_data_response.get('uuid')
        print(f"✅ Clip creado: {clip_uuid}")
        
        # Paso 5: Esperar a que el clip esté listo y descargarlo
        print("⏳ Esperando a que el audio esté listo...")
        max_attempts = 30
        attempt = 0
        
        while attempt < max_attempts:
            time.sleep(2)  # Esperar 2 segundos entre intentos
            clip_status_response = requests.get(
                f"{API_BASE_URL}/projects/{project_uuid}/clips/{clip_uuid}",
                headers=headers
            )
            
            if clip_status_response.status_code == 200:
                clip_info = clip_status_response.json().get('item', {})
                status = clip_info.get('status', '')
                
                if status == 'completed':
                    # Descargar el audio
                    audio_url = clip_info.get('audio_src') or clip_info.get('audio_url')
                    if audio_url:
                        print(f"📥 Descargando audio desde: {audio_url}")
                        audio_response = requests.get(audio_url)
                        
                        if audio_response.status_code == 200:
                            output_abs = os.path.abspath(output_path)
                            os.makedirs(os.path.dirname(output_abs), exist_ok=True)
                            
                            with open(output_abs, 'wb') as f:
                                f.write(audio_response.content)
                            
                            if os.path.exists(output_abs):
                                file_size = os.path.getsize(output_abs)
                                print(f"✅ Audio generado exitosamente: {output_abs} ({file_size} bytes)")
                                
                                # Limpiar: eliminar voz temporal (opcional)
                                try:
                                    requests.delete(
                                        f"{API_BASE_URL}/projects/{project_uuid}/voices/{voice_uuid}",
                                        headers=headers
                                    )
                                    print(f"🧹 Voz temporal eliminada")
                                except:
                                    pass
                                
                                return {
                                    'audio_path': output_abs,
                                    'status': 'success',
                                    'message': 'Voz clonada y sintetizada exitosamente con Resemble.ai'
                                }
                elif status == 'failed':
                    return {
                        'audio_path': None,
                        'status': 'error',
                        'message': 'Error: El clip falló al procesarse en Resemble.ai'
                    }
            
            attempt += 1
            print(f"   Intento {attempt}/{max_attempts}...")
        
        return {
            'audio_path': None,
            'status': 'error',
            'message': 'Timeout: El audio tardó demasiado en generarse'
        }
        
    except ImportError:
        return {
            'audio_path': None,
            'status': 'error',
            'message': 'La librería requests no está instalada. Ejecuta: pip install requests'
        }
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        error_message = str(e)
        
        # Verificar si es un error de HTML (404) o de API
        if '<!DOCTYPE' in error_message or '<html' in error_message or '404' in error_message:
            print(f"\n❌ Resemble.ai devolvió una página de error (404)")
            print(f"💡 Esto puede indicar que:")
            print(f"   - El endpoint de la API es incorrecto")
            print(f"   - La API key no tiene permisos suficientes")
            print(f"   - La estructura de la API ha cambiado")
            return {
                'audio_path': None,
                'status': 'error',
                'message': f'Error 404 con Resemble.ai: El endpoint puede estar incorrecto o la API key no tiene permisos. Verifica tu configuración.'
            }
        
        print(f"❌ Error en clonación con Resemble.ai: {error_message}")
        print(f"Traceback: {error_trace}")
        return {
            'audio_path': None,
            'status': 'error',
            'message': f'Error con Resemble.ai API: {error_message}. Verifica tu API key y configuración.'
        }

def usar_voz_predefinida_elevenlabs(texto, output_path, api_key, voice_id_predefinida=None):
    """
    Usar una voz predefinida de ElevenLabs para pruebas (sin necesidad de clonar)
    Útil cuando no se puede clonar voz o para hacer pruebas rápidas
    
    Voces predefinidas populares de ElevenLabs:
    - Rachel (21m00Tcm4TlvDq8ikWAM): Voz femenina profesional
    - Domi (AZnzlk1XvdvUeBnXmlld): Voz femenina expresiva
    - Bella (EXAVITQu4vr4xnSDxMaL): Voz femenina suave
    - Elli (MF3mGyEYCl7XYWbV9V6O): Voz femenina joven
    - Josh (TxGEqnHWrfWFTfGW9XjX): Voz masculina profesional
    - Arnold (VR6AewLTigWG4xSOukaG): Voz masculina profunda
    - Adam (pNInz6obpgDQGcFmaJgB): Voz masculina suave
    - Sam (yoZ06aMxZJJ28mfd3POQ): Voz masculina joven
    
    Args:
        texto: Texto a sintetizar
        output_path: Ruta donde guardar el audio generado
        api_key: API key de ElevenLabs
        voice_id_predefinida: (Opcional) Voice ID de una voz predefinida. Si es None, usa Rachel por defecto
    
    Returns:
        dict: Resultado de la síntesis
    """
    try:
        from elevenlabs import ElevenLabs, VoiceSettings
        
        client = ElevenLabs(api_key=api_key)
        
        # Usar Rachel por defecto si no se especifica una voz
        if voice_id_predefinida is None:
            voice_id_predefinida = "21m00Tcm4TlvDq8ikWAM"  # Rachel
        
        print(f"🎤 Usando voz predefinida de ElevenLabs (Voice ID: {voice_id_predefinida})...")
        print(f"Texto a sintetizar: {texto[:50]}...")
        print(f"💡 Tip: Esta es una voz predefinida, no requiere clonación")
        
        # Generar audio usando la voz predefinida
        audio_stream = client.text_to_speech.convert(
            voice_id=voice_id_predefinida,
            text=texto,
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=0.5,
                similarity_boost=0.75,
                style=0.0,
                use_speaker_boost=True
            )
        )
        
        # Guardar el audio generado
        output_abs = os.path.abspath(output_path)
        os.makedirs(os.path.dirname(output_abs), exist_ok=True)
        
        with open(output_abs, 'wb') as f:
            for chunk in audio_stream:
                if hasattr(chunk, 'read'):
                    f.write(chunk.read())
                else:
                    f.write(chunk)
        
        if os.path.exists(output_abs):
            return {
                'audio_path': output_abs,
                'status': 'success',
                'message': f'Audio generado exitosamente con voz predefinida (ID: {voice_id_predefinida})'
            }
        else:
            return {
                'audio_path': None,
                'status': 'error',
                'message': f'No se pudo generar el archivo de audio en: {output_abs}'
            }
            
    except Exception as e:
        import traceback
        from elevenlabs.core.api_error import ApiError
        
        error_trace = traceback.format_exc()
        error_message = str(e)
        
        # Detectar si es un error de cuota excedida
        is_quota_error = False
        credits_needed = None
        credits_remaining = None
        
        if isinstance(e, ApiError):
            body = getattr(e, 'body', {})
            if isinstance(body, dict):
                detail = body.get('detail', {})
                if isinstance(detail, dict):
                    status = detail.get('status', '')
                    message = detail.get('message', '')
                    if 'quota_exceeded' in status or 'quota' in message.lower():
                        is_quota_error = True
                        # Intentar extraer números del mensaje
                        import re
                        numbers = re.findall(r'\d+', message)
                        if len(numbers) >= 2:
                            credits_remaining = int(numbers[0]) if numbers else None
                            credits_needed = int(numbers[1]) if len(numbers) > 1 else None
        else:
            # Verificar en el mensaje de error
            if 'quota_exceeded' in error_message.lower() or 'exceeds your quota' in error_message.lower():
                is_quota_error = True
                import re
                numbers = re.findall(r'\d+', error_message)
                if len(numbers) >= 2:
                    credits_remaining = int(numbers[0]) if numbers else None
                    credits_needed = int(numbers[1]) if len(numbers) > 1 else None
        
        if is_quota_error:
            print("\n" + "=" * 60)
            print("❌ ERROR: Créditos de ElevenLabs Insuficientes")
            print("=" * 60)
            print("\n💳 PROBLEMA:")
            print(f"   Tienes {credits_remaining or 'pocos'} créditos restantes")
            print(f"   Necesitas {credits_needed or 'muchos'} créditos para esta solicitud")
            print("\n📝 SOLUCIÓN:")
            print("   1. Espera a que se renueven tus créditos mensuales")
            print("   2. Actualiza tu plan de ElevenLabs para obtener más créditos")
            print("   3. Divide el texto en partes más pequeñas")
            print("   4. Usa una letra más corta para la síntesis")
            print("\n💡 CONSEJO:")
            print("   - Una canción completa puede requerir muchos créditos")
            print("   - Considera procesar solo una parte de la canción primero")
            print("   - Plan Starter: 30,000 créditos/mes (~30 minutos de audio)")
            print("   - Plan Creator: 100,000 créditos/mes (~100 minutos de audio)")
            print("=" * 60 + "\n")
            
            return {
                'audio_path': None,
                'status': 'error',
                'message': f'Créditos de ElevenLabs insuficientes. Tienes {credits_remaining or "pocos"} créditos restantes pero necesitas {credits_needed or "muchos"} para esta solicitud. La letra es demasiado larga. Considera dividirla en partes más pequeñas o actualizar tu plan.'
            }
        
        print(f"❌ Error al usar voz predefinida: {error_message}")
        print(f"Traceback: {error_trace}")
        return {
            'audio_path': None,
            'status': 'error',
            'message': f'Error al usar voz predefinida: {error_message}'
        }

def _usar_voz_existente_elevenlabs(texto, voice_id, output_path, api_key):
    """
    Usar una voz existente en ElevenLabs (creada desde el dashboard web)
    Útil cuando no se tiene permiso voices_write para crear voces programáticamente
    
    Args:
        texto: Texto a sintetizar
        voice_id: ID de la voz existente en ElevenLabs
        output_path: Ruta donde guardar el audio generado
        api_key: API key de ElevenLabs
    
    Returns:
        dict: Resultado de la síntesis
    """
    try:
        from elevenlabs import ElevenLabs, VoiceSettings
        
        client = ElevenLabs(api_key=api_key)
        
        print(f"🎤 Usando voz existente de ElevenLabs (Voice ID: {voice_id})...")
        print(f"Texto a sintetizar: {texto[:50]}...")
        
        # Generar audio usando la voz existente
        audio_stream = client.text_to_speech.convert(
            voice_id=voice_id,
            text=texto,
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=0.5,
                similarity_boost=0.75,
                style=0.0,
                use_speaker_boost=True
            )
        )
        
        # Guardar el audio generado
        output_abs = os.path.abspath(output_path)
        os.makedirs(os.path.dirname(output_abs), exist_ok=True)
        
        with open(output_abs, 'wb') as f:
            for chunk in audio_stream:
                if hasattr(chunk, 'read'):
                    f.write(chunk.read())
                else:
                    f.write(chunk)
        
        if os.path.exists(output_abs):
            return {
                'audio_path': output_abs,
                'status': 'success',
                'message': f'Audio generado exitosamente con voz existente (ID: {voice_id})'
            }
        else:
            return {
                'audio_path': None,
                'status': 'error',
                'message': f'No se pudo generar el archivo de audio en: {output_abs}'
            }
            
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error al usar voz existente: {str(e)}")
        print(f"Traceback: {error_trace}")
        return {
            'audio_path': None,
            'status': 'error',
            'message': f'Error al usar voz existente: {str(e)}'
        }

def _clonar_voz_elevenlabs(texto, voz_referencia_path, output_path, api_key):
    """
    Clonar voz usando ElevenLabs API con Instant Voice Cloning (IVC)
    Compatible con plan Starter ($5/mes) y superiores
    No requiere entrenamiento previo, se puede usar inmediatamente
    """
    try:
        from elevenlabs import ElevenLabs, VoiceSettings
        from io import BytesIO
        import json
        
        # Crear cliente ElevenLabs con API key
        client = ElevenLabs(api_key=api_key)
        
        print(f"🚀 Clonando voz con ElevenLabs Instant Voice Cloning (IVC)...")
        print(f"Texto a sintetizar: {texto[:50]}...")
        print(f"Voz de referencia: {voz_referencia_path}")
        
        # Normalizar rutas
        voz_referencia_path = os.path.normpath(voz_referencia_path)
        output_path = os.path.normpath(output_path)
        
        # Verificar que el archivo de referencia existe
        if not os.path.exists(voz_referencia_path):
            return {
                'audio_path': None,
                'status': 'error',
                'message': f'Archivo de voz de referencia no encontrado: {voz_referencia_path}'
            }
        
        print(f"✅ Archivo de referencia verificado: {voz_referencia_path}")
        
        # Paso 1: Crear clon de voz instantáneo (Instant Voice Cloning)
        # IVC está disponible en plan Starter y no requiere entrenamiento
        print("📝 Creando clon de voz instantáneo (IVC)...")
        voice_name = f"temp_voice_{uuid.uuid4().hex[:8]}"
        voice_id = None
        
        try:
            # Leer el archivo de audio de referencia
            with open(voz_referencia_path, 'rb') as audio_file:
                audio_bytes = BytesIO(audio_file.read())
                
                # Crear clon de voz instantáneo usando IVC
                # IVC está disponible en plan Starter ($5/mes)
                cloned_voice = client.voices.ivc.create(
                    name=voice_name,
                    files=[audio_bytes]
                )
                voice_id = cloned_voice.voice_id
                print(f"✅ Voz clonada instantáneamente (IVC). Voice ID: {voice_id}")
                print(f"ℹ️  Nota: IVC no requiere entrenamiento, se puede usar inmediatamente")
            
        except AttributeError as attr_error:
            # Si el método ivc no existe, intentar método alternativo
            print(f"⚠️  Método IVC no disponible, intentando método alternativo...")
            try:
                # Método alternativo: usar voices.add() con archivo
                with open(voz_referencia_path, 'rb') as audio_file:
                    cloned_voice = client.voices.add(
                        name=voice_name,
                        files=[audio_file]
                    )
                    voice_id = cloned_voice.voice_id
                    print(f"✅ Voz clonada usando método alternativo. Voice ID: {voice_id}")
            except Exception as alt_error:
                print(f"❌ Error con método alternativo: {str(alt_error)}")
                raise alt_error
            
        except Exception as create_error:
            import traceback
            error_trace = traceback.format_exc()
            error_message = str(create_error)
            
            # Verificar si es un error de permisos de API key
            if 'missing_permissions' in error_message.lower() or 'voices_write' in error_message.lower():
                print(f"\n❌ ERROR DE PERMISOS DE API KEY")
                print(f"=" * 60)
                print(f"Tu API key de ElevenLabs no tiene el permiso 'voices_write' necesario.")
                print(f"\n📋 SOLUCIÓN:")
                print(f"1. Ve a: https://elevenlabs.io/app/settings/api-keys")
                print(f"2. Encuentra tu API key actual")
                print(f"3. Haz clic en 'Edit' o 'Configurar permisos'")
                print(f"4. Asegúrate de que tenga activado el permiso 'voices_write'")
                print(f"5. Guarda los cambios")
                print(f"6. Si no puedes activar el permiso, crea una nueva API key con todos los permisos")
                print(f"\n💡 Nota: El plan Starter debe permitir crear voces, verifica los permisos de tu API key.")
                print(f"🔄 Cambiando automáticamente al modelo local (más pesado pero gratis)...\n")
                raise create_error  # Se manejará en el except externo
            
            # Verificar si es un error de plan/subscripción
            if 'subscription' in error_message.lower() or 'not available' in error_message.lower():
                print(f"\n⚠️  Error: {error_message}")
                print(f"💡 Tu plan puede no incluir Instant Voice Cloning.")
                print(f"🔄 Intentando fallback al modelo local...\n")
                raise create_error  # Se manejará en el except externo
            
            print(f"❌ Error al crear clon de voz: {error_message}")
            print(f"Traceback: {error_trace}")
            raise create_error
        
        if not voice_id:
            return {
                'audio_path': None,
                'status': 'error',
                'message': 'No se pudo obtener el voice_id de la voz clonada'
            }
        
        print(f"✅ Voz clonada exitosamente. Voice ID: {voice_id}")
        
        # Paso 2: Generar audio con la voz clonada (sin necesidad de esperar entrenamiento)
        # IVC permite usar la voz inmediatamente después de crearla
        print("🎵 Generando audio con voz clonada (IVC - uso inmediato)...")
        
        try:
            # Generar audio usando text-to-speech con la voz clonada
            audio_stream = client.text_to_speech.convert(
                voice_id=voice_id,
                text=texto,
                model_id="eleven_multilingual_v2",  # Soporta español
                voice_settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.75,
                    style=0.0,
                    use_speaker_boost=True
                )
            )
            
            # Guardar el audio generado
            output_abs = os.path.abspath(output_path)
            os.makedirs(os.path.dirname(output_abs), exist_ok=True)
            
            with open(output_abs, 'wb') as f:
                for chunk in audio_stream:
                    if hasattr(chunk, 'read'):
                        f.write(chunk.read())
                    else:
                        f.write(chunk)
            
            print(f"✅ Audio generado exitosamente: {output_abs}")
            
        except Exception as tts_error:
            # Si falla la generación, intentar limpiar la voz antes de retornar error
            try:
                client.voices.delete(voice_id=voice_id)
            except:
                pass
            raise tts_error
        
        # Limpiar: eliminar la voz clonada (opcional, para no acumular voces)
        # Nota: ElevenLabs tiene límite de voces clonadas según el plan
        # Plan Starter permite un número limitado de voces
        try:
            # Eliminar la voz temporal para no acumular voces
            client.voices.delete(voice_id=voice_id)
            print(f"🧹 Voz temporal eliminada: {voice_id}")
        except Exception as cleanup_error:
            print(f"⚠️ No se pudo eliminar voz temporal: {cleanup_error}")
            print(f"ℹ️ Puedes eliminarla manualmente desde el dashboard de ElevenLabs si es necesario")
            print(f"ℹ️ Plan Starter tiene límite de voces clonadas, considera limpiar voces antiguas")
        
        if os.path.exists(output_abs):
            file_size = os.path.getsize(output_abs)
            print(f"📊 Tamaño del archivo generado: {file_size} bytes")
            return {
                'audio_path': output_abs,
                'status': 'success',
                'message': 'Voz clonada y sintetizada exitosamente con ElevenLabs Instant Voice Cloning (IVC)'
            }
        else:
            return {
                'audio_path': None,
                'status': 'error',
                'message': f'No se pudo generar el archivo de audio en: {output_abs}'
            }
            
    except ImportError as ie:
        import traceback
        error_trace = traceback.format_exc()
        print(f"ImportError: {str(ie)}")
        print(f"Traceback: {error_trace}")
        return {
            'audio_path': None,
            'status': 'error',
            'message': 'ElevenLabs no está instalado. Ejecuta: pip install elevenlabs'
        }
    except Exception as e:
        import traceback
        from elevenlabs.core.api_error import ApiError
        
        error_trace = traceback.format_exc()
        error_message = str(e)
        
        # Verificar si es un error de permisos de API key
        is_permission_error = False
        is_subscription_error = False
        
        if isinstance(e, ApiError):
            body = getattr(e, 'body', {})
            if isinstance(body, dict):
                detail = body.get('detail', {})
                if isinstance(detail, dict):
                    status = detail.get('status', '')
                    message = detail.get('message', '')
                    if 'missing_permissions' in status.lower() or 'voices_write' in message.lower():
                        is_permission_error = True
                    elif 'not available on your subscription' in message or 'can_not_use' in status:
                        is_subscription_error = True
        else:
            # Verificar en el mensaje de error
            if 'missing_permissions' in error_message.lower() or 'voices_write' in error_message.lower():
                is_permission_error = True
            elif 'subscription' in error_message.lower() or 'not available' in error_message.lower() or 'can_not_use' in error_message.lower():
                is_subscription_error = True
        
        # Verificar si es un error de permisos de API key
        if is_permission_error:
            print("\n" + "=" * 60)
            print("❌ ERROR: Permisos de API Key Insuficientes")
            print("=" * 60)
            print("\n🔑 PROBLEMA:")
            print("Tu API key de ElevenLabs no tiene el permiso 'voices_write' necesario")
            print("para crear voces clonadas.")
            print("\n📋 SOLUCIÓN PASO A PASO:")
            print("1. Ve a tu dashboard de ElevenLabs:")
            print("   https://elevenlabs.io/app/settings/api-keys")
            print("\n2. Encuentra tu API key actual (la que está en tu archivo .env)")
            print("\n3. Haz clic en 'Edit' o 'Configurar' en esa API key")
            print("\n4. Asegúrate de que tenga activado:")
            print("   ✅ voices_write (permiso para crear/modificar voces)")
            print("   ✅ voices_read (permiso para leer voces)")
            print("   ✅ text_to_speech (permiso para generar audio)")
            print("\n5. Guarda los cambios")
            print("\n6. Si no puedes editar los permisos:")
            print("   a) Crea una nueva API key")
            print("   b) Selecciona TODOS los permisos disponibles")
            print("   c) Copia la nueva API key")
            print("   d) Actualiza ELEVENLABS_API_KEY en tu archivo .env")
            print("   e) Reinicia el servidor Flask")
            print("\n💡 NOTA IMPORTANTE:")
            print("El plan Starter ($5/mes) SÍ permite crear voces con Instant Voice Cloning.")
            print("El problema es que tu API key no tiene los permisos configurados correctamente.")
            print("\n💡 ALTERNATIVA:")
            print("Puedes usar voces predefinidas de ElevenLabs para pruebas sin necesidad de clonar.")
            print("Consulta la documentación sobre cómo usar voces de prueba.\n")
            return {
                'audio_path': None,
                'status': 'error',
                'message': 'Error de permisos: Tu API key no tiene el permiso voices_write. Verifica la configuración de permisos en ElevenLabs.'
            }
        
        # Verificar si es un error de suscripción/plan
        if is_subscription_error:
            print("\n⚠️ Error: Tu plan de ElevenLabs no incluye esta funcionalidad.")
            print("💡 Instant Voice Cloning (IVC) está disponible en plan Starter ($5/mes) y superiores.")
            print("💡 Si tienes plan Starter, verifica que tu API key sea correcta.")
            print("\n💡 ALTERNATIVA:")
            print("Puedes usar voces predefinidas de ElevenLabs para pruebas sin necesidad de clonar.")
            print("Consulta la documentación sobre cómo usar voces de prueba.\n")
            return {
                'audio_path': None,
                'status': 'error',
                'message': 'Error de plan: Tu plan de ElevenLabs no incluye Instant Voice Cloning. Considera actualizar tu plan o usar voces predefinidas.'
            }
        
        # Verificar si es un error de API key o límites
        if 'api key' in error_message.lower() or 'unauthorized' in error_message.lower():
            print(f"\n❌ Error de autenticación con ElevenLabs API")
            print(f"💡 Verifica que tu ELEVENLABS_API_KEY esté correctamente configurada en el archivo .env")
            return {
                'audio_path': None,
                'status': 'error',
                'message': 'Error de autenticación: Verifica que tu ELEVENLABS_API_KEY sea correcta en el archivo .env'
            }
        
        # Verificar si es un error de límites de uso
        if 'quota' in error_message.lower() or 'limit' in error_message.lower() or 'credits' in error_message.lower():
            print(f"\n⚠️ Error: Has alcanzado el límite de uso de tu plan ElevenLabs")
            print(f"💡 Plan Starter incluye 30,000 créditos mensuales (~30 minutos de audio)")
            print(f"💡 Considera actualizar tu plan o esperar al próximo ciclo de facturación")
            return {
                'audio_path': None,
                'status': 'error',
                'message': 'Error de límite: Has alcanzado el límite de uso de tu plan ElevenLabs. Espera al próximo ciclo o actualiza tu plan.'
            }
        
        print(f"❌ Error en clonación con ElevenLabs: {error_message}")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Traceback: {error_trace}")
        return {
            'audio_path': None,
            'status': 'error',
            'message': f'Error con ElevenLabs API: {error_message}. Verifica tu API key, permisos y plan.'
        }

def _clonar_voz_local(texto, voz_referencia_path, output_path):
    """
    Clonar voz usando Coqui TTS XTTS (local, más pesado, requiere cargar modelo)
    """
    try:
        from TTS.api import TTS
        import sys
        import torch
        
        print(f"Clonando voz con Coqui TTS XTTS (modelo local)...")
        print(f"Texto a sintetizar: {texto[:50]}...")
        print(f"Voz de referencia: {voz_referencia_path}")
        print("\n⚠️ NOTA: Si es la primera vez, XTTS pedirá confirmación de licencia.")
        print("   Responde 'y' para aceptar los términos no comerciales.")
        print("   ⚠️ Este método carga modelos pesados en memoria (~1.5GB)\n")
        
        # Normalizar la ruta (convertir backslash a forward slash si es Windows)
        voz_referencia_path = os.path.normpath(voz_referencia_path)
        output_path = os.path.normpath(output_path)
        
        # Verificar que el archivo de referencia existe
        if not os.path.exists(voz_referencia_path):
            return {
                'audio_path': None,
                'status': 'error',
                'message': f'Archivo de voz de referencia no encontrado: {voz_referencia_path}'
            }
        
        print(f"Archivo de referencia verificado: {voz_referencia_path}")
        print(f"Tamaño del archivo: {os.path.getsize(voz_referencia_path)} bytes")
        
        # Fix para PyTorch 2.6+: Parches para compatibilidad
        try:
            # Parche 1: torch.load con weights_only=False
            import TTS.utils.io as tts_io
            original_load_fsspec = tts_io.load_fsspec
            
            def patched_load_fsspec(path, map_location=None, **kwargs):
                """Versión parcheada que fuerza weights_only=False para XTTS"""
                kwargs['weights_only'] = False
                return original_load_fsspec(path, map_location=map_location, **kwargs)
            
            tts_io.load_fsspec = patched_load_fsspec
            
            # Parche 2: torchaudio.load usando soundfile en lugar de torchcodec
            # torchcodec no es compatible con PyTorch CPU en Windows
            try:
                import torchaudio
                original_torchaudio_load = torchaudio.load
                
                def patched_torchaudio_load(filepath, frame_offset=0, num_frames=-1, normalize=True, channels_first=True, format=None, **kwargs):
                    """Versión parcheada que usa soundfile en lugar de torchcodec"""
                    try:
                        # Intentar usar soundfile primero
                        import soundfile as sf
                        data, sample_rate = sf.read(filepath, start=frame_offset, stop=frame_offset + num_frames if num_frames > 0 else None)
                        
                        # Convertir a torch tensor
                        import torch
                        if len(data.shape) == 1:
                            data = data.reshape(-1, 1)
                        
                        tensor = torch.from_numpy(data).float()
                        
                        if normalize:
                            tensor = tensor / (tensor.abs().max() + 1e-8)
                        
                        if channels_first:
                            tensor = tensor.t()
                        
                        return tensor, sample_rate
                    except Exception:
                        # Fallback al método original si soundfile falla
                        return original_torchaudio_load(filepath, frame_offset, num_frames, normalize, channels_first, format, **kwargs)
                
                torchaudio.load = patched_torchaudio_load
                print("✅ Parche aplicado: torchaudio usando soundfile (evita torchcodec)")
            except Exception as audio_patch_error:
                print(f"⚠️ No se pudo parchear torchaudio: {audio_patch_error}")
            
            print("✅ Parche aplicado para compatibilidad con PyTorch 2.6+")
        except Exception as patch_error:
            print(f"⚠️ No se pudo aplicar parche (puede que no sea necesario): {patch_error}")
        
        # Inicializar TTS con modelo XTTS (soporta clonación de voz)
        # XTTS es el modelo que permite clonar voces
        # La primera vez descargará el modelo (~1.5GB) y pedirá confirmación de licencia
        print("Inicializando modelo XTTS...")
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True)
        print("Modelo XTTS inicializado correctamente.")
        
        # Sintetizar el texto usando la voz de referencia
        # XTTS puede clonar la voz desde un archivo de audio de referencia
        # Nota: XTTS puede manejar varios formatos (WAV, MP3, M4A) pero funciona mejor con WAV
        print(f"Iniciando síntesis de voz con el archivo: {voz_referencia_path}")
        print(f"Guardando resultado en: {output_path}")
        
        # Convertir la ruta a string absoluto para evitar problemas
        voz_ref_abs = os.path.abspath(voz_referencia_path)
        output_abs = os.path.abspath(output_path)
        
        print(f"Ruta absoluta de referencia: {voz_ref_abs}")
        print(f"Ruta absoluta de salida: {output_abs}")
        
        tts.tts_to_file(
            text=texto,
            file_path=output_abs,
            speaker_wav=voz_ref_abs,
            language="es"  # Puedes detectar el idioma automáticamente
        )
        print(f"Síntesis completada. Verificando archivo: {output_abs}")
        
        # Verificar ambos paths (original y absoluto)
        final_path = output_abs if os.path.exists(output_abs) else output_path
        
        if os.path.exists(final_path):
            file_size = os.path.getsize(final_path)
            print(f"✅ Archivo generado exitosamente. Tamaño: {file_size} bytes")
            return {
                'audio_path': final_path,
                'status': 'success',
                'message': 'Voz clonada y sintetizada exitosamente'
            }
        elif os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Archivo generado exitosamente (path relativo). Tamaño: {file_size} bytes")
            return {
                'audio_path': output_path,
                'status': 'success',
                'message': 'Voz clonada y sintetizada exitosamente'
            }
        else:
            # Listar archivos en el directorio para debugging
            dir_path = os.path.dirname(output_abs)
            if os.path.exists(dir_path):
                files = os.listdir(dir_path)
                print(f"Archivos en el directorio {dir_path}: {files[:10]}")
            return {
                'audio_path': None,
                'status': 'error',
                'message': f'No se pudo generar el archivo de audio. Buscado en: {output_abs} y {output_path}'
            }
            
    except ImportError as ie:
        import traceback
        error_trace = traceback.format_exc()
        print(f"ImportError detectado: {str(ie)}")
        print(f"Traceback: {error_trace}")
        return {
            'audio_path': None,
            'status': 'error',
            'message': f'Coqui TTS no está instalado o falta una dependencia: {str(ie)}. Ejecuta: pip install TTS'
        }
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error en clonación de voz: {str(e)}")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Traceback completo:\n{error_trace}")
        
        # Si XTTS falla, intentar con modelo más simple
        try:
            print(f"\n🔄 Intentando con modelo alternativo (sin clonación)...")
            from TTS.api import TTS
            
            # Usar modelo más simple que no requiere clonación
            tts = TTS(model_name="tts_models/es/css10/vits", progress_bar=True)
            tts.tts_to_file(text=texto, file_path=output_path)
            
            if os.path.exists(output_path):
                print("✅ Síntesis exitosa con modelo alternativo")
                return {
                    'audio_path': output_path,
                    'status': 'success',
                    'message': 'Voz sintetizada (sin clonación, usando modelo por defecto)'
                }
        except Exception as fallback_error:
            print(f"❌ Error también con modelo alternativo: {str(fallback_error)}")
            import traceback
            print(traceback.format_exc())
        
        return {
            'audio_path': None,
            'status': 'error',
            'message': f'Error en clonación de voz: {str(e)}. Tipo: {type(e).__name__}'
        }

def detectar_inicio_voz(audio_path, umbral_db=-40, ventana_ms=100):
    """
    Detecta cuándo empieza la voz en un archivo de audio
    Analiza la energía del audio para encontrar el primer momento donde hay voz
    
    Args:
        audio_path: Ruta al archivo de audio
        umbral_db: Umbral de energía en dB para considerar que hay voz (default: -40)
        ventana_ms: Tamaño de la ventana de análisis en milisegundos (default: 100)
    
    Returns:
        int: Tiempo en milisegundos cuando empieza la voz (0 si no se detecta)
    """
    try:
        from pydub import AudioSegment
        import math
        
        audio = AudioSegment.from_file(audio_path)
        
        # Convertir a mono si es estéreo para simplificar el análisis
        if audio.channels > 1:
            audio = audio.set_channels(1)
        
        # Normalizar el audio
        audio = audio.normalize()
        
        # Calcular la energía promedio de todo el audio para usar como referencia
        # Esto ayuda a detectar mejor cuándo empieza la voz comparado con el ruido de fondo
        energia_promedio = audio.rms
        
        # Usar un porcentaje de la energía promedio como umbral
        # Si la voz es más fuerte que el 30% del promedio, consideramos que hay voz
        umbral_rms = energia_promedio * 0.3
        
        # También calcular umbral mínimo para evitar falsos positivos con ruido muy bajo
        umbral_minimo = audio.max_possible_amplitude * 0.01  # 1% del máximo
        
        # Usar el mayor de los dos umbrales
        umbral_final = max(umbral_rms, umbral_minimo)
        
        # Analizar la energía en ventanas de tiempo
        inicio_voz = 0
        encontrado = False
        ventanas_con_voz = 0  # Contador para confirmar que realmente hay voz
        
        # Procesar en ventanas de tiempo especificado
        for i in range(0, len(audio), ventana_ms):
            ventana = audio[i:i + ventana_ms]
            
            if len(ventana) == 0:
                break
            
            # Calcular el RMS (Root Mean Square) de la ventana como medida de energía
            rms = ventana.rms
            
            # Si la energía supera el umbral, consideramos que hay voz
            if rms > umbral_final:
                ventanas_con_voz += 1
                # Necesitamos al menos 2 ventanas consecutivas con voz para confirmar
                if ventanas_con_voz >= 2:
                    # Retroceder un poco para capturar el inicio real
                    inicio_voz = max(0, i - ventana_ms)
                    encontrado = True
                    break
            else:
                # Si encontramos una ventana sin voz después de detectar voz, reiniciar
                ventanas_con_voz = 0
        
        if encontrado:
            print(f"✅ Inicio de voz detectado en: {inicio_voz / 1000:.2f} segundos ({inicio_voz} ms)")
        else:
            print(f"⚠️  No se detectó inicio de voz claro (umbral: {umbral_db} dB), usando inicio del audio")
            inicio_voz = 0
        
        return inicio_voz
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"⚠️  Error al detectar inicio de voz: {str(e)}")
        print(f"Traceback: {error_trace}")
        print(f"   Usando inicio del audio (0 ms)")
        return 0

def mezclar_audio(voz_path, instrumental_path, output_path=None, voz_original_path=None):
    """
    Paso 4: Mezclar la voz clonada con el instrumental
    Sincroniza la voz sintetizada con el momento en que empieza la voz original
    
    Usa Pydub (gratis, local)
    
    Args:
        voz_path: Ruta al audio de la voz clonada/sintetizada
        instrumental_path: Ruta al audio instrumental
        output_path: Ruta donde guardar el audio final mezclado
        voz_original_path: (Opcional) Ruta al audio de la voz original separada para detectar sincronización
    
    Returns:
        dict: {
            'audio_final_path': ruta al audio final,
            'status': 'success' o 'error',
            'message': mensaje descriptivo
        }
    """
    if output_path is None:
        unique_id = uuid.uuid4().hex[:8]
        output_path = os.path.join(TEMP_DIR, f"cancion_final_{unique_id}.wav")
    
    try:
        from pydub import AudioSegment
        
        print(f"🎵 Mezclando voz e instrumental...")
        print(f"   Voz sintetizada: {voz_path}")
        print(f"   Instrumental: {instrumental_path}")
        
        # Cargar los archivos de audio
        voz = AudioSegment.from_file(voz_path)
        instrumental = AudioSegment.from_file(instrumental_path)
        
        # Detectar cuándo empieza la voz en el audio original (si está disponible)
        inicio_voz_ms = 0
        if voz_original_path and os.path.exists(voz_original_path):
            print(f"🔍 Detectando inicio de voz en: {voz_original_path}")
            inicio_voz_ms = detectar_inicio_voz(voz_original_path)
        else:
            print(f"💡 No se proporcionó voz original para sincronización, la voz empezará desde el inicio")
        
        # Si la voz original empieza después de 0ms, agregar silencio al inicio de la voz sintetizada
        if inicio_voz_ms > 0:
            print(f"⏱️  Agregando {inicio_voz_ms / 1000:.2f} segundos de silencio al inicio de la voz sintetizada")
            silencio = AudioSegment.silent(duration=inicio_voz_ms)
            voz = silencio + voz
        
        # Ajustar la duración: hacer que la voz tenga la misma duración que el instrumental
        # Si la voz es más corta, repetirla; si es más larga, cortarla
        duracion_instrumental = len(instrumental)
        duracion_voz_actual = len(voz)
        
        if duracion_voz_actual < duracion_instrumental:
            # Calcular cuántas veces necesitamos repetir la voz
            veces = (duracion_instrumental // duracion_voz_actual) + 1
            voz = (voz * veces)[:duracion_instrumental]
            print(f"🔄 Voz repetida {veces} veces para ajustar duración")
        elif duracion_voz_actual > duracion_instrumental:
            # Cortar la voz a la duración del instrumental
            voz = voz[:duracion_instrumental]
            print(f"✂️  Voz cortada a {duracion_instrumental / 1000:.2f} segundos")
        
        # Asegurar que la voz no sea más larga que el instrumental después de agregar silencio
        if len(voz) > len(instrumental):
            voz = voz[:len(instrumental)]
        
        # Ajustar niveles de volumen (opcional, puedes ajustar estos valores)
        # Reducir un poco el instrumental para que la voz se escuche mejor
        instrumental = instrumental - 3  # Reducir 3dB
        voz = voz + 2  # Aumentar 2dB la voz
        
        print(f"🎚️  Ajustando niveles: Instrumental -3dB, Voz +2dB")
        
        # Mezclar: superponer la voz sobre el instrumental
        print(f"🔀 Mezclando audio final...")
        mezcla = instrumental.overlay(voz)
        
        # Exportar el resultado
        mezcla.export(output_path, format="wav")
        
        print(f"✅ Mezcla completada: {output_path}")
        
        if os.path.exists(output_path):
            return {
                'audio_final_path': output_path,
                'status': 'success',
                'message': 'Mezcla completada exitosamente con sincronización'
            }
        else:
            return {
                'audio_final_path': None,
                'status': 'error',
                'message': 'No se pudo crear el archivo final'
            }
            
    except ImportError:
        return {
            'audio_final_path': None,
            'status': 'error',
            'message': 'Pydub no está instalado. Ejecuta: pip install pydub'
        }
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error en la mezcla: {str(e)}")
        print(f"Traceback: {error_trace}")
        return {
            'audio_final_path': None,
            'status': 'error',
            'message': f'Error en la mezcla: {str(e)}'
        }

def procesar_completo(audio_original_path, voz_referencia_path=None, texto_letra=None, 
                      usar_voz_original=False, idioma='es', traducir_a=None, modo_voz='clonar', voz_predefinida_id=None):
    """
    Procesa el flujo completo del sintetizador
    
    Args:
        audio_original_path: Ruta al audio original con música
        voz_referencia_path: Ruta al audio de referencia de la voz a clonar (None si modo_voz='predefinida')
        texto_letra: Texto de la letra (opcional, se puede extraer)
        usar_voz_original: Si True, usa la voz original separada en lugar de clonar
        idioma: Idioma de la letra original (código ISO, ej: 'es', 'en')
        traducir_a: Idioma al que traducir la letra (código ISO, ej: 'en', 'fr'). Si es None, no traduce
        modo_voz: 'clonar' o 'predefinida'
        voz_predefinida_id: Voice ID de ElevenLabs si modo_voz='predefinida'
    
    Returns:
        dict: Resultado completo del proceso con todos los pasos
    """
    resultado = {
        'paso1_separacion': None,
        'paso2_letra': None,
        'paso3_sintesis': None,
        'paso4_mezcla': None,
        'audio_final': None,
        'status': 'processing',
        'errores': []
    }
    
    try:
        # Verificar que los archivos existen
        if not os.path.exists(audio_original_path):
            resultado['errores'].append(f'Archivo de audio original no encontrado: {audio_original_path}')
            resultado['status'] = 'error'
            return resultado
        
        # Solo verificar voz_referencia_path si estamos en modo clonar
        if modo_voz == 'clonar' and voz_referencia_path and not os.path.exists(voz_referencia_path):
            resultado['errores'].append(f'Archivo de voz de referencia no encontrado: {voz_referencia_path}')
            resultado['status'] = 'error'
            return resultado
        
        # Verificar que tenemos voz_predefinida_id si estamos en modo predefinida
        if modo_voz == 'predefinida' and not voz_predefinida_id:
            resultado['errores'].append(f'Se requiere voz_predefinida_id cuando modo_voz es "predefinida"')
            resultado['status'] = 'error'
            return resultado
        
        print("=" * 50)
        print("PASO 1: Separación de Stems")
        print("=" * 50)
        # Paso 1: Separar stems
        resultado['paso1_separacion'] = separar_stems(audio_original_path)
        print(f"Resultado separación: {resultado['paso1_separacion']}")
        
        if resultado['paso1_separacion']['status'] != 'success':
            error_msg = resultado['paso1_separacion'].get('message', 'Error desconocido en separación')
            resultado['errores'].append(f'Error en separación de stems: {error_msg}')
            resultado['status'] = 'error'
            return resultado
        
        print("=" * 50)
        print("PASO 2: Generación de Letra")
        print("=" * 50)
        # Paso 2: Generar letra (con traducción opcional)
        resultado['paso2_letra'] = generar_letra(
            texto_letra=texto_letra,
            audio_path=audio_original_path,
            idioma=idioma,
            traducir_a=traducir_a  # Si se especifica, traduce la letra
        )
        print(f"Resultado letra: {resultado['paso2_letra']}")
        
        if resultado['paso2_letra']['status'] != 'success':
            error_msg = resultado['paso2_letra'].get('message', 'Error desconocido en generación de letra')
            resultado['errores'].append(f'Error en generación de letra: {error_msg}')
            resultado['status'] = 'error'
            return resultado
        
        print("=" * 50)
        print("PASO 3: Clonación/Síntesis de Voz")
        print("=" * 50)
        # Paso 3: Clonar voz, usar voz predefinida o usar voz original
        if usar_voz_original:
            voz_path = resultado['paso1_separacion']['voz_path']
            if not os.path.exists(voz_path):
                resultado['errores'].append(f'Archivo de voz separada no encontrado: {voz_path}')
                resultado['status'] = 'error'
                return resultado
            resultado['paso3_sintesis'] = {
                'audio_path': voz_path,
                'status': 'success',
                'message': 'Usando voz original separada'
            }
        elif modo_voz == 'predefinida':
            # Usar voz predefinida de ElevenLabs
            print("🎤 Usando voz predefinida de ElevenLabs...")
            from config import DevConfig
            elevenlabs_api_key = DevConfig.ELEVENLABS_API_KEY
            
            if not elevenlabs_api_key:
                resultado['errores'].append('Se requiere ELEVENLABS_API_KEY para usar voces predefinidas')
                resultado['status'] = 'error'
                return resultado
            
            # Generar ruta de salida para la voz sintetizada
            unique_id = uuid.uuid4().hex[:8]
            voz_output_path = os.path.join(TEMP_DIR, f"voz_predefinida_{unique_id}.wav")
            
            resultado['paso3_sintesis'] = usar_voz_predefinida_elevenlabs(
                texto=resultado['paso2_letra']['letra'],
                output_path=voz_output_path,
                api_key=elevenlabs_api_key,
                voice_id_predefinida=voz_predefinida_id
            )
            print(f"Resultado síntesis con voz predefinida: {resultado['paso3_sintesis']}")
            
            if resultado['paso3_sintesis']['status'] != 'success':
                error_msg = resultado['paso3_sintesis'].get('message', 'Error desconocido en síntesis')
                resultado['errores'].append(f'Error en síntesis con voz predefinida: {error_msg}')
                resultado['status'] = 'error'
                return resultado
        else:
            # Modo clonar: clonar voz del usuario
            resultado['paso3_sintesis'] = clonar_voz(
                texto=resultado['paso2_letra']['letra'],
                voz_referencia_path=voz_referencia_path
            )
            print(f"Resultado clonación: {resultado['paso3_sintesis']}")
            
            if resultado['paso3_sintesis']['status'] != 'success':
                error_msg = resultado['paso3_sintesis'].get('message', 'Error desconocido en clonación')
                resultado['errores'].append(f'Error en clonación de voz: {error_msg}')
                resultado['status'] = 'error'
                return resultado
        
        print("=" * 50)
        print("PASO 4: Mezcla Final (con sincronización)")
        print("=" * 50)
        # Paso 4: Mezclar con sincronización
        voz_path_mezcla = resultado['paso3_sintesis']['audio_path']
        instrumental_path_mezcla = resultado['paso1_separacion']['instrumental_path']
        voz_original_path = resultado['paso1_separacion'].get('voz_path')  # Voz original separada para sincronización
        
        if not os.path.exists(voz_path_mezcla):
            resultado['errores'].append(f'Archivo de voz para mezclar no encontrado: {voz_path_mezcla}')
            resultado['status'] = 'error'
            return resultado
        
        if not os.path.exists(instrumental_path_mezcla):
            resultado['errores'].append(f'Archivo instrumental no encontrado: {instrumental_path_mezcla}')
            resultado['status'] = 'error'
            return resultado
        
        # Usar la voz original separada para detectar cuándo empieza la voz y sincronizar
        resultado['paso4_mezcla'] = mezclar_audio(
            voz_path=voz_path_mezcla,
            instrumental_path=instrumental_path_mezcla,
            voz_original_path=voz_original_path  # Pasar voz original para sincronización
        )
        print(f"Resultado mezcla: {resultado['paso4_mezcla']}")
        
        if resultado['paso4_mezcla']['status'] != 'success':
            error_msg = resultado['paso4_mezcla'].get('message', 'Error desconocido en mezcla')
            resultado['errores'].append(f'Error en mezcla final: {error_msg}')
            resultado['status'] = 'error'
            return resultado
        
        resultado['audio_final'] = resultado['paso4_mezcla']['audio_final_path']
        resultado['status'] = 'success'
        
        print("=" * 50)
        print("✅ PROCESO COMPLETADO EXITOSAMENTE")
        print(f"Audio final: {resultado['audio_final']}")
        print("=" * 50)
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ ERROR GENERAL: {str(e)}")
        print(f"Traceback: {error_trace}")
        resultado['status'] = 'error'
        resultado['errores'].append(f'Error general: {str(e)}')
        resultado['traceback'] = error_trace
    
    return resultado

def limpiar_archivos_temporales():
    """Limpia los archivos temporales del sintetizador"""
    try:
        for file in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return True
    except Exception as e:
        print(f"Error al limpiar archivos temporales: {e}")
        return False

