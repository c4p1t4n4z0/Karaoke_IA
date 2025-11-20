# Solución Alternativa: Usar Voz Existente de ElevenLabs

## 🎯 Problema

Tu plan Starter incluye "Clonación instantánea de voz", pero tu API key no tiene el permiso `voices_write` para crear voces programáticamente.

## ✅ Solución: Crear Voz desde Dashboard y Usarla

Si no puedes activar el permiso `voices_write` en tu API key, puedes crear la voz manualmente desde el dashboard web y luego usarla en el código.

### Paso 1: Crear Voz desde el Dashboard Web

1. Ve a: https://elevenlabs.io/app/voices
2. Haz clic en **"Add Voice"** o **"Agregar Voz"**
3. Selecciona **"Instant Voice Cloning"** o **"Clonación Instantánea"**
4. Sube tu archivo de audio de referencia:
   - El mismo archivo que usarías (`Grabacion_1.wav`)
   - Formato: WAV, MP3, M4A, FLAC
   - Duración recomendada: 30-60 segundos
5. Dale un nombre a la voz (ej: "Mi Voz Karaoke")
6. Espera a que se procese (puede tardar unos segundos)
7. **COPIA EL VOICE ID** de la voz creada
   - Se muestra en la URL o en los detalles de la voz
   - Formato: algo como `21m00Tcm4TlvDq8ikWAM` o similar

### Paso 2: Configurar Voice ID en el Código

**Opción A: Variable de Entorno (Recomendado)**

1. Agrega al archivo `.env`:
   ```env
   ELEVENLABS_API_KEY=sk-tu-api-key-aqui
   ELEVENLABS_VOICE_ID=tu-voice-id-aqui
   ```

2. Modifica `config.py` para leer el Voice ID:
   ```python
   ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "").strip()
   ```

3. Modifica `SintetizadorController.py` para usar el Voice ID si está configurado

**Opción B: Modificar el Código Directamente**

Puedo modificar el código para que detecte automáticamente si hay un Voice ID configurado y lo use en lugar de intentar crear una nueva voz.

### Paso 3: Usar la Voz en el Sintetizador

Una vez configurado, el código:
1. Verificará si hay un `ELEVENLABS_VOICE_ID` configurado
2. Si existe, usará esa voz directamente (sin intentar crear una nueva)
3. Si no existe, intentará crear una nueva voz (y fallará si no tienes permisos)
4. Si falla, hará fallback al modelo local

## 🔄 Ventajas de Esta Solución

- ✅ No necesitas el permiso `voices_write`
- ✅ Funciona con plan Starter
- ✅ Solo necesitas crear la voz una vez
- ✅ Puedes reutilizar la misma voz para múltiples canciones
- ✅ Más rápido (no crea voz cada vez)

## 📋 Pasos Rápidos

1. **Crear voz en dashboard:** https://elevenlabs.io/app/voices
2. **Copiar Voice ID** de la voz creada
3. **Agregar a .env:**
   ```env
   ELEVENLABS_VOICE_ID=tu-voice-id-aqui
   ```
4. **Actualizar código** para usar voz existente
5. **Probar sintetizador**

## 🆘 ¿Dónde Encontrar el Voice ID?

El Voice ID se encuentra en:

1. **En la URL del dashboard:**
   - Ve a: https://elevenlabs.io/app/voices
   - Haz clic en tu voz
   - El Voice ID aparece en la URL: `.../voices/[VOICE_ID]`

2. **En los detalles de la voz:**
   - Haz clic en tu voz
   - Busca "Voice ID" o "ID" en los detalles
   - Copia el ID (formato: cadena de caracteres alfanuméricos)

3. **Usando la API (si tienes permisos de lectura):**
   ```python
   from elevenlabs import ElevenLabs
   client = ElevenLabs(api_key="tu-api-key")
   voices = client.voices.get_all()
   for voice in voices.voices:
       print(f"{voice.name}: {voice.voice_id}")
   ```

## 💡 Nota Importante

- Puedes crear múltiples voces desde el dashboard
- Cada voz tiene su propio Voice ID
- Puedes cambiar el Voice ID en `.env` cuando quieras usar otra voz
- La voz creada desde el dashboard se mantiene y puedes reutilizarla

---

**¿Quieres que modifique el código para que use automáticamente el Voice ID si está configurado?**


