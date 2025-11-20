"""
Script para listar todas las voces predefinidas disponibles en ElevenLabs

Uso:
    python listar_voces_elevenlabs.py

Este script te mostrará todas las voces predefinidas disponibles en tu cuenta de ElevenLabs,
incluyendo sus Voice IDs que puedes usar en el formulario.
"""

import os
import sys

# Agregar el directorio raíz al path para importar config
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from elevenlabs import ElevenLabs
    from config import DevConfig
    
    # Obtener API key de la configuración
    api_key = DevConfig.ELEVENLABS_API_KEY
    
    if not api_key or api_key == "sk-tu-api-key-aqui":
        print("❌ ERROR: No hay API key configurada")
        print("\n📋 SOLUCIÓN:")
        print("1. Abre tu archivo .env")
        print("2. Agrega tu API key de ElevenLabs:")
        print("   ELEVENLABS_API_KEY=sk-tu-api-key-real")
        print("3. Vuelve a ejecutar este script")
        sys.exit(1)
    
    print("🔍 Conectando con ElevenLabs API...")
    print(f"📋 API Key: {api_key[:10]}...{api_key[-5:]}")
    print()
    
    # Crear cliente ElevenLabs
    client = ElevenLabs(api_key=api_key)
    
    # Obtener todas las voces disponibles
    print("📥 Obteniendo lista de voces disponibles...")
    voices_response = client.voices.get_all()
    
    if not voices_response or not hasattr(voices_response, 'voices'):
        print("❌ Error: No se pudieron obtener las voces")
        sys.exit(1)
    
    voices = voices_response.voices
    
    if not voices:
        print("⚠️  No se encontraron voces en tu cuenta")
        sys.exit(0)
    
    # Separar voces predefinidas de voces personalizadas
    premade_voices = []
    custom_voices = []
    
    for voice in voices:
        # Las voces predefinidas generalmente tienen category='premade' o name conocido
        # También podemos identificarlas porque son públicas y tienen nombres específicos
        voice_info = {
            'name': getattr(voice, 'name', 'Sin nombre'),
            'voice_id': getattr(voice, 'voice_id', 'N/A'),
            'category': getattr(voice, 'category', 'unknown'),
            'description': getattr(voice, 'description', 'Sin descripción')
        }
        
        # Intentar identificar si es predefinida
        # Las voces predefinidas suelen tener category='premade' o nombres conocidos
        category = voice_info.get('category', '').lower()
        if 'premade' in category or voice_info['name'] in ['Rachel', 'Domi', 'Bella', 'Elli', 'Josh', 'Arnold', 'Adam', 'Sam']:
            premade_voices.append(voice_info)
        else:
            custom_voices.append(voice_info)
    
    # Mostrar voces predefinidas
    print("=" * 80)
    print("🎤 VOCES PREDEFINIDAS DISPONIBLES")
    print("=" * 80)
    print()
    
    if premade_voices:
        # Separar por género si es posible
        femeninas = []
        masculinas = []
        otras = []
        
        nombres_femeninos = ['Rachel', 'Domi', 'Bella', 'Elli', 'Bella', 'Sarah', 'Nicole', 'Emily']
        nombres_masculinos = ['Josh', 'Arnold', 'Adam', 'Sam', 'Antoni', 'Thomas', 'Charlie', 'Daniel']
        
        for voice in premade_voices:
            nombre = voice['name']
            if nombre in nombres_femeninos:
                femeninas.append(voice)
            elif nombre in nombres_masculinos:
                masculinas.append(voice)
            else:
                otras.append(voice)
        
        if femeninas:
            print("👩 VOCES FEMENINAS:")
            print("-" * 80)
            for voice in femeninas:
                print(f"  • {voice['name']}")
                print(f"    Voice ID: {voice['voice_id']}")
                if voice.get('description'):
                    print(f"    Descripción: {voice['description']}")
                print()
        
        if masculinas:
            print("👨 VOCES MASCULINAS:")
            print("-" * 80)
            for voice in masculinas:
                print(f"  • {voice['name']}")
                print(f"    Voice ID: {voice['voice_id']}")
                if voice.get('description'):
                    print(f"    Descripción: {voice['description']}")
                print()
        
        if otras:
            print("🔊 OTRAS VOCES:")
            print("-" * 80)
            for voice in otras:
                print(f"  • {voice['name']}")
                print(f"    Voice ID: {voice['voice_id']}")
                if voice.get('description'):
                    print(f"    Descripción: {voice['description']}")
                print()
    else:
        print("⚠️  No se encontraron voces predefinidas en la respuesta")
        print("💡 Esto puede deberse a que la API no las clasifica como 'premade'")
        print("💡 Todas las voces disponibles se mostrarán a continuación")
        print()
    
    # Mostrar todas las voces disponibles (incluyendo personalizadas)
    print("=" * 80)
    print("📋 TODAS LAS VOCES DISPONIBLES EN TU CUENTA")
    print("=" * 80)
    print()
    
    for i, voice in enumerate(voices, 1):
        name = getattr(voice, 'name', 'Sin nombre')
        voice_id = getattr(voice, 'voice_id', 'N/A')
        category = getattr(voice, 'category', 'unknown')
        description = getattr(voice, 'description', '')
        
        print(f"{i}. {name}")
        print(f"   Voice ID: {voice_id}")
        print(f"   Categoría: {category}")
        if description:
            print(f"   Descripción: {description}")
        print()
    
    # Generar código HTML para el formulario
    print("=" * 80)
    print("💡 CÓDIGO HTML PARA AGREGAR AL FORMULARIO")
    print("=" * 80)
    print()
    print("Puedes copiar y pegar este código en el dropdown de voces predefinidas:")
    print()
    print('<select id="vozPredefinida" name="vozPredefinida" class="form-control">')
    print('    <optgroup label="Voces Femeninas">')
    
    if femeninas:
        for voice in femeninas:
            print(f'        <option value="{voice["voice_id"]}">{voice["name"]} - Voz femenina</option>')
    
    print('    </optgroup>')
    print('    <optgroup label="Voces Masculinas">')
    
    if masculinas:
        for voice in masculinas:
            print(f'        <option value="{voice["voice_id"]}">{voice["name"]} - Voz masculina</option>')
    
    print('    </optgroup>')
    
    if otras:
        print('    <optgroup label="Otras Voces">')
        for voice in otras:
            print(f'        <option value="{voice["voice_id"]}">{voice["name"]}</option>')
        print('    </optgroup>')
    
    print('</select>')
    print()
    
    print("=" * 80)
    print("✅ Listado completado")
    print("=" * 80)
    print()
    print("💡 CONSEJOS:")
    print("   - Usa los Voice IDs mostrados arriba en el formulario")
    print("   - Puedes probar diferentes voces hasta encontrar la que prefieras")
    print("   - Las voces predefinidas no requieren clonación, son más rápidas")
    print()

except ImportError as e:
    print(f"❌ ERROR: No se pudo importar la librería necesaria: {e}")
    print("\n📋 SOLUCIÓN:")
    print("1. Asegúrate de tener instalado elevenlabs:")
    print("   pip install elevenlabs")
    print("2. Verifica que el archivo config.py exista y tenga DevConfig")
    sys.exit(1)

except Exception as e:
    import traceback
    print(f"❌ ERROR: {str(e)}")
    print("\n📋 DETALLES:")
    print(traceback.format_exc())
    sys.exit(1)




