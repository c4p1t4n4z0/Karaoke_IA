# Guía de Instalación - Sintetizador (Opción Gratis)

Esta guía te ayudará a instalar y configurar el módulo Sintetizador usando solo herramientas gratuitas y locales.

## 📦 Dependencias Necesarias

### 1. Instalar las librerías Python

```bash
# Activa tu entorno virtual primero
# Windows:
.\env\Scripts\activate

# Linux/Mac:
source env/bin/activate

# Luego instala las dependencias:
pip install spleeter openai-whisper TTS librosa soundfile
```

### 2. Dependencias del Sistema

#### FFmpeg (Requerido para procesamiento de audio)
- **Windows:** 
  - Descarga desde: https://ffmpeg.org/download.html
  - O usa: `choco install ffmpeg` (si tienes Chocolatey)
  - Agrega FFmpeg al PATH del sistema

- **Linux:**
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

- **Mac:**
  ```bash
  brew install ffmpeg
  ```

#### CUDA (Opcional, para GPU - acelera el procesamiento)
Si tienes una GPU NVIDIA, instala CUDA para acelerar:
- **Windows/Linux:** https://developer.nvidia.com/cuda-downloads
- **Mac:** No soporta CUDA (usa CPU)

## 🔧 Verificación de Instalación

### Verificar que todo está instalado:

```python
# Ejecuta esto en Python para verificar:
import spleeter
import whisper
import TTS
import librosa
import soundfile
import pydub

print("✅ Todas las dependencias están instaladas")
```

## 📝 Notas Importantes

### Spleeter
- **Primera ejecución:** Spleeter descargará los modelos automáticamente (~100MB)
- **Tiempo de procesamiento:** 1-5 minutos por canción (depende de tu CPU/GPU)
- **Calidad:** Buena para pruebas, aceptable para producción

### Whisper
- **Primera ejecución:** Descargará el modelo "base" (~150MB)
- **Modelos disponibles:** tiny, base, small, medium, large
- **Recomendación:** Usa "base" para balance velocidad/calidad
- **Tiempo:** 30 segundos - 2 minutos por canción

### Coqui TTS (XTTS)
- **Primera ejecución:** Descargará el modelo XTTS (~1.5GB)
- **Tiempo de descarga:** 5-10 minutos (solo la primera vez)
- **Tiempo de síntesis:** 10-30 segundos por canción
- **Requisitos:** Al menos 4GB RAM libre

### Pydub
- Ya está en requirements.txt
- Requiere FFmpeg instalado en el sistema

## 🚀 Probar la Instalación

### Test rápido:

```python
# test_sintetizador.py
from proyecto.controllers.SintetizadorController import (
    separar_stems, 
    generar_letra, 
    clonar_voz, 
    mezclar_audio
)

# Test 1: Separación (necesitas un archivo de audio)
# resultado = separar_stems("ruta/a/tu/audio.mp3")
# print(resultado)

# Test 2: Extracción de letra
# resultado = generar_letra(audio_path="ruta/a/tu/audio.mp3", idioma="es")
# print(resultado)

print("✅ Módulo Sintetizador listo para usar")
```

## ⚠️ Problemas Comunes

### "Spleeter no encuentra los modelos"
- Ejecuta manualmente: `spleeter separate -h` para forzar la descarga
- Los modelos se guardan en: `~/.spleeter/` (Linux/Mac) o `C:\Users\TuUsuario\.spleeter\` (Windows)

### "Whisper no puede descargar el modelo"
- Verifica tu conexión a internet
- Los modelos se guardan en: `~/.cache/whisper/`

### "TTS no puede descargar XTTS"
- Verifica que tienes suficiente espacio (necesita ~2GB)
- Los modelos se guardan en: `~/.local/share/tts/`

### "FFmpeg no encontrado"
- Verifica que FFmpeg está en tu PATH
- Ejecuta: `ffmpeg -version` para verificar

### "Error de memoria"
- XTTS requiere bastante RAM
- Cierra otras aplicaciones
- O usa un modelo más pequeño de TTS

## 📊 Tiempos Estimados de Procesamiento

Para una canción de 3 minutos:

| Paso | Tiempo (CPU) | Tiempo (GPU) |
|------|--------------|--------------|
| Separación (Spleeter) | 2-5 min | 30-60 seg |
| Extracción Letra (Whisper) | 1-2 min | 20-30 seg |
| Clonación Voz (XTTS) | 30-60 seg | 15-30 seg |
| Mezcla (Pydub) | 5-10 seg | 5-10 seg |
| **Total** | **4-8 min** | **1-2 min** |

## 🎯 Próximos Pasos

1. ✅ Instala todas las dependencias
2. ✅ Verifica que todo funciona
3. ✅ Prueba con un archivo de audio pequeño primero
4. ✅ Si los resultados son buenos, considera actualizar a versiones de pago para mejor calidad

## 💡 Consejos

- **Empieza con archivos pequeños** (30 segundos) para probar
- **Usa formato WAV** para mejor calidad
- **Asegúrate de tener buena calidad de audio de referencia** para la clonación
- **La voz de referencia debe ser clara** (sin ruido de fondo)

¡Buena suerte con las pruebas! 🎵




