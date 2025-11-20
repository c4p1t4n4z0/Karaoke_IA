# Solución: Error de Permisos de API Key de ElevenLabs

## 🔴 Error Encontrado

```
missing_permissions: The API key you used is missing the permission voices_write
```

## 📋 Solución Paso a Paso

### Paso 1: Acceder a la Configuración de API Keys

1. Ve a tu cuenta de ElevenLabs: https://elevenlabs.io/
2. Inicia sesión con tu cuenta
3. Ve a: **Settings** → **API Keys**
   - O directamente: https://elevenlabs.io/app/settings/api-keys

### Paso 2: Verificar tu API Key Actual

1. En la lista de API keys, encuentra la que estás usando
2. Verifica cuál es (puedes ver los últimos caracteres)
3. Compara con la que tienes en tu archivo `.env`

### Paso 3: Editar Permisos de la API Key

**Opción A: Editar API Key Existente**

1. Haz clic en **"Edit"** o **"Configurar"** en tu API key
2. En la sección de permisos, busca la categoría **"Voices"** o **"Voice Management"**
3. Asegúrate de activar:
   - ✅ **Voices: Write** (permiso para crear/modificar voces) ⚠️ **ESENCIAL**
   - ✅ **Voices: Read** o **Access** (permiso para leer voces)
   - ✅ **Text-to-speech: Access** (ya lo tienes activado ✓)
   - ✅ **Voice generation: Access** (ya lo tienes activado ✓)
4. **IMPORTANTE:** Si no ves la sección "Voices", puede estar en:
   - Una sección colapsada (haz clic para expandir)
   - Una pestaña diferente
   - Con el nombre "Voice Management" o "Voice Library"
5. Guarda los cambios

**Opción B: Crear Nueva API Key (Recomendado si no puedes editar)**

1. Haz clic en **"Create API Key"** o **"Nueva API Key"**
2. Dale un nombre descriptivo (ej: "Sintetizador Karaoke")
3. **IMPORTANTE:** Selecciona **TODOS** los permisos disponibles:
   - ✅ voices_write
   - ✅ voices_read
   - ✅ text_to_speech
   - ✅ voices_delete (opcional, para limpiar voces temporales)
4. Haz clic en **"Create"** o **"Crear"**
5. **COPIA LA API KEY INMEDIATAMENTE** (solo se muestra una vez)

### Paso 4: Actualizar el Archivo .env

1. Abre el archivo `.env` en la raíz de tu proyecto
2. Busca la línea:
   ```env
   ELEVENLABS_API_KEY=tu-api-key-anterior
   ```
3. Reemplázala con tu nueva API key:
   ```env
   ELEVENLABS_API_KEY=sk-tu-nueva-api-key-aqui
   ```
4. Guarda el archivo

### Paso 5: Reiniciar el Servidor Flask

1. Detén el servidor Flask (Ctrl+C en la terminal)
2. Inicia el servidor nuevamente:
   ```bash
   python run.py
   ```

### Paso 6: Probar Nuevamente

1. Ve al módulo Sintetizador en tu aplicación
2. Sube los archivos de audio
3. Inicia el procesamiento
4. Debería funcionar correctamente ahora

---

## ✅ Verificación

Para verificar que los permisos están correctos:

1. Ve a: https://elevenlabs.io/app/settings/api-keys
2. Revisa que tu API key tenga activado al menos:
   - `voices_write`
   - `voices_read`
   - `text_to_speech`

---

## 🔍 Notas Importantes

### ¿Por qué ocurre este error?

- Las API keys de ElevenLabs tienen permisos granulares para seguridad
- Por defecto, algunas API keys pueden no tener todos los permisos activados
- El permiso `voices_write` es necesario para crear voces clonadas

### ¿El plan Starter permite esto?

**SÍ**, el plan Starter ($5/mes) **SÍ permite** crear voces con Instant Voice Cloning (IVC).
El problema no es el plan, sino los permisos de tu API key.

### ¿Qué pasa si no puedo editar los permisos?

Si no puedes editar los permisos de tu API key existente:
1. Crea una nueva API key con todos los permisos
2. Reemplaza la antigua en tu archivo `.env`
3. Puedes eliminar la API key antigua si quieres (opcional)

---

## 🆘 Si el Problema Persiste

Si después de seguir estos pasos el error continúa:

1. **Verifica que la API key esté correctamente copiada** (sin espacios extra)
2. **Verifica que el archivo .env esté en la raíz del proyecto**
3. **Verifica que reiniciaste el servidor Flask** después de cambiar el .env
4. **Revisa la consola** para ver si hay otros errores
5. **Prueba crear una API key completamente nueva** con todos los permisos

---

## 🔄 Fallback Automático

Mientras tanto, el sistema automáticamente:
- Detectará el error de permisos
- Mostrará este mensaje informativo
- Cambiará automáticamente al modelo local (Coqui TTS)
- El procesamiento continuará, aunque será más lento

El modelo local funciona sin API keys, pero es más pesado y requiere más recursos.

---

## 📞 Enlaces Útiles

- **Dashboard de API Keys:** https://elevenlabs.io/app/settings/api-keys
- **Documentación de ElevenLabs:** https://elevenlabs.io/docs
- **Soporte de ElevenLabs:** https://elevenlabs.io/support

---

**Última actualización:** Noviembre 2024

