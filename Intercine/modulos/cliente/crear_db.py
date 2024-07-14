import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Crear la tabla de usuarios
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, 
             username TEXT UNIQUE, 
             password TEXT)
             ''')

# Insertar un usuario administrador
c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', '123'))

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()
