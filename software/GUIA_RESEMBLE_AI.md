# Guía: Usar Resemble.ai en el Sintetizador

## ✅ Implementación Completada

He implementado soporte completo para Resemble.ai en tu sintetizador. Ahora el código usará Resemble.ai automáticamente si está configurado.

## 🔧 Configuración

### Paso 1: Agregar API Key al .env

Abre tu archivo `.env` y agrega:

```env
RESEMBLE_API_KEY=tu-api-key-de-resemble-aqui
```

**Ejemplo:**
```env
RESEMBLE_API_KEY=abc123def456ghi789
```

### Paso 2: Obtener tu API Key

1. Ve a: https://app.resemble.ai/
2. Inicia sesión en tu cuenta
3. Ve a: **Settings** → **API Keys**
4. Copia tu API key
5. Pégala en el archivo `.env`

### Paso 3: Reiniciar el Servidor

```bash
# Detén el servidor (Ctrl+C)
# Inicia nuevamente
python run.py
```

## 🎯 Cómo Funciona

El código ahora tiene esta **prioridad de uso**:

1. **Resemble.ai** (si `RESEMBLE_API_KEY` está configurado) ⭐ **NUEVO**
2. **ElevenLabs** (si `ELEVENLABS_API_KEY` está configurado)
3. **Coqui TTS local** (fallback automático, gratis)

## 📋 Proceso con Resemble.ai

Cuando uses el sintetizador con Resemble.ai:

1. **Crea/obtiene un proyecto** en Resemble.ai automáticamente
2. **Sube tu archivo de audio** de referencia (`Grabacion_1.wav`)
3. **Clona la voz** desde el audio
4. **Genera el audio** con el texto de la letra
5. **Descarga el resultado** automáticamente
6. **Limpia voces temporales** (opcional)

## ⚙️ Características

- ✅ **Creación automática de proyectos** - No necesitas crear proyectos manualmente
- ✅ **Clonación de voz** - Crea voces desde archivos de audio
- ✅ **Síntesis de texto** - Convierte texto en audio con la voz clonada
- ✅ **Limpieza automática** - Elimina voces temporales después de usar
- ✅ **Manejo de errores** - Fallback automático si algo falla

## 🧪 Probar

1. Asegúrate de que `RESEMBLE_API_KEY` esté en tu `.env`
2. Reinicia el servidor Flask
3. Ve al módulo Sintetizador
4. Sube:
   - Audio original (canción)
   - Voz de referencia (tu voz)
5. Haz clic en "Iniciar Procesamiento"
6. Verás en la consola: `🎤 Usando Resemble.ai API...`

## 🔍 Verificación

Para verificar que está funcionando, revisa los mensajes en la consola:

```
🎤 Usando Resemble.ai API...
🎤 Clonando voz con Resemble.ai API...
✅ Archivo de referencia verificado: uploads\Grabacion_1.wav
📁 Obteniendo proyecto de Resemble.ai...
✅ Usando proyecto existente: [project-uuid]
📤 Subiendo audio de referencia para clonar voz...
✅ Voz creada: [voice-uuid]
🎵 Generando audio con voz clonada...
✅ Clip creado: [clip-uuid]
⏳ Esperando a que el audio esté listo...
✅ Audio generado exitosamente: [ruta]
```

## ⚠️ Notas Importantes

### Requisitos del Audio de Referencia

- **Formato:** WAV, MP3, M4A, FLAC
- **Duración:** 30-60 segundos recomendado
- **Calidad:** Voz clara, sin ruido de fondo
- **Tamaño:** Máximo según límites de Resemble.ai

### Límites de Resemble.ai

- **Costo:** $0.006 por segundo de audio generado
- **Planes:** Desde $29/mes
- **Tiempo de procesamiento:** Puede tardar 10-30 segundos

### Si Algo Falla

Si Resemble.ai falla por cualquier razón:
- El código automáticamente hará **fallback a Coqui TTS local**
- Verás un mensaje: `🔄 Cambiando automáticamente al modelo local...`
- El procesamiento continuará sin interrupciones

## 🆘 Solución de Problemas

### Error: "requests no está instalado"
```bash
pip install requests
```

### Error: "API key inválida"
- Verifica que copiaste la API key completa
- Verifica que no hay espacios extra
- Verifica que la API key esté activa en Resemble.ai

### Error: "Timeout al generar audio"
- Resemble.ai puede tardar más en procesar
- El código espera hasta 60 segundos
- Si tarda más, intenta con un texto más corto

### Error: "No se pudo crear proyecto"
- Verifica que tu cuenta de Resemble.ai esté activa
- Verifica que tengas permisos para crear proyectos
- Revisa los límites de tu plan

## 📞 Recursos

- **Dashboard de Resemble.ai:** https://app.resemble.ai/
- **Documentación API:** https://www.resemble.ai/docs/
- **Soporte:** https://www.resemble.ai/support

---

**¡Listo para usar!** 🎉


