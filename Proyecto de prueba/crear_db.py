import sqlite3

# 1. Crear conexión con la base de datos
conn = sqlite3.connect("stock_plus.db")
cursor = conn.cursor()
from datetime import datetime

fecha_actual = datetime.now().date()  # Esto devuelve solo la fecha, sin hora
# Guárdala en la base de datos como texto o DATE: '2025-05-12'


# 2. Crear la tabla de usuarios
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombres TEXT NOT NULL,
    primer_apellido TEXT NOT NULL,
    segundo_apellido TEXT,
    fecha_nacimiento TEXT NOT NULL,
    telefono TEXT,
    email TEXT UNIQUE NOT NULL,
    contraseña TEXT NOT NULL
);
""")

# 4. Confirmar los cambios
conn.commit()

# 5. Cerrar la conexión
conn.close()

print("Base de datos creada con éxito.")


