# Configurar OpenAI para Transcripción de Audio

Ahora puedes usar la **API de OpenAI (Whisper API)** para transcribir audio a texto en lugar de Whisper local. Esto es más rápido y preciso.

## 🚀 Ventajas de usar OpenAI Whisper API

✅ **Más rápido** - No necesita descargar ni cargar modelos locales  
✅ **Más preciso** - Mejor calidad de transcripción  
✅ **Menos recursos** - No consume memoria/CPU local  
✅ **Más idiomas** - Mejor soporte multilingüe  
✅ **Automático** - Sin configuración adicional  

## 📋 Cómo Configurarlo

### Paso 1: Agregar API Key al archivo `.env`

Abre tu archivo `.env` y agrega tu API key de OpenAI:

```env
OPENAI_API_KEY=sk-tu-api-key-aqui
```

**Ejemplo:**
```env
OPENAI_API_KEY=sk-proj-1234567890abcdefghijklmnopqrstuvwxyz
```

### Paso 2: Instalar la librería de OpenAI

Si aún no tienes instalada la librería oficial de OpenAI:

```bash
pip install openai
```

O instala todas las dependencias:

```bash
pip install -r requirements.txt
```

### Paso 3: Reiniciar el servidor Flask

Después de agregar la API key, reinicia tu servidor Flask:

```bash
python .\run.py
```

## 🔄 Cómo Funciona

El sistema ahora usa una **prioridad automática**:

1. **Primero intenta usar OpenAI Whisper API** (si `OPENAI_API_KEY` está configurada)
2. **Si no hay API key o falla, usa Whisper local** (fallback automático)

### Cuando usas OpenAI API:
- Verás: `🚀 Usando OpenAI Whisper API para transcribir...`
- Más rápido y preciso
- Requiere conexión a internet
- Tiene costo (~$0.006 por minuto)

### Cuando usas Whisper local:
- Verás: `📦 Usando Whisper local para transcribir...`
- Gratis pero más lento
- Requiere instalar `openai-whisper`
- Descarga modelos pesados localmente

## 💰 Costo de OpenAI Whisper API

- **Precio**: ~$0.006 por minuto de audio
- **Ejemplo**: Una canción de 3 minutos = ~$0.018 (menos de 2 centavos)

### Límites gratuitos

OpenAI ofrece créditos gratuitos al registrarte:
- Generalmente $5-18 USD en créditos
- Suficiente para muchas transcripciones

## 🎯 Verificar que Funciona

Cuando proceses un audio, verás en la consola:

```
🚀 Usando OpenAI Whisper API para transcribir: /ruta/al/audio.mp3
🎤 Transcribiendo con OpenAI Whisper API...
   Idioma: es
   Audio: /ruta/al/audio.mp3
✅ Transcripción completada con OpenAI Whisper API
   Letra extraída: 150 caracteres
```

Si no tienes API key configurada, verás:

```
📦 Usando Whisper local para transcribir: /ruta/al/audio.mp3
💡 Tip: Agrega OPENAI_API_KEY en .env para usar API de OpenAI (más rápida y precisa)
```

## 🔧 Solución de Problemas

### Error: "No module named 'openai'"

**Solución:**
```bash
pip install openai
```

### Error: "Incorrect API key provided"

**Solución:**
1. Verifica que tu API key esté correcta en el archivo `.env`
2. Asegúrate de que empiece con `sk-`
3. Copia y pega la API key exactamente como aparece en tu cuenta de OpenAI

### Error: "Insufficient quota"

**Solución:**
1. Verifica que tengas créditos disponibles en tu cuenta de OpenAI
2. Ve a: https://platform.openai.com/usage
3. Si no tienes créditos, agrega fondos o espera a que se renueven

### No funciona y cae a Whisper local

Si el sistema siempre usa Whisper local:
1. Verifica que `OPENAI_API_KEY` esté en tu archivo `.env`
2. Asegúrate de que no esté comentada (sin `#` al inicio)
3. Reinicia el servidor Flask después de cambiar el `.env`

## 📝 Notas Importantes

1. **El fallback es automático**: Si OpenAI falla por cualquier razón, automáticamente usa Whisper local
2. **Whisper local sigue disponible**: No necesitas eliminarlo, funciona como respaldo
3. **Ambos métodos funcionan**: Puedes alternar entre API y local según tu necesidad
4. **Sin API key**: Si no configuras `OPENAI_API_KEY`, el sistema seguirá funcionando con Whisper local

## 🔗 Enlaces Útiles

- **Dashboard de OpenAI**: https://platform.openai.com/
- **API Keys de OpenAI**: https://platform.openai.com/api-keys
- **Uso y Facturación**: https://platform.openai.com/usage
- **Documentación de Whisper API**: https://platform.openai.com/docs/guides/speech-to-text



