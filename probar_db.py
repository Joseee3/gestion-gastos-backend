
from app.database import probar_conexion

try:
    resultado = probar_conexion()
    print(f"¡Conexión exitosa! Resultado: {resultado}")
except Exception as error:
    print("Error al conectar con PostgreSQL:")
    print(error)
