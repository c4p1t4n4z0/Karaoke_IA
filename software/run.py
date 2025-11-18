from proyecto import app
from dotenv import load_dotenv
import os

# Cargar las variables de entorno
load_dotenv()

# Imprimir las variables de entorno para verificar que se cargaron correctamente
print("DB_HOST:", os.environ.get("DB_HOST"))
print("DB_NAME:", os.environ.get("DB_NAME"))
print("DB_USER:", os.environ.get("DB_USER"))
print("DB_PASS:", os.environ.get("DB_PASS"))
print("DB_PORT:", os.environ.get("DB_PORT"))

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
