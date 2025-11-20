# Audios de Prueba de ElevenLabs

Si no tienes audios propios o quieres probar el sistema antes de clonar tu voz, puedes usar **voces predefinidas de ElevenLabs** para hacer pruebas.

## 🎤 Voces Predefinidas Disponibles

ElevenLabs proporciona varias voces predefinidas que puedes usar para pruebas sin necesidad de clonar tu voz. Estas voces ya están entrenadas y listas para usar.

### Voces Femeninas

| Nombre | Voice ID | Descripción | Uso Recomendado |
|--------|----------|-------------|-----------------|
| **Rachel** | `21m00Tcm4TlvDq8ikWAM` | Voz femenina profesional y clara | General, narración |
| **Domi** | `AZnzlk1XvdvUeBnXmlld` | Voz femenina expresiva y dinámica | Música, expresivo |
| **Bella** | `EXAVITQu4vr4xnSDxMaL` | Voz femenina suave y cálida | Relajante, íntimo |
| **Elli** | `MF3mGyEYCl7XYWbV9V6O` | Voz femenina joven y fresca | Contemporáneo, joven |

### Voces Masculinas

| Nombre | Voice ID | Descripción | Uso Recomendado |
|--------|----------|-------------|-----------------|
| **Josh** | `TxGEqnHWrfWFTfGW9XjX` | Voz masculina profesional | General, narración |
| **Arnold** | `VR6AewLTigWG4xSOukaG` | Voz masculina profunda y autoritaria | Dramático, serio |
| **Adam** | `pNInz6obpgDQGcFmaJgB` | Voz masculina suave y cálida | Relajante, íntimo |
| **Sam** | `yoZ06aMxZJJ28mfd3POQ` | Voz masculina joven y fresca | Contemporáneo, joven |

## 💡 Cómo Usar Voces Predefinidas

### Opción 1: Usando la Función Directa

Si quieres probar directamente sin clonar voz, puedes usar la función `usar_voz_predefinida_elevenlabs`:

```python
from proyecto.controllers.SintetizadorController import usar_voz_predefinida_elevenlabs
from config import DevConfig

# Usar voz predefinida (Rachel por defecto)
resultado = usar_voz_predefinida_elevenlabs(
    texto="Hola, esta es una prueba de voz",
    output_path="prueba_rachel.wav",
    api_key=DevConfig.ELEVENLABS_API_KEY
)

# O especificar una voz diferente
resultado = usar_voz_predefinida_elevenlabs(
    texto="Hola, esta es una prueba de voz",
    output_path="prueba_josh.wav",
    api_key=DevConfig.ELEVENLABS_API_KEY,
    voice_id_predefinida="TxGEqnHWrfWFTfGW9XjX"  # Josh
)
```

### Opción 2: Configurar Voice ID en .env

Si ya tienes un Voice ID de una voz predefinida que quieres usar siempre, puedes configurarlo en tu archivo `.env`:

```env
ELEVENLABS_API_KEY=sk-tu-api-key-aqui
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM  # Rachel (voz por defecto)
```

Cuando tengas `ELEVENLABS_VOICE_ID` configurado, el sistema automáticamente usará esa voz en lugar de intentar clonar.

### Opción 3: Usar desde el Dashboard Web

1. Ve a tu dashboard de ElevenLabs: https://elevenlabs.io/app/voices
2. Navega a la sección "Pre-made Voices" (Voces Predefinidas)
3. Escucha las voces disponibles y elige la que prefieras
4. Copia el Voice ID de la voz que quieras usar
5. Agrega ese Voice ID a tu archivo `.env` como `ELEVENLABS_VOICE_ID`

## 🔍 Obtener Voice IDs de Voces Predefinidas

Puedes obtener la lista completa de voces predefinidas disponibles usando la API de ElevenLabs:

```python
from elevenlabs import ElevenLabs
from config import DevConfig

client = ElevenLabs(api_key=DevConfig.ELEVENLABS_API_KEY)

# Obtener todas las voces disponibles (incluyendo predefinidas)
voices = client.voices.get_all()

for voice in voices.voices:
    print(f"Nombre: {voice.name}, ID: {voice.voice_id}")
    print(f"  Categoría: {voice.category}")  # 'premade' para voces predefinidas
```

## ⚠️ Notas Importantes

1. **No requiere clonación**: Las voces predefinidas no requieren entrenamiento ni clonación. Están listas para usar inmediatamente.

2. **Funciona con todos los planes**: Las voces predefinidas funcionan incluso con el plan gratuito de ElevenLabs (si está disponible) o el plan Starter.

3. **No consume créditos de clonación**: Usar voces predefinidas solo consume créditos de texto-a-voz, no de clonación de voz.

4. **Ideal para pruebas**: Perfecto para probar el sistema completo antes de invertir en clonar tu propia voz.

5. **Límites**: Aunque puedes usar voces predefinidas, aún estás limitado por tu plan de ElevenLabs en términos de créditos de texto-a-voz.

## 🎯 Cuándo Usar Voces Predefinidas

✅ **Usa voces predefinidas cuando:**
- Quieres probar el sistema rápidamente
- No tienes un audio de referencia de buena calidad
- Quieres evitar la complejidad de la clonación
- Necesitas resultados inmediatos sin entrenamiento
- Tu plan de ElevenLabs no incluye clonación de voz

❌ **No uses voces predefinidas cuando:**
- Necesitas tu voz específica o una voz personalizada
- Quieres clonar la voz de otra persona
- Necesitas una voz única para tu proyecto

## 📝 Ejemplo Completo

```python
# Importar funciones necesarias
from proyecto.controllers.SintetizadorController import (
    separar_stems,
    generar_letra,
    usar_voz_predefinida_elevenlabs,
    mezclar_audio
)
from config import DevConfig

# Paso 1: Separar stems del audio original
resultado_separacion = separar_stems("cancion_original.mp3")

# Paso 2: Generar letra (extraer del audio o proporcionarla)
resultado_letra = generar_letra(
    texto_letra="Aquí va la letra de la canción",
    audio_path="cancion_original.mp3"
)

# Paso 3: Usar voz predefinida en lugar de clonar
resultado_voz = usar_voz_predefinida_elevenlabs(
    texto=resultado_letra['letra'],
    output_path="voz_predefinida.wav",
    api_key=DevConfig.ELEVENLABS_API_KEY,
    voice_id_predefinida="21m00Tcm4TlvDq8ikWAM"  # Rachel
)

# Paso 4: Mezclar voz con instrumental
resultado_mezcla = mezclar_audio(
    voz_path=resultado_voz['audio_path'],
    instrumental_path=resultado_separacion['instrumental_path']
)

print(f"✅ Canción final: {resultado_mezcla['audio_final_path']}")
```

## 🔗 Enlaces Útiles

- **Dashboard de ElevenLabs**: https://elevenlabs.io/app/voices
- **Documentación de API**: https://elevenlabs.io/docs/api-reference
- **Precios y Planes**: https://elevenlabs.io/pricing




