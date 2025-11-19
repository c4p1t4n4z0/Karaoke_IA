# Servicios de IA Necesarios para el Módulo Sintetizador

Este documento describe los servicios de IA que necesitas configurar para que el módulo Sintetizador funcione completamente.

## Resumen del Proceso

1. **Separación de Stems** → Extraer voz e instrumental
2. **Generación de Letra** → Extraer o generar letra
3. **Clonación de Voz** → Clonar tu voz y sintetizar
4. **Mezcla Final** → Combinar todo

---

## 1. Separación de Stems (Voz / Instrumental)

### Opción A: Spleeter (Open Source, Local) ⭐ Recomendado para empezar
```bash
pip install spleeter
```

**Ventajas:**
- Gratis
- Funciona localmente
- No requiere API keys

**Desventajas:**
- Requiere GPU para mejor rendimiento
- Calidad media

**Implementación:**
```python
from spleeter.separator import Separator

separator = Separator('spleeter:2stems-16kHz')
separator.separate_to_file(audio_path, output_dir)
```

### Opción B: Demucs (Open Source, Mejor Calidad)
```bash
pip install demucs
```

**Ventajas:**
- Mejor calidad que Spleeter
- Gratis
- Open source

**Desventajas:**
- Más lento
- Requiere más recursos

### Opción C: LALAL.AI API (Servicio Pago)
**Costo:** ~$0.10 por canción
**API:** https://www.lalal.ai/api

**Ventajas:**
- Excelente calidad
- Rápido
- API simple

**Desventajas:**
- Requiere pago
- Límites de uso

---

## 2. Generación de Letra / Alineamiento

### Opción A: Whisper (Open Source) ⭐ Recomendado
```bash
pip install openai-whisper
```

**Ventajas:**
- Gratis
- Excelente para extracción de letra
- Múltiples idiomas

**Implementación:**
```python
import whisper

model = whisper.load_model("base")
result = model.transcribe(audio_path)
letra = result["text"]
```

### Opción B: OpenAI GPT (Para Generación)
**Costo:** ~$0.002 por 1K tokens
**API:** https://platform.openai.com/

**Uso:** Si el usuario quiere generar letra nueva en lugar de extraerla

### Opción C: Montreal Forced Aligner (Alineamiento)
```bash
pip install montreal-forced-alignment
```

**Uso:** Para alinear la letra con la melodía temporalmente

---

## 3. Clonación / Síntesis de Voz

### Opción A: ElevenLabs API ⭐ Más Recomendado
**Costo:** $5/mes (plan básico) - 30,000 caracteres
**API:** https://elevenlabs.io/

**Ventajas:**
- Excelente calidad
- Fácil de usar
- Clonación rápida

**Implementación:**
```python
from elevenlabs import generate, clone, set_api_key

set_api_key("TU_API_KEY")
voice = clone(name="Mi Voz", files=[voz_referencia_path])
audio = generate(text=letra, voice=voice)
```

**Registro:** https://elevenlabs.io/app/sign-up

### Opción B: Coqui TTS (Open Source)
```bash
pip install TTS
```

**Ventajas:**
- Gratis
- Funciona localmente
- Open source

**Desventajas:**
- Requiere más configuración
- Calidad variable

### Opción C: Resemble.ai API
**Costo:** $0.006 por segundo de audio
**API:** https://www.resemble.ai/

**Ventajas:**
- Buena calidad
- API robusta

### Opción D: XTTS (Open Source, Local)
```bash
pip install TTS[all]
```

**Ventajas:**
- Gratis
- Buena calidad
- Funciona offline

---

## 4. Mezcla Final

### Opción A: Pydub (Simple) ⭐ Recomendado
```bash
pip install pydub
```

**Ya está en requirements.txt**

**Implementación:**
```python
from pydub import AudioSegment

voz = AudioSegment.from_wav(voz_path)
instrumental = AudioSegment.from_wav(instrumental_path)
mezcla = instrumental.overlay(voz)
mezcla.export(output_path, format="wav")
```

### Opción B: Librosa + Soundfile (Más Control)
```bash
pip install librosa soundfile
```

**Ventajas:**
- Más control sobre la mezcla
- Mejor para ajustes finos

---

## Configuración Recomendada para Empezar

### Stack Mínimo (Gratis):
1. **Separación:** Spleeter
2. **Letra:** Whisper
3. **Clonación:** Coqui TTS o XTTS
4. **Mezcla:** Pydub

### Stack Profesional (Pago):
1. **Separación:** Demucs o LALAL.AI
2. **Letra:** Whisper + GPT (opcional)
3. **Clonación:** ElevenLabs
4. **Mezcla:** Pydub o Librosa

---

## Variables de Entorno Necesarias

Agrega estas variables a tu archivo `.env`:

```env
# ElevenLabs (si usas)
ELEVENLABS_API_KEY=tu_api_key_aqui

# OpenAI (si usas GPT para letras)
OPENAI_API_KEY=tu_api_key_aqui

# LALAL.AI (si usas)
LALALAI_API_KEY=tu_api_key_aqui
```

---

## Pasos para Implementar

1. **Elegir servicios:** Decide qué servicios usar según tu presupuesto
2. **Obtener API keys:** Registrate en los servicios que requieran pago
3. **Instalar dependencias:** Agrega las librerías necesarias a `requirements.txt`
4. **Implementar funciones:** Completa las funciones en `SintetizadorController.py`
5. **Probar:** Prueba con archivos de ejemplo
6. **Optimizar:** Ajusta parámetros según resultados

---

## Costos Estimados

### Opción Gratis:
- $0/mes (todo local, requiere GPU para mejor rendimiento)

### Opción Híbrida:
- ElevenLabs: $5/mes (30K caracteres)
- Total: ~$5/mes

### Opción Profesional:
- ElevenLabs: $22/mes (100K caracteres)
- LALAL.AI: ~$10/mes (100 canciones)
- Total: ~$32/mes

---

## Notas Importantes

- **GPU Recomendada:** Para procesamiento local (Spleeter, Demucs, Coqui TTS)
- **Tiempo de Procesamiento:** Local puede ser más lento pero gratis
- **Calidad:** Servicios pagos generalmente ofrecen mejor calidad
- **Límites:** Revisa los límites de uso de cada API

---

## Próximos Pasos

1. Revisa el código en `SintetizadorController.py`
2. Elige los servicios que mejor se adapten a tus necesidades
3. Obtén las API keys necesarias
4. Completa las implementaciones en las funciones TODO
5. Prueba el flujo completo

¡Buena suerte con la implementación! 🎵




