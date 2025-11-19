# Notas sobre la Licencia de XTTS (Coqui TTS)

## ⚠️ Primera Ejecución - Confirmación de Licencia

Cuando uses XTTS por primera vez, verás este mensaje:

```
> You must confirm the following:
> "I have purchased a commercial license from Coqui: licensing@coqui.ai"
> "Otherwise, I agree to the terms of the non-commercial CPML: https://coqui.ai/cpml" - [y/n]
```

### ¿Qué hacer?

**Responde con `y` (yes)** para aceptar los términos de la licencia no comercial.

### ¿Qué significa esto?

- **Licencia No Comercial (CPML):** Puedes usar XTTS gratis para proyectos no comerciales
- **Licencia Comercial:** Si vas a usar esto comercialmente, necesitas comprar una licencia

### Para Uso No Comercial (Gratis):
- ✅ Proyectos personales
- ✅ Investigación
- ✅ Educación
- ✅ Desarrollo de prototipos

### Requiere Licencia Comercial:
- ❌ Productos comerciales
- ❌ Servicios de pago
- ❌ Uso en producción comercial

## 📥 Descarga del Modelo

Después de confirmar, XTTS descargará el modelo automáticamente:

- **Tamaño:** ~1.5 GB
- **Ubicación:** `C:\Users\TuUsuario\AppData\Local\tts\tts_models--multilingual--multi-dataset--xtts_v2`
- **Tiempo:** 5-15 minutos (depende de tu conexión)
- **Solo la primera vez:** Después de descargar, se reutiliza

## 🔄 Proceso Automático

El proceso se detendrá esperando tu confirmación. Una vez que respondas `y`, continuará automáticamente.

## 💡 Solución para Evitar la Confirmación Manual

Si quieres evitar la confirmación manual en el futuro, puedes:

1. **Aceptar automáticamente** (solo para desarrollo):
   - Modificar el código para aceptar automáticamente
   - ⚠️ Solo si estás seguro de que es para uso no comercial

2. **Pre-descargar el modelo**:
   ```python
   from TTS.api import TTS
   tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
   # Esto descargará el modelo si no está presente
   ```

## 📝 Nota Importante

Esta confirmación solo aparece **la primera vez** que usas XTTS. Después de aceptar y descargar el modelo, no volverá a aparecer.

## 🔗 Enlaces Útiles

- **Términos de Licencia:** https://coqui.ai/cpml
- **Licencia Comercial:** licensing@coqui.ai
- **Documentación XTTS:** https://github.com/coqui-ai/TTS

---

**Resumen:** Responde `y` cuando te lo pida, espera a que descargue el modelo (~1.5GB), y después funcionará automáticamente.


