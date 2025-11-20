import os
from dotenv import load_dotenv                          # Instalar con pip install python-dotenv

load_dotenv()                                           # Cargar todo el cotenido de .env en variables de entorno

#configuración basica que debe tener
class BaseConfig():
    #SERVER_NAME = "localhost:5000"
    SECRET_KEY = os.environ.get("SECRET_KEY","").strip() or "dev-secret-key-change-in-production"        #clave secreta para la proteccion del login
    DEBUG = True
    TEMPLATE_FOLDER = "views/templates"                 # defino las rutas para los archivos de vista 
    STATIC_FOLDER ="views/static"

# configuracion para la base de datos
class DevConfig(BaseConfig):
    #de la variable de entorno .env traigo todas las configuraciones propias
    DB_HOST = os.environ.get("DB_HOST","").strip()     
    DB_NAME = os.environ.get("DB_NAME","").strip() 
    DB_USER = os.environ.get("DB_USER","").strip() 
    DB_PASS = os.environ.get("DB_PASS","").strip() 
    DB_PORT = int(os.environ.get("DB_PORT","5433").strip()) if os.environ.get("DB_PORT","").strip() else 5433 

    #Define la cadena de conexión a tu base de datos PostgreSQL, importante cambiar la contraseñadel postgres en ubuntu
    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost:5432/db_diagrama'
    SQLALCHEMY_DATABASE_URI = 'postgresql://'+DB_USER+':'+DB_PASS+'@'+DB_HOST+':'+str(DB_PORT)+'/'+DB_NAME
    #Establece esta opción en False para mejorar el rendimiento.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API Keys para servicios externos (opcional)
    ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY","").strip()  # API Key de ElevenLabs para síntesis de voz (más liviano que modelos locales)
    ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID","").strip()  # Voice ID de una voz existente en ElevenLabs (opcional, si no tienes permiso voices_write)
    RESEMBLE_API_KEY = os.environ.get("RESEMBLE_API_KEY","").strip()  # API Key de Resemble.ai para clonación de voz (alternativa a ElevenLabs)
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY","").strip()  # API Key de OpenAI para transcripción de audio (Whisper API - más rápida y precisa que Whisper local)
    
    print(SQLALCHEMY_DATABASE_URI)
