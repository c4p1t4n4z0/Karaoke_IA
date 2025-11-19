# Formatos de Audio para Voz de Referencia

## 📋 Formatos Soportados

### Formatos Recomendados (Mejor Compatibilidad):
- **WAV** ⭐ **Más Recomendado**
  - Mejor calidad
  - Sin compresión
  - Compatible con todas las librerías

- **MP3**
  - Ampliamente soportado
  - Buena calidad si es de alta bitrate (192kbps o más)

- **FLAC**
  - Sin pérdida de calidad
  - Buena opción si tienes espacio

### Formatos También Soportados:
- **M4A** / **AAC**
- **OGG**
- **OPUS**

### Formatos NO Soportados:
- Formatos de video (MP4, AVI, etc.) - solo audio
- Formatos muy antiguos o raros

---

## 🎯 Especificaciones Recomendadas

### Duración:
- **Mínimo:** 10 segundos
- **Recomendado:** 30-60 segundos
- **Máximo:** 5 minutos (pero no es necesario)

### Calidad del Audio:
- **Sample Rate:** 16 kHz o superior (recomendado: 22.05 kHz o 44.1 kHz)
- **Bit Depth:** 16-bit o superior
- **Canales:** Mono o Estéreo (ambos funcionan)

### Contenido del Audio:
- ✅ **Ideal:** Voz clara hablando o cantando
- ✅ **Aceptable:** Voz con música de fondo suave
- ❌ **Evitar:** Mucho ruido de fondo, eco, distorsión

---

## 💡 Consejos para Obtener Mejores Resultados

### 1. Calidad de la Grabación:
- Graba en un ambiente silencioso
- Usa un micrófono de buena calidad si es posible
- Evita ecos o reverberación excesiva

### 2. Contenido:
- Habla o canta de forma natural
- No necesitas decir algo específico, solo hablar normalmente
- Si vas a cantar, canta en el mismo estilo que quieres que se replique

### 3. Preparación del Archivo:
- Si el audio tiene mucho ruido, usa un editor de audio para limpiarlo
- Normaliza el volumen (no muy bajo ni muy alto)
- Asegúrate de que la voz sea claramente audible

---

## 🔧 Conversión de Formatos

Si necesitas convertir tu audio a WAV (recomendado), puedes usar:

### Con FFmpeg (línea de comandos):
```bash
ffmpeg -i tu_audio.mp3 -ar 22050 -ac 1 -sample_fmt s16 tu_audio.wav
```

### Con Audacity (interfaz gráfica):
1. Abre tu archivo
2. File → Export → Export as WAV
3. Selecciona: 16-bit, Mono o Stereo, 22050 Hz o 44100 Hz

### Con herramientas online:
- CloudConvert: https://cloudconvert.com/
- Online-Convert: https://www.online-convert.com/

---

## 📊 Comparación de Formatos

| Formato | Calidad | Tamaño | Compatibilidad | Recomendación |
|---------|---------|--------|----------------|---------------|
| **WAV** | ⭐⭐⭐⭐⭐ | Grande | Excelente | ⭐⭐⭐⭐⭐ |
| **FLAC** | ⭐⭐⭐⭐⭐ | Mediano | Buena | ⭐⭐⭐⭐ |
| **MP3 (320kbps)** | ⭐⭐⭐⭐ | Pequeño | Excelente | ⭐⭐⭐⭐ |
| **MP3 (192kbps)** | ⭐⭐⭐ | Pequeño | Excelente | ⭐⭐⭐ |
| **M4A** | ⭐⭐⭐⭐ | Pequeño | Buena | ⭐⭐⭐ |
| **OGG** | ⭐⭐⭐⭐ | Pequeño | Buena | ⭐⭐⭐ |

---

## ⚠️ Problemas Comunes

### "El formato no es compatible"
- **Solución:** Convierte a WAV usando FFmpeg o Audacity

### "El audio es muy corto"
- **Solución:** Necesitas al menos 10 segundos de audio

### "La calidad de clonación es mala"
- **Causas posibles:**
  - Audio con mucho ruido de fondo
  - Voz muy distorsionada o con eco
  - Audio de muy baja calidad (bitrate muy bajo)
- **Solución:** Graba un nuevo audio con mejor calidad

### "El audio es muy largo"
- **Solución:** No es necesario más de 60 segundos. Puedes cortar el audio a la parte más clara

---

## 🎤 Ejemplo de Audio Ideal

Un audio de referencia ideal sería:
- **Formato:** WAV
- **Duración:** 30-45 segundos
- **Contenido:** Tú hablando o cantando de forma natural
- **Calidad:** Sin ruido de fondo, voz clara
- **Sample Rate:** 22050 Hz o 44100 Hz
- **Bitrate:** 16-bit o superior

---

## 📝 Resumen Rápido

✅ **Usa:** WAV, MP3 (alta calidad), o FLAC  
✅ **Duración:** 30-60 segundos  
✅ **Calidad:** Voz clara, sin ruido  
❌ **Evita:** Formatos raros, audio con mucho ruido, duraciones muy cortas (<10 seg)

---

**Nota:** El sistema convertirá automáticamente el audio al formato necesario internamente, pero usar WAV desde el inicio da mejores resultados.




