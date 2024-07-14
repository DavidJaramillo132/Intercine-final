import sqlite3
from tkinter import messagebox

def verify_login(entry_username, entry_password, usuario_cliente, usuario_admin):
    username = entry_username.get() #obtiene los valores
    password = entry_password.get()#obtiene los valores
    
    try:
        #Se conecta con el archivo users.db
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        #comando para consultar los datos lo nombres
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone() #recuper la fila del resultado de la consulta
        
        if result:
            # Si la consulta devolvió una fila, el login es exitoso
            messagebox.showinfo("Login", "Login exitoso")
            if username == "a" and password == "a":
                usuario_admin(username)  #entro comom administrador
            else:
                usuario_cliente(username)  #entro como cliente
            
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        if conn:
            conn.close()
            
def register_user(entry_new_username, entry_new_password, usuario_cliente):
    username = entry_new_username.get()#obtiene los valores
    password = entry_new_password.get()#obtiene los valores
    #Verifica que usermane y el password tenga datos
    if not username or not password:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    
    try:
        #Se conecta con el archivo users.db
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        #comando para consultar los datos lo nombres
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        result = c.fetchone()#recuper la fila del resultado de la consulta
        #verifica si el usuario ya existe
        if result:
            messagebox.showerror("Error", "El usuario ya existe")
        else:
            #comando para consultar los datos lo nombres
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit() #confirma una transicion 
            #verifica si solo una(1) fila fue afectada correctamente
            if c.rowcount == 1:
                messagebox.showinfo("Registro", "Usuario registrado exitosamente")
                usuario_cliente(username)  # Llama a la función para mostrar los botones laterales después del registro
            else:
                messagebox.showerror("Error", "No se pudo registrar el usuario")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        if conn:
            conn.close()

