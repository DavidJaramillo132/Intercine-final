import customtkinter as ctk
import json
from tkinter import messagebox
from PIL import Image, ImageTk
from modulos.cliente.asientos import mostrar_asientos
from modulos.utilidades import crear_frame, init_fonts, color_principal, color_botones, contenido_principal

#abre el archivo JSON en modo de lectura(r) y la informacion lo guarda en la variable horarios
with open("horarios.json", 'r') as file:
    horarios = json.load(file)

def crear_boton_seleccion(parent, text, variable, value, name):
    return ctk.CTkRadioButton(parent, text=text, variable=variable, value=value)

#abre el archivo JSON en modo de lectura(r) y la informacion lo guarda en la variable data_peliculas
with open("peliculas.json", "r") as f: 
    data_peliculas = json.load(f)
    
    
# Crear una lista de títulos de películas a partir de data_peliculas
peliculas = [pelicula["titulo"] for pelicula in data_peliculas]
# Crear una lista de rutas de imágenes de películas a partir de data_peliculas
rutas_imagenes = [pelicula["imagen_path"] for pelicula in data_peliculas]
# Crear un diccionario donde las claves son los títulos de las películas y los valores son las descripciones
sinopsis_peliculas = {pelicula["titulo"]: pelicula["descripcion"] for pelicula in data_peliculas}
# Crear un diccionario donde las claves son los títulos de las películas y los valores son las rutas de los trailers
trailer_peliculas = {pelicula["titulo"]: pelicula["trailer"] for pelicula in data_peliculas}

#abre el archivo JSON en modo de lectura(r) y la informacion lo guarda en la variable data_salas
with open("salas.json", "r") as f:
    data_salas = json.load(f)

salas = data_salas['salas']

def cartelera(contenido_principal):
    for widget in contenido_principal.winfo_children():
        widget.destroy()
    
    fuente_textos, fuente_titulos_subtitulos, fuente_sinopsi = init_fonts(contenido_principal)
    #El canvas para colocar barra de desplazamiento
    canvas = ctk.CTkCanvas(contenido_principal, width=600, height=350, highlightthickness=0)   
    canvas.config(bg=color_principal) 
    canvas.pack(side="left", fill="both", expand=True)
    #Agrega la barra de desplazamiento
    scrollbar = ctk.CTkScrollbar(contenido_principal, orientation="vertical", fg_color=color_principal, command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    scrollable_frame = ctk.CTkFrame(canvas, fg_color=color_principal)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    #coloca texto
    label = ctk.CTkLabel(scrollable_frame, text="Películas Disponibles en nuestra cartelera", font=fuente_titulos_subtitulos)
    label.pack(side="top", fill="x", expand=True, pady=10)
    #frame para colocar las peliculas
    frame_peliculas = ctk.CTkFrame(scrollable_frame, fg_color=color_principal)
    frame_peliculas.pack(pady=5)

    cols = 5

    # Iterar sobre las listas peliculas y rutas_imagenes usando enumerate y zip
    for i, (pelicula, ruta_imagen) in enumerate(zip(peliculas, rutas_imagenes)):
        # Calcular la columna y fila en la cuadrícula de películas
        col = i % cols  # Calcular la columna actual usando el operador módulo
        row = i // cols  # Calcular la fila actual usando la división entera

        # Abrir la imagen desde la ruta especificada
        imagen = Image.open(ruta_imagen)
        # Redimensionar la imagen a un tamaño específico (350x370 píxeles)
        imagen = imagen.resize((350, 370))
        # Convertir la imagen a un formato compatible con Tkinter
        imagen_tk = ImageTk.PhotoImage(imagen)
    
        # Crear un label con imagen usando CTkLabel de customtkinter
        label_imagen = ctk.CTkLabel(frame_peliculas, image=imagen_tk, text="")
        label_imagen.image = imagen_tk  # Asegurar que la imagen no se pierda por recolección de basura
        # Colocar el label en la cuadrícula, especificando fila y columna, con relleno y espaciado
        label_imagen.grid(row=row * 4, column=col, padx=14, pady=10)
    
        # Crear un botón con el título de la película usando CTkButton de customtkinter
        boton = ctk.CTkButton(master=frame_peliculas, text=pelicula, font=fuente_textos, fg_color=color_principal,
                            hover_color=color_botones, width=100, height=25, corner_radius=10,
                            command=lambda p=pelicula: seleccionar_horario_sala(contenido_principal, p))
        # Colocar el botón en la cuadrícula, justo debajo del label de imagen
        boton.grid(row=row * 4 + 1, column=col, padx=14, pady=10, sticky='nsew')

    # Configurar las columnas del frame_peliculas para que se expandan de manera uniforme
    for i in range(cols):
        frame_peliculas.columnconfigure(i, weight=1)

# Diccionario para rastrear qué botón está seleccionado en cada categoría
botones_seleccionados = {"horario": None, "sala": None}

# Cambia el color de los botones
def cambiar_color_boton(boton, seleccionado):
    if seleccionado:
        boton.configure(fg_color=color_botones)
    else:
        boton.configure(fg_color=color_principal)

# Maneja la selección de los botones
def manejar_seleccion_boton(boton, var, valor, categoria):
    global botones_seleccionados
    if botones_seleccionados[categoria] is boton:
        var.set("")  # Desselecciona el botón
        cambiar_color_boton(boton, False)
        botones_seleccionados[categoria] = None
    else:
        if botones_seleccionados[categoria] is not None:
            cambiar_color_boton(botones_seleccionados[categoria], False)  # Deselecciona el botón anterior
        var.set(valor)  # Selecciona el nuevo botón
        cambiar_color_boton(boton, True)
        botones_seleccionados[categoria] = boton

# Crea un botón de selección
def crear_boton_seleccion(frame, texto, var, valor, categoria):
    boton = ctk.CTkButton(frame, text=texto, fg_color=color_principal, hover_color=color_botones,
                          command=lambda: manejar_seleccion_boton(boton, var, valor, categoria))
    boton.pack(padx=20, pady=5)
    return boton

# Muestra la interfaz para seleccionar horario y sala
def seleccionar_horario_sala(contenido_principal, pelicula):
    global botones_seleccionados
    botones_seleccionados = {"horario": None, "sala": None}  # Reinicia la selección de botones

    # Elimina los widgets anteriores
    for widget in contenido_principal.winfo_children():
        widget.destroy()
        
    # Inicializa las fuentes de texto
    fuente_textos, fuente_titulos_subtitulos, fuente_sinopsi = init_fonts(contenido_principal)

    # Crea el marco izquierdo para la información de la película
    frame_izquierda = ctk.CTkFrame(contenido_principal, fg_color=color_principal)
    frame_izquierda.pack(side="left", fill="y", padx=10, pady=10)

    # Crea el marco derecho para la selección de horario y sala
    frame_derecha = ctk.CTkFrame(contenido_principal, fg_color=color_principal)
    frame_derecha.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # Muestra el nombre de la película
    nombre_pelicula = ctk.CTkLabel(frame_izquierda, text=pelicula, text_color="white", font=fuente_titulos_subtitulos)
    nombre_pelicula.pack(pady=10)

    # Muestra la imagen de la película
    ruta_imagen = rutas_imagenes[peliculas.index(pelicula)]
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
    
    # Muestra la sinopsis de la película
    sinopsis_label = ctk.CTkLabel(frame_derecha, text="Sinopsis", text_color="white", font=fuente_titulos_subtitulos, wraplength=1000, justify="left")
    sinopsis_label.pack(pady=10, padx=10)
    
    sinopsis_label = ctk.CTkLabel(frame_derecha, text=sinopsis_peliculas[pelicula], font=fuente_sinopsi, text_color="white", wraplength=1000, justify="left")
    sinopsis_label.pack(pady=10, padx=10)
    
    # Crea el marco para la selección de horario
    contenido_horario = crear_frame(frame_derecha)
    horario_label = ctk.CTkLabel(contenido_horario, text="Seleccione un Horario:", text_color="white", font=fuente_titulos_subtitulos, fg_color=color_principal)
    horario_label.pack(pady=5)
    horario_var = ctk.StringVar()
    frame_horarios = ctk.CTkFrame(contenido_horario, fg_color=color_principal)
    frame_horarios.pack(pady=10)
    
    #Crea botones para cada horario disponible
    for horario in horarios:
        crear_boton_seleccion(frame_horarios, horario, horario_var, horario, "horario").pack(side="left", padx=5)
        
    contenido_horario.pack(side="top", fill="both", expand=True)

    #Crea el marco para la selección de sala
    contenido_sala = crear_frame(frame_derecha)
    sala_label = ctk.CTkLabel(contenido_sala, text="Seleccione una sala de Cine:", text_color="white", font=fuente_titulos_subtitulos)
    sala_label.pack(pady=10)
    sala_var = ctk.StringVar() #rastrear y actualizar su valor automáticamente cuando cambian
    frame_salas = ctk.CTkFrame(contenido_sala, fg_color=color_principal)
    frame_salas.pack(pady=10)
    
    #Crea botones para cada sala disponible que hay en el archivo salas.json
    for i, sala in enumerate(salas, start=1):
        crear_boton_seleccion(frame_salas, sala["nombre"], sala_var, i, "sala").pack(side="left", padx=5)

    # Botón para confirmar la selección
    confirmar_button = ctk.CTkButton(frame_derecha, text="Confirmar", fg_color=color_principal, font=fuente_titulos_subtitulos,
                                     command=lambda: confirmar_seleccion(contenido_principal, horario_var, sala_var, pelicula, imagen_tk))
    confirmar_button.pack(pady=20)

#Abre el tráiler de la película en un navegador web
def abrir_trailer(link):
    import webbrowser
    webbrowser.open(link)

#Confirma la selección de horario y sala y muestra los asientos disponibles
def confirmar_seleccion(contenido_principal, horario_var, sala_var, pelicula, img):
    horario_seleccionado = horario_var.get()
    sala_seleccionado = sala_var.get()
    if horario_seleccionado and sala_seleccionado:
        mostrar_asientos(contenido_principal, pelicula, horario_seleccionado, sala_seleccionado, img)
    else:
        messagebox.showwarning("Selección incompleta", "Por favor seleccione tanto el horario como la película.")
