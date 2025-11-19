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

def generar_letra(texto_letra=None, audio_path=None, idioma='es'):
    """
    Paso 2: Generar o extraer letra y alinearla con la melodía
    Usa Whisper para extraer letra del audio (gratis, local)
    
    Args:
        texto_letra: Texto de la letra proporcionado por el usuario (opcional)
        audio_path: Ruta al audio para extraer letra automáticamente (opcional)
        idioma: Idioma de la letra (código ISO, ej: 'es', 'en')
    
    Returns:
        dict: {
            'letra': texto de la letra,
            'alineamiento': datos de alineamiento temporal,
            'status': 'success' o 'error',
            'message': mensaje descriptivo
        }
    """
    try:
        # Si ya se proporcionó la letra, usarla directamente
        if texto_letra and texto_letra.strip():
            return {
                'letra': texto_letra.strip(),
                'alineamiento': {},
                'status': 'success',
                'message': 'Letra proporcionada por el usuario'
            }
        
        # Si no hay letra pero hay audio, extraerla con Whisper
        if audio_path and os.path.exists(audio_path):
            import whisper
            
            print(f"Extrayendo letra del audio con Whisper: {audio_path}")
            
            # Cargar modelo Whisper (base es un buen balance entre velocidad y calidad)
            # Modelos disponibles: tiny, base, small, medium, large
            model = whisper.load_model("base")
            
            # Transcribir el audio
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
            
            result = model.transcribe(
                audio_path,
                language=whisper_lang,
                task="transcribe"
            )
            
            letra_extraida = result["text"].strip()
            
            if letra_extraida:
                return {
                    'letra': letra_extraida,
                    'alineamiento': {
                        'segments': result.get('segments', []),
                        'language': result.get('language', idioma)
                    },
                    'status': 'success',
                    'message': 'Letra extraída exitosamente del audio'
                }
            else:
                return {
                    'letra': '',
                    'alineamiento': {},
                    'status': 'error',
                    'message': 'No se pudo extraer letra del audio'
                }
        
        # Si no hay letra ni audio, error
        return {
            'letra': '',
            'alineamiento': {},
            'status': 'error',
            'message': 'No se proporcionó letra ni audio para extraerla'
        }
        
    except ImportError:
        return {
            'letra': texto_letra or '',
            'alineamiento': {},
            'status': 'error',
            'message': 'Whisper no está instalado. Ejecuta: pip install openai-whisper'
        }
    except Exception as e:
        return {
            'letra': texto_letra or '',
            'alineamiento': {},
            'status': 'error',
            'message': f'Error al extraer letra: {str(e)}'
        }

def clonar_voz(texto, voz_referencia_path, output_path=None):
    """
    Paso 3: Clonar la voz del usuario y sintetizar la letra
    Usa Coqui TTS con XTTS (gratis, local)
    
    Args:
        texto: Texto a sintetizar con la voz clonada
        voz_referencia_path: Ruta al audio de referencia de la voz a clonar
        output_path: Ruta donde guardar el audio generado
    
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
    
    try:
        from TTS.api import TTS
        import sys
        import torch
        
        print(f"Clonando voz con Coqui TTS XTTS...")
        print(f"Texto a sintetizar: {texto[:50]}...")
        print(f"Voz de referencia: {voz_referencia_path}")
        print("\n⚠️ NOTA: Si es la primera vez, XTTS pedirá confirmación de licencia.")
        print("   Responde 'y' para aceptar los términos no comerciales.\n")
        
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

def mezclar_audio(voz_path, instrumental_path, output_path=None):
    """
    Paso 4: Mezclar la voz clonada con el instrumental
    Usa Pydub (gratis, local)
    
    Args:
        voz_path: Ruta al audio de la voz clonada
        instrumental_path: Ruta al audio instrumental
        output_path: Ruta donde guardar el audio final mezclado
    
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
        
        print(f"Mezclando voz e instrumental...")
        print(f"Voz: {voz_path}")
        print(f"Instrumental: {instrumental_path}")
        
        # Cargar los archivos de audio
        # Pydub puede manejar diferentes formatos automáticamente
        voz = AudioSegment.from_file(voz_path)
        instrumental = AudioSegment.from_file(instrumental_path)
        
        # Ajustar la duración: hacer que la voz tenga la misma duración que el instrumental
        # Si la voz es más corta, repetirla; si es más larga, cortarla
        if len(voz) < len(instrumental):
            # Repetir la voz hasta alcanzar la duración del instrumental
            veces = (len(instrumental) // len(voz)) + 1
            voz = (voz * veces)[:len(instrumental)]
        elif len(voz) > len(instrumental):
            # Cortar la voz a la duración del instrumental
            voz = voz[:len(instrumental)]
        
        # Ajustar niveles de volumen (opcional, puedes ajustar estos valores)
        # Reducir un poco el instrumental para que la voz se escuche mejor
        instrumental = instrumental - 3  # Reducir 3dB
        voz = voz + 2  # Aumentar 2dB la voz
        
        # Mezclar: superponer la voz sobre el instrumental
        mezcla = instrumental.overlay(voz)
        
        # Exportar el resultado
        mezcla.export(output_path, format="wav")
        
        if os.path.exists(output_path):
            return {
                'audio_final_path': output_path,
                'status': 'success',
                'message': 'Mezcla completada exitosamente'
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
        return {
            'audio_final_path': None,
            'status': 'error',
            'message': f'Error en la mezcla: {str(e)}'
        }

def procesar_completo(audio_original_path, voz_referencia_path, texto_letra=None, 
                      usar_voz_original=False, idioma='es'):
    """
    Procesa el flujo completo del sintetizador
    
    Args:
        audio_original_path: Ruta al audio original con música
        voz_referencia_path: Ruta al audio de referencia de la voz a clonar
        texto_letra: Texto de la letra (opcional, se puede extraer)
        usar_voz_original: Si True, usa la voz original separada en lugar de clonar
        idioma: Idioma de la letra
    
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
        
        if not os.path.exists(voz_referencia_path):
            resultado['errores'].append(f'Archivo de voz de referencia no encontrado: {voz_referencia_path}')
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
        # Paso 2: Generar letra
        resultado['paso2_letra'] = generar_letra(
            texto_letra=texto_letra,
            audio_path=audio_original_path,
            idioma=idioma
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
        # Paso 3: Clonar voz o usar voz original
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
        else:
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
        print("PASO 4: Mezcla Final")
        print("=" * 50)
        # Paso 4: Mezclar
        voz_path_mezcla = resultado['paso3_sintesis']['audio_path']
        instrumental_path_mezcla = resultado['paso1_separacion']['instrumental_path']
        
        if not os.path.exists(voz_path_mezcla):
            resultado['errores'].append(f'Archivo de voz para mezclar no encontrado: {voz_path_mezcla}')
            resultado['status'] = 'error'
            return resultado
        
        if not os.path.exists(instrumental_path_mezcla):
            resultado['errores'].append(f'Archivo instrumental no encontrado: {instrumental_path_mezcla}')
            resultado['status'] = 'error'
            return resultado
        
        resultado['paso4_mezcla'] = mezclar_audio(
            voz_path=voz_path_mezcla,
            instrumental_path=instrumental_path_mezcla
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

