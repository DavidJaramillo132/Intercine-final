import customtkinter as ctk
import json
from tkinter import messagebox
from PIL import Image, ImageTk
from modulos.admin.admin_asientos import mostrar_asientos
from modulos.utilidades import crear_frame, init_fonts, color_principal, color_botones, contenido_principal

# Cargar los horarios desde el archivo JSON
with open('horarios.json', 'r') as file:
    horarios = json.load(file)

# Función para crear un botón de selección (RadioButton)
def crear_boton_seleccion(parent, text, variable, value, name):
    return ctk.CTkRadioButton(parent, text=text, variable=variable, value=value)

# Cargar los datos de las películas desde el archivo JSON
with open("peliculas.json", "r") as f:
    data_peliculas = json.load(f)

# Extraer información de las películas
peliculas = [pelicula["titulo"] for pelicula in data_peliculas]
rutas_imagenes = [pelicula["imagen_path"] for pelicula in data_peliculas]
sinopsis_peliculas = {pelicula["titulo"]: pelicula["descripcion"] for pelicula in data_peliculas}
trailer_peliculas = {pelicula["titulo"]: pelicula["trailer"] for pelicula in data_peliculas}

# Cargar los datos de las salas desde el archivo JSON
with open("salas.json", "r") as f:
    data_salas = json.load(f)

# Extraer información de las salas
salas = data_salas['salas']

# Diccionario para rastrear los botones seleccionados
botones_seleccionados = {"horario": None, "sala": None}

# Función para cambiar el color de un botón cuando es seleccionado o deseleccionado
def cambiar_color_boton(boton, seleccionado):
    if seleccionado:
        boton.configure(fg_color=color_botones)
    else:
        boton.configure(fg_color=color_principal)

# Función para manejar la selección de botones
def manejar_seleccion_boton(boton, var, valor, categoria):
    global botones_seleccionados
    if botones_seleccionados[categoria] is boton:
        var.set("")
        cambiar_color_boton(boton, False)
        botones_seleccionados[categoria] = None
    else:
        if botones_seleccionados[categoria] is not None:
            cambiar_color_boton(botones_seleccionados[categoria], False)
        var.set(valor)
        cambiar_color_boton(boton, True)
        botones_seleccionados[categoria] = boton

# Función para crear un botón de selección (Button)
def crear_boton_seleccion(frame, texto, var, valor, categoria):
    boton = ctk.CTkButton(frame, text=texto, fg_color=color_principal, hover_color=color_botones,
                          command=lambda: manejar_seleccion_boton(boton, var, valor, categoria))
    boton.pack(padx=20, pady=5)
    return boton

# Función para la selección de horario y sala por el administrador
def admin_seleccionar_horario_sala(contenido_principal, pelicula):
    global botones_seleccionados
    botones_seleccionados = {"horario": None, "sala": None}  # Reiniciar selección de botones

    # Eliminar widgets existentes
    for widget in contenido_principal.winfo_children():
        widget.destroy()
    
    # Inicializar fuentes
    fuente_textos, fuente_titulos_subtitulos, fuente_sinopsi = init_fonts(contenido_principal)

    # Crear marco principal
    frame_principal = ctk.CTkFrame(contenido_principal, fg_color=color_principal)
    frame_principal.pack(expand=True, padx=10, pady=10)
        
    # Crear marco izquierdo
    frame_izquierda = ctk.CTkFrame(frame_principal, fg_color=color_principal)
    frame_izquierda.pack(side="left", fill="y", expand=True, padx=10, pady=10)

    # Crear marco derecho
    frame_derecha = ctk.CTkFrame(frame_principal, fg_color=color_principal)
    frame_derecha.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # Mostrar el nombre de la película
    nombre_pelicula = ctk.CTkLabel(frame_izquierda, text=pelicula, text_color="white", font=fuente_titulos_subtitulos)
    nombre_pelicula.pack(pady=10)

    # Manejo de errores si la película no se encuentra
    try:
        ruta_imagen = rutas_imagenes[peliculas.index(pelicula)]
    except ValueError:
        messagebox.showerror("Error", f"La película '{pelicula}' no se encuentra en la lista de películas.")
        return

    # Mostrar la imagen de la película
    imagen = Image.open(ruta_imagen)
    imagen = imagen.resize((550, 570))
    imagen_tk = ImageTk.PhotoImage(imagen)
    label_imagen = ctk.CTkLabel(frame_izquierda, image=imagen_tk, text="")
    label_imagen.image = imagen_tk
    label_imagen.pack(pady=10)

    # Botón para ver el tráiler
    trailer_label = ctk.CTkButton(frame_izquierda, text="Ver tráiler", text_color="White", cursor="hand2", font=fuente_titulos_subtitulos, fg_color=color_principal)
    trailer_label.pack(pady=10)
    trailer_label.bind("<Button-1>", lambda e: abrir_trailer(trailer_peliculas[pelicula]))
    
    # Mostrar sinopsis de la película
    sinopsis_label = ctk.CTkLabel(frame_derecha, text="Sinopsis", text_color="white", font=fuente_titulos_subtitulos, wraplength=1000, justify="left")
    sinopsis_label.pack(pady=10, padx=10)
    
    sinopsis_label = ctk.CTkLabel(frame_derecha, text=sinopsis_peliculas[pelicula], font=fuente_sinopsi, text_color="white", wraplength=1000, justify="left")
    sinopsis_label.pack(pady=10, padx=10)
    
    # Crear contenido para seleccionar horario
    contenido_horario = crear_frame(frame_derecha)

    horario_label = ctk.CTkLabel(contenido_horario, text="Seleccione un Horario:", text_color="white", font=fuente_titulos_subtitulos, fg_color=color_principal)
    horario_label.pack(pady=5)
    horario_var = ctk.StringVar()
    
    frame_horarios = ctk.CTkFrame(contenido_horario, fg_color=color_principal)
    frame_horarios.pack(pady=10)
    
    # Crear botones de selección de horario
    for horario in horarios:
        crear_boton_seleccion(frame_horarios, horario, horario_var, horario, "horario").pack(side="left", padx=5)
        
    contenido_horario.pack(side="top", fill="both", expand=True)

    # Crear contenido para seleccionar sala
    contenido_sala = crear_frame(frame_derecha)
    sala_label = ctk.CTkLabel(contenido_sala, text="Seleccione una sala de Cine:", text_color="white", font=fuente_titulos_subtitulos)
    sala_label.pack(pady=10)
    sala_var = ctk.StringVar() 
    
    frame_salas = ctk.CTkFrame(contenido_sala, fg_color=color_principal)
    frame_salas.pack(pady=10)
    
    # Crear botones de selección de sala
    for i, sala in enumerate(salas, start=1):
        crear_boton_seleccion(frame_salas, sala["nombre"], sala_var, i, "sala").pack(side="left", padx=5)

    # Botón para confirmar la selección
    confirmar_button = ctk.CTkButton(frame_derecha, text="Confirmar", fg_color=color_principal, font=fuente_titulos_subtitulos,
                                     command=lambda: confirmar_seleccion(contenido_principal, horario_var, sala_var, pelicula, imagen_tk))
    confirmar_button.pack(pady=20)

# Función para abrir el tráiler en el navegador web
def abrir_trailer(link):
    import webbrowser
    webbrowser.open(link)

# Función para confirmar la selección de horario y sala
def confirmar_seleccion(contenido_principal, horario_var, sala_var, pelicula, img):
    horario_seleccionado = horario_var.get()
    sala_seleccionado = sala_var.get()
    if horario_seleccionado and sala_seleccionado:
        mostrar_asientos(contenido_principal, pelicula, horario_seleccionado, sala_seleccionado, img)
    else:
        messagebox.showwarning("Selección incompleta", "Por favor seleccione tanto el horario como la película.")
