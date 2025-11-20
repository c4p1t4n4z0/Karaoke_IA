# Guía: Activar Permiso "Voices: Write" en ElevenLabs

## 🔍 Problema

Tu API key tiene estos permisos activados:
- ✅ Text-to-speech: Access
- ✅ Voice generation: Access
- ❌ **FALTA: Voices: Write** (necesario para crear voces)

## 📋 Solución: Encontrar y Activar "Voices: Write"

### Método 1: Buscar en la Interfaz

1. Ve a: https://elevenlabs.io/app/settings/api-keys
2. Haz clic en **"Edit"** en tu API key
3. Busca en la lista de permisos una sección que diga:
   - **"Voices"**
   - **"Voice Management"**
   - **"Voice Library"**
   - **"Voice Operations"**

4. En esa sección, busca:
   - **"Write"** o **"Create"** o **"Add"**
   - Actívalo marcando la casilla o cambiando a "Write"

### Método 2: Si No Aparece la Sección "Voices"

Si no ves una sección específica de "Voices", puede ser que:

1. **La interfaz esté colapsada:**
   - Busca flechas (▼) o iconos de expandir
   - Haz clic para expandir todas las secciones

2. **Esté en otra categoría:**
   - Revisa la sección "Administration"
   - Revisa la sección "User"
   - Revisa la sección "Workspace"

3. **Necesites crear una nueva API key:**
   - Ve a "Create API Key"
   - Selecciona **"Full Access"** o **"All Permissions"**
   - Esto debería incluir automáticamente Voices: Write

### Método 3: Crear Nueva API Key con Todos los Permisos (RECOMENDADO)

Si no puedes encontrar o activar el permiso Voices: Write:

1. Ve a: https://elevenlabs.io/app/settings/api-keys
2. Haz clic en **"Create API Key"**
3. Dale un nombre: "Sintetizador - Full Access"
4. **Selecciona "Full Access" o "All Permissions"** (si está disponible)
5. Si no hay opción de "Full Access", activa manualmente:
   - ✅ Todas las opciones de "Text-to-speech"
   - ✅ Todas las opciones de "Voice generation"
   - ✅ **Voices: Write** (si aparece)
   - ✅ **Voices: Read** (si aparece)
   - ✅ Todas las demás opciones que veas
6. Haz clic en **"Create"**
7. **COPIA LA API KEY INMEDIATAMENTE** (solo se muestra una vez)
8. Actualiza tu archivo `.env`:
   ```env
   ELEVENLABS_API_KEY=sk-tu-nueva-api-key-completa
   ```
9. Reinicia el servidor Flask

## 🔍 Verificación Visual

Cuando tengas los permisos correctos, deberías ver algo como:

```
Voices
├── Read: ✅ Access
└── Write: ✅ Write  ← ESTE ES EL QUE NECESITAS
```

O en formato de tabla:

| Permiso | Acceso |
|---------|--------|
| Voices: Read | ✅ Access |
| Voices: Write | ✅ Write | ← ESTE ES EL QUE NECESITAS |

## ⚠️ Nota Importante

Si después de buscar exhaustivamente **NO encuentras** la opción "Voices: Write", puede ser que:

1. **Tu plan Starter tenga limitaciones:**
   - Algunos planes pueden no permitir crear voces programáticamente
   - Verifica en: https://elevenlabs.io/pricing

2. **La interfaz haya cambiado:**
   - ElevenLabs puede haber reorganizado los permisos
   - Contacta soporte: https://elevenlabs.io/support

3. **Necesites usar el dashboard web:**
   - Puede que necesites crear voces desde el dashboard web primero
   - Luego usar esas voces con la API

## 🆘 Alternativa: Usar Dashboard Web

Si no puedes activar Voices: Write, puedes:

1. Crear la voz manualmente desde el dashboard:
   - Ve a: https://elevenlabs.io/app/voices
   - Haz clic en "Add Voice" → "Instant Voice Cloning"
   - Sube tu archivo de audio de referencia
   - Obtén el Voice ID de la voz creada

2. Modificar el código para usar voces existentes en lugar de crear nuevas

## 📞 Contactar Soporte

Si el problema persiste:

1. Contacta soporte de ElevenLabs: https://elevenlabs.io/support
2. Pregunta específicamente: "¿Cómo activo el permiso Voices: Write en mi API key del plan Starter?"
3. Menciona que necesitas crear voces programáticamente con Instant Voice Cloning

---

**Última actualización:** Noviembre 2024


