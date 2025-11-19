# API Keys Necesarias para el Módulo Sintetizador

Esta es una lista completa de todas las API keys que podrías necesitar según la opción que elijas.

---

## 📋 Resumen Rápido

### Opción 100% Gratis (Sin API Keys)
✅ **No necesitas ninguna API key** - Todo funciona localmente
- Separación: Spleeter/Demucs (local)
- Letra: Whisper (local)
- Clonación: Coqui TTS/XTTS (local)
- Mezcla: Pydub (local)

### Opción Híbrida (1 API Key)
🔑 **Necesitas: ElevenLabs API Key**
- Separación: Spleeter (local, gratis)
- Letra: Whisper (local, gratis)
- Clonación: **ElevenLabs** (API, pago)
- Mezcla: Pydub (local, gratis)

### Opción Profesional (2-3 API Keys)
🔑 **Necesitas: ElevenLabs + LALAL.AI + (Opcional) OpenAI**
- Separación: **LALAL.AI** (API, pago)
- Letra: Whisper (local) + **OpenAI GPT** (opcional, para generar letras)
- Clonación: **ElevenLabs** (API, pago)
- Mezcla: Pydub (local, gratis)

---

## 🔑 API Keys Detalladas

### 1. ElevenLabs API Key ⭐ RECOMENDADO

**¿Para qué?** Clonación y síntesis de voz (Paso 3)

**¿Es necesaria?** Solo si quieres usar ElevenLabs en lugar de soluciones locales

**Cómo obtenerla:**
1. Ve a: https://elevenlabs.io/
2. Crea una cuenta: https://elevenlabs.io/app/sign-up
3. Ve a tu perfil → API Keys
4. Genera una nueva API key
5. Cópiala

**Costo:**
- Plan Starter: $5/mes (30,000 caracteres)
- Plan Creator: $22/mes (100,000 caracteres)
- Plan Pro: $99/mes (500,000 caracteres)

**Variable de entorno:**
```env
ELEVENLABS_API_KEY=sk-tu-api-key-aqui
```

**Ejemplo de API Key:**
```
sk_1234567890abcdefghijklmnopqrstuvwxyz
```

---

### 2. LALAL.AI API Key

**¿Para qué?** Separación de stems (voz/instrumental) - Paso 1

**¿Es necesaria?** Solo si quieres usar LALAL.AI en lugar de Spleeter/Demucs local

**Cómo obtenerla:**
1. Ve a: https://www.lalal.ai/
2. Crea una cuenta
3. Ve a: https://www.lalal.ai/api
4. Genera tu API key
5. Cópiala

**Costo:**
- ~$0.10 por canción procesada
- Planes desde $15/mes

**Variable de entorno:**
```env
LALALAI_API_KEY=tu-api-key-aqui
```

**Ejemplo de API Key:**
```
lalal_1234567890abcdefghijklmnopqrstuvwxyz
```

---

### 3. OpenAI API Key (Opcional)

**¿Para qué?** Generación de letras nuevas (Paso 2) - Solo si quieres generar letras en lugar de solo extraerlas

**¿Es necesaria?** NO - Solo si quieres la funcionalidad de generar letras nuevas con IA

**Cómo obtenerla:**
1. Ve a: https://platform.openai.com/
2. Crea una cuenta o inicia sesión
3. Ve a: https://platform.openai.com/api-keys
4. Crea una nueva API key
5. Cópiala (solo se muestra una vez, guárdala bien)

**Costo:**
- GPT-3.5: ~$0.002 por 1K tokens
- GPT-4: ~$0.03 por 1K tokens
- Tienes créditos gratis al registrarte

**Variable de entorno:**
```env
OPENAI_API_KEY=sk-tu-api-key-aqui
```

**Ejemplo de API Key:**
```
sk-proj-1234567890abcdefghijklmnopqrstuvwxyz
```

---

### 4. Resemble.ai API Key (Alternativa a ElevenLabs)

**¿Para qué?** Clonación de voz (Paso 3) - Alternativa a ElevenLabs

**¿Es necesaria?** Solo si prefieres Resemble.ai sobre ElevenLabs

**Cómo obtenerla:**
1. Ve a: https://www.resemble.ai/
2. Crea una cuenta
3. Ve a tu dashboard → API Keys
4. Genera una nueva API key

**Costo:**
- $0.006 por segundo de audio generado
- Planes desde $29/mes

**Variable de entorno:**
```env
RESEMBLE_API_KEY=tu-api-key-aqui
```

---

### 5. PlayHT API Key (Alternativa a ElevenLabs)

**¿Para qué?** Clonación de voz (Paso 3) - Otra alternativa

**¿Es necesaria?** Solo si prefieres PlayHT

**Cómo obtenerla:**
1. Ve a: https://play.ht/
2. Crea una cuenta
3. Ve a Settings → API Keys
4. Genera una nueva API key

**Costo:**
- Planes desde $19/mes

**Variable de entorno:**
```env
PLAYHT_API_KEY=tu-api-key-aqui
PLAYHT_USER_ID=tu-user-id-aqui
```

---

## 📝 Configuración en el Archivo .env

Agrega las API keys que vayas a usar a tu archivo `.env`:

```env
# ============================================
# API KEYS PARA SINTETIZADOR
# ============================================

# ElevenLabs (Recomendado para clonación de voz)
ELEVENLABS_API_KEY=sk-tu-api-key-aqui

# LALAL.AI (Para separación de stems - opcional)
LALALAI_API_KEY=tu-api-key-aqui

# OpenAI (Para generación de letras - opcional)
OPENAI_API_KEY=sk-proj-tu-api-key-aqui

# Resemble.ai (Alternativa a ElevenLabs - opcional)
RESEMBLE_API_KEY=tu-api-key-aqui

# PlayHT (Alternativa a ElevenLabs - opcional)
PLAYHT_API_KEY=tu-api-key-aqui
PLAYHT_USER_ID=tu-user-id-aqui
```

---

## 🎯 Recomendación por Presupuesto

### Presupuesto $0 (Gratis)
**API Keys necesarias:** ❌ Ninguna
- Usa Spleeter, Whisper, Coqui TTS localmente
- Todo funciona sin conexión a internet (después de instalar modelos)

### Presupuesto $5-10/mes
**API Keys necesarias:** ✅ **Solo ElevenLabs**
```env
ELEVENLABS_API_KEY=sk-tu-api-key-aqui
```
- Mejor calidad de clonación de voz
- Resto funciona localmente

### Presupuesto $30-50/mes
**API Keys necesarias:** ✅ **ElevenLabs + LALAL.AI**
```env
ELEVENLABS_API_KEY=sk-tu-api-key-aqui
LALALAI_API_KEY=tu-api-key-aqui
```
- Mejor calidad en separación y clonación
- Procesamiento más rápido

### Presupuesto $50+/mes
**API Keys necesarias:** ✅ **ElevenLabs + LALAL.AI + OpenAI**
```env
ELEVENLABS_API_KEY=sk-tu-api-key-aqui
LALALAI_API_KEY=tu-api-key-aqui
OPENAI_API_KEY=sk-proj-tu-api-key-aqui
```
- Máxima calidad y funcionalidades

---

## 🔒 Seguridad de las API Keys

### ⚠️ IMPORTANTE:
1. **NUNCA** subas tu archivo `.env` a GitHub
2. **NUNCA** compartas tus API keys públicamente
3. **NUNCA** hardcodees las keys en el código
4. **SIEMPRE** usa variables de entorno
5. **SIEMPRE** agrega `.env` a tu `.gitignore`

### Verificar que .env está en .gitignore:
```bash
# Asegúrate de que .gitignore contiene:
.env
*.env
.env.local
```

---

## 📚 Cómo Usar las API Keys en el Código

Ejemplo en `SintetizadorController.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Obtener API key
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')

if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY no está configurada en .env")

# Usar la API key
from elevenlabs import set_api_key
set_api_key(ELEVENLABS_API_KEY)
```

---

## ✅ Checklist de Configuración

- [ ] Decidir qué servicios usar (gratis vs pago)
- [ ] Crear cuentas en los servicios elegidos
- [ ] Obtener las API keys necesarias
- [ ] Agregar las keys al archivo `.env`
- [ ] Verificar que `.env` está en `.gitignore`
- [ ] Probar que las keys funcionan
- [ ] Implementar las funciones en `SintetizadorController.py`

---

## 🆘 Problemas Comunes

### "API Key no encontrada"
- Verifica que el archivo `.env` existe
- Verifica que la variable tiene el nombre correcto
- Verifica que ejecutaste `load_dotenv()` antes de usar la key

### "API Key inválida"
- Verifica que copiaste la key completa
- Verifica que no hay espacios extra
- Verifica que la key no expiró (algunas keys tienen expiración)

### "Límite de uso excedido"
- Revisa tu plan y límites
- Considera actualizar tu plan
- O usa la versión local/gratis

---

## 📞 Enlaces Útiles

- **ElevenLabs:** https://elevenlabs.io/app/sign-up
- **LALAL.AI:** https://www.lalal.ai/
- **OpenAI:** https://platform.openai.com/api-keys
- **Resemble.ai:** https://www.resemble.ai/
- **PlayHT:** https://play.ht/

---

**Nota:** Empieza con la opción gratis (sin API keys) para probar, y luego agrega las que necesites según tus necesidades de calidad y presupuesto.




