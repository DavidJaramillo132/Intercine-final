import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

# Funciones de interfaz de usuario
def quienes_somos(contenido_principal):
        #elimina todos los widget del contenido principal
    for widget in contenido_principal.winfo_children():
        widget.destroy()
    
    imagen = Image.open(r"SegundoSemestre\Intercine\imagenes\intercine.png")
    imagen = imagen.resize((300, 200))#tamaño de la imagen
    imagen_fondo = ImageTk.PhotoImage(imagen)
    label_bienvenida = ctk.CTkLabel(contenido_principal, text="Somos InterCine, Cine de calidad", font=ctk.CTkFont(size=25, weight="bold"))
    label_bienvenida.pack(pady=20)
    label_instrucciones = ctk.CTkLabel(contenido_principal, text="¡Descubre la magia del cine en InterCine, donde la emoción cobra vida en la gran pantalla!\nSumérgete en una experiencia cinematográfica sin igual", font=ctk.CTkFont(size=14))
    label_instrucciones.pack(pady=10)
    logo = ctk.CTkLabel(master=contenido_principal, image=imagen_fondo, text="")#Muestra ña imagen
    logo.pack()
    
    
    
    


#cierra la app
def salir(root):
    if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir?"):
        root.destroy()
