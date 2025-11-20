# Cómo Obtener las Voces Predefinidas de ElevenLabs

Las **voces predefinidas** son voces que ya están disponibles en ElevenLabs y no necesitas crearlas ni subirlas. Estas voces vienen incluidas con tu cuenta de ElevenLabs.

## 🎯 ¿De dónde vienen las voces predefinidas?

Las voces predefinidas **ya están en tu cuenta de ElevenLabs** cuando te registras. Son voces públicas que ElevenLabs proporciona a todos los usuarios para que puedas probar el servicio sin necesidad de clonar tu voz.

## 🔍 Cómo Ver Todas las Voces Predefinidas Disponibles

### Opción 1: Usando el Script Automático (Recomendado)

Ejecuta el script que he creado para listar todas las voces disponibles:

```bash
python listar_voces_elevenlabs.py
```

Este script:
- ✅ Se conecta a tu cuenta de ElevenLabs
- ✅ Lista todas las voces predefinidas disponibles
- ✅ Muestra los Voice IDs que necesitas para el formulario
- ✅ Genera código HTML para agregar más voces al dropdown

### Opción 2: Desde el Dashboard Web de ElevenLabs

1. Ve a tu dashboard de ElevenLabs: **https://elevenlabs.io/app/voices**
2. Inicia sesión con tu cuenta
3. Navega a la sección **"Pre-made Voices"** o **"Library"**
4. Ahí verás todas las voces predefinidas disponibles
5. Haz clic en cada voz para escucharla
6. Copia el **Voice ID** de la voz que quieras usar

### Opción 3: Usando la API de ElevenLabs Directamente

Puedes usar Python para obtener la lista:

```python
from elevenlabs import ElevenLabs
from config import DevConfig

# Crear cliente
client = ElevenLabs(api_key=DevConfig.ELEVENLABS_API_KEY)

# Obtener todas las voces
voices = client.voices.get_all()

# Filtrar voces predefinidas (category='premade')
for voice in voices.voices:
    category = getattr(voice, 'category', '')
    if 'premade' in category.lower():
        print(f"Nombre: {voice.name}")
        print(f"Voice ID: {voice.voice_id}")
        print()
```

## 📋 Voces Predefinidas Más Populares

Ya están incluidas en el formulario estas voces populares:

### Voces Femeninas
- **Rachel** (`21m00Tcm4TlvDq8ikWAM`) - Voz femenina profesional
- **Domi** (`AZnzlk1XvdvUeBnXmlld`) - Voz femenina expresiva
- **Bella** (`EXAVITQu4vr4xnSDxMaL`) - Voz femenina suave
- **Elli** (`MF3mGyEYCl7XYWbV9V6O`) - Voz femenina joven

### Voces Masculinas
- **Josh** (`TxGEqnHWrfWFTfGW9XjX`) - Voz masculina profesional
- **Arnold** (`VR6AewLTigWG4xSOukaG`) - Voz masculina profunda
- **Adam** (`pNInz6obpgDQGcFmaJgB`) - Voz masculina suave
- **Sam** (`yoZ06aMxZJJ28mfd3POQ`) - Voz masculina joven

## ➕ Cómo Agregar Más Voces al Formulario

Si encuentras otras voces predefinidas que te gustan, puedes agregarlas al formulario:

### Paso 1: Obtener el Voice ID

Ejecuta el script `listar_voces_elevenlabs.py` o busca en el dashboard de ElevenLabs.

### Paso 2: Agregar al Formulario

Edita el archivo `software/proyecto/views/templates/sintetizador.html` y busca la sección del dropdown de voces predefinidas. Agrega la nueva opción:

```html
<select id="vozPredefinida" name="vozPredefinida" class="form-control">
    <optgroup label="Voces Femeninas">
        <option value="21m00Tcm4TlvDq8ikWAM">Rachel - Voz femenina profesional</option>
        <!-- ... otras voces ... -->
        <!-- Agrega aquí tu nueva voz -->
        <option value="NUEVO_VOICE_ID">Nombre de la Voz - Descripción</option>
    </optgroup>
    <!-- ... resto del código ... -->
</select>
```

### Paso 3: Reiniciar el Servidor

Después de agregar la voz, reinicia tu servidor Flask para que los cambios surtan efecto.

## ⚠️ Importante

1. **Las voces predefinidas ya están disponibles**: No necesitas crear ni subir nada
2. **Requieren API key**: Necesitas tener configurada `ELEVENLABS_API_KEY` en tu `.env`
3. **Funcionan con todos los planes**: Incluso con el plan gratuito (si está disponible)
4. **No requieren clonación**: Son más rápidas porque no necesitan entrenamiento

## 🔗 Enlaces Útiles

- **Dashboard de ElevenLabs**: https://elevenlabs.io/app/voices
- **Documentación de API**: https://elevenlabs.io/docs/api-reference
- **Script para listar voces**: `python listar_voces_elevenlabs.py`

## 💡 Consejo

Si quieres probar rápidamente sin configurar nada, usa las voces que ya están en el formulario (Rachel, Domi, Josh, etc.). Si encuentras otras que prefieras, puedes agregarlas usando los pasos anteriores.




