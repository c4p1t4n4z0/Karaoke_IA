# Cómo Verificar y Obtener una API Key Válida de OpenAI

## ❌ Error que estás viendo

```
Error code: 401 - Incorrect API key provided
```

Esto significa que la API key en tu archivo `.env` no es válida o está mal configurada.

## ✅ Solución Paso a Paso

### Paso 1: Verificar tu API key actual

1. Abre tu archivo `.env`
2. Busca la línea que dice:
   ```env
   OPENAI_API_KEY=sk-proj-...
   ```
3. Verifica que:
   - No tenga espacios antes o después del `=`
   - No esté comentada (sin `#` al inicio)
   - Esté completa (no cortada)
   - Empiece con `sk-` o `sk-proj-`

### Paso 2: Obtener una API key nueva de OpenAI

1. **Ve a OpenAI Platform**: https://platform.openai.com/
2. **Inicia sesión** con tu cuenta (o crea una si no tienes)
3. **Ve a API Keys**: https://platform.openai.com/api-keys
4. **Crea una nueva API key**:
   - Haz clic en "Create new secret key"
   - Dale un nombre (ej: "Karaoke IA")
   - **Copia la API key inmediatamente** (solo se muestra una vez)
   - La API key debe verse así: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Paso 3: Actualizar tu archivo `.env`

1. Abre tu archivo `.env`
2. Reemplaza la línea de `OPENAI_API_KEY` con tu nueva API key:
   ```env
   OPENAI_API_KEY=sk-proj-tu-api-key-real-aqui
   ```
   **Importante:**
   - Sin comillas
   - Sin espacios
   - Sin `#` al inicio
   - La API key completa en una sola línea

### Paso 4: Verificar que tienes créditos

1. Ve a: https://platform.openai.com/usage
2. Verifica que tengas créditos disponibles
3. Si no tienes créditos, agrega fondos o usa la prueba gratuita

### Paso 5: Reiniciar el servidor

Después de actualizar el `.env`, reinicia tu servidor Flask:

```bash
python .\run.py
```

## 🔍 Verificar que Funciona

Cuando proceses un audio, deberías ver:

```
🚀 Usando OpenAI Whisper API para transcribir: uploads\audio.mp3
🎤 Transcribiendo con OpenAI Whisper API...
   Idioma: es
   Audio: uploads\audio.mp3
✅ Transcripción completada con OpenAI Whisper API
   Letra extraída: 150 caracteres
```

**NO deberías ver:**
```
❌ Error con OpenAI Whisper API: Error code: 401
```

## ⚠️ Errores Comunes

### Error: "Incorrect API key provided"

**Causas posibles:**
- API key incorrecta o mal copiada
- API key expirada o revocada
- API key de otro servicio (no de OpenAI)

**Solución:**
1. Obtén una nueva API key desde https://platform.openai.com/api-keys
2. Verifica que sea de OpenAI (empieza con `sk-`)
3. Cópiala completa sin espacios

### Error: "Insufficient quota"

**Causa:** No tienes créditos en tu cuenta de OpenAI

**Solución:**
1. Ve a: https://platform.openai.com/usage
2. Agrega fondos a tu cuenta
3. O usa la prueba gratuita si está disponible

### Error: API key muy larga o con caracteres extraños

**Causa:** La API key fue mal copiada o tiene caracteres invisibles

**Solución:**
1. Obtén una nueva API key
2. Cópiala directamente desde OpenAI (sin editar)
3. Pégalo directamente en el `.env`

## 💡 Nota Importante

**Mientras tanto, el sistema funciona con Whisper local** (gratis pero más lento). El fallback automático está funcionando correctamente, así que tu aplicación sigue funcionando. Solo necesitas configurar la API key correcta si quieres usar OpenAI para obtener mejor velocidad y precisión.

## 🔗 Enlaces Útiles

- **Obtener API Key**: https://platform.openai.com/api-keys
- **Verificar Créditos**: https://platform.openai.com/usage
- **Documentación**: https://platform.openai.com/docs/guides/speech-to-text
- **Soporte**: https://help.openai.com/



