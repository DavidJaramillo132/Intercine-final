import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

def perfil(contenido_principal, username):
    #elimina todos los widget del contenido principal
    for widget in contenido_principal.winfo_children():
        widget.destroy()
    #carga la imagen
    imagen = Image.open(r"SegundoSemestre\Intercine\imagenes\perfil.png")
    imagen = imagen.resize((450, 450)) #tamaño de la imagen
    imagen_fondo = ImageTk.PhotoImage(imagen)
    label_bienvenida_nombre = ctk.CTkLabel(contenido_principal, text=f"¡Bienvenido de vuelta {username} !", font=ctk.CTkFont(size=25, weight="bold"))
    label_bienvenida_nombre.pack(pady=20)
    foto_perfil = ctk.CTkLabel(master=contenido_principal, image=imagen_fondo, text="") #muestrala imagen
    foto_perfil.pack()
    label_bienvenida_texto = ctk.CTkLabel(contenido_principal, text="Esperamos que le agrade nuestra app", font=ctk.CTkFont(size=14))
    label_bienvenida_texto.pack(pady=10)