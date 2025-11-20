# Traducción de Letras con OpenAI GPT (ChatGPT)

Con tu API key de OpenAI (ChatGPT), ahora puedes **traducir letras de canciones a cualquier idioma** usando la misma API key que usas para la transcripción.

## 🌍 ¿Qué puede hacer?

✅ **Transcribir audio a texto** (Whisper API)  
✅ **Traducir texto a cualquier idioma** (GPT-3.5-turbo)  
✅ **Todo con la misma API key de OpenAI**

## 🎯 Cómo Funciona

1. **Transcripción**: Extrae la letra del audio usando Whisper API
2. **Traducción**: Traduce la letra a otro idioma usando GPT (ChatGPT)
3. **Síntesis**: Sintetiza la letra traducida con la voz elegida

## 📋 Cómo Usar la Traducción

### Desde el Formulario Web

1. **Sube tu audio original** (canción)
2. **Elige tu voz** (predefinida o clonada)
3. **Marca la casilla "Traducir la letra a otro idioma"**
4. **Selecciona el idioma destino** del dropdown
5. **Procesa**

El sistema automáticamente:
- Transcribe el audio (si no proporcionaste letra)
- Traduce la letra al idioma elegido
- Sintetiza la letra traducida con la voz elegida

### Ejemplo de Flujo

```
Audio en español → Transcripción (Whisper) → Letra en español
→ Traducción (GPT) → Letra en inglés → Síntesis (ElevenLabs) → Audio final
```

## 💰 Costo de la Traducción

- **GPT-3.5-turbo**: ~$0.0015 por 1K tokens
- **Ejemplo**: Una letra de canción (~500 palabras) = ~$0.002 (muy económico)
- **Muy barato** comparado con la síntesis de voz

## 🌐 Idiomas Soportados

La traducción funciona con **cualquier idioma** que GPT-3.5 soporte, incluyendo:

### Idiomas Principales
- ✅ Español
- ✅ Inglés
- ✅ Francés
- ✅ Alemán
- ✅ Italiano
- ✅ Portugués

### Otros Idiomas
- ✅ Japonés
- ✅ Coreano
- ✅ Chino
- ✅ Ruso
- ✅ Árabe
- ✅ Hindi
- ✅ Y muchos más...

## 🔧 Configuración Requerida

Solo necesitas:
- ✅ `OPENAI_API_KEY` configurada en tu archivo `.env`
- ✅ La misma API key sirve para transcripción y traducción

## 📝 Ejemplo de Uso Programático

Si quieres usar la traducción directamente en código:

```python
from proyecto.controllers.SintetizadorController import traducir_letra_con_openai
from config import DevConfig

# Traducir una letra
resultado = traducir_letra_con_openai(
    texto="Voy manejando por la noche y pienso en ti",
    idioma_origen='es',
    idioma_destino='en',
    api_key=DevConfig.OPENAI_API_KEY
)

if resultado['status'] == 'success':
    print(f"Texto traducido: {resultado['texto_traducido']}")
```

## 💡 Ventajas de Usar GPT para Traducción

✅ **Mejor calidad** que traductores automáticos básicos  
✅ **Mantiene formato** (saltos de línea, estrofas)  
✅ **Intenta mantener rima** cuando es posible  
✅ **Mismo precio** que usar GPT para otras tareas  
✅ **Misma API key** que la transcripción  

## ⚠️ Notas Importantes

1. **Requiere API key**: Necesitas `OPENAI_API_KEY` configurada
2. **Tiene costo**: Usa créditos de OpenAI (pero es muy económico)
3. **Fallback**: Si falla la traducción, se usa la letra original
4. **Calidad**: GPT-3.5 es muy bueno para traducción, pero puede no ser perfecta al 100%

## 🎯 Casos de Uso

✅ **Cantar en otro idioma**: Transcribe una canción en español y tradúcela a inglés para cantarla  
✅ **Karaoke multilingüe**: Crea versiones de la misma canción en diferentes idiomas  
✅ **Aprender idiomas**: Escucha cómo se pronuncian canciones en otros idiomas  
✅ **Contenido internacional**: Prepara contenido de audio para audiencias internacionales  

## 📊 Costo Total Estimado

Para una canción completa (3 minutos):
- **Transcripción (Whisper)**: ~$0.018
- **Traducción (GPT-3.5)**: ~$0.002
- **Síntesis (ElevenLabs)**: ~$1.50-5.00 (según plan)
- **Total**: ~$1.52-5.02 por canción completa traducida

## 🔗 Enlaces Útiles

- **API de OpenAI**: https://platform.openai.com/
- **Precios de GPT-3.5**: https://openai.com/pricing
- **Documentación de ChatGPT API**: https://platform.openai.com/docs/guides/text-generation



