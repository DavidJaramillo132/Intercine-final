import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from modulos.admin.cargar_imagenes import cargar_imagen, seleccionar_imagen
from modulos.admin.cargar_datos import cargar_datos, guardar_datos
from modulos.admin.Asientos_hora import admin_seleccionar_horario_sala
from modulos.utilidades import init_fonts, color_botones, color_principal

DATA_FILE = 'peliculas.json'
peliculas = []

def mostrar_peliculas(contenido_principal):
    global canvas, scrollbar, scrollable_frame, peliculas
    peliculas = cargar_datos()
    
    for widget in contenido_principal.winfo_children():
        widget.destroy()

    peliculas_frame = ctk.CTkFrame(contenido_principal, fg_color=color_principal)
    peliculas_frame.pack(fill="both", expand=True)

    agregar = ctk.CTkButton(peliculas_frame, text="Agregar Película", fg_color=color_principal, hover_color=color_botones, 
                            command=agregar_pelicula)
    agregar.pack(pady=10)
    

    canvas = ctk.CTkCanvas(peliculas_frame, width=600, height=350, highlightthickness=0, bg=color_principal)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(peliculas_frame, orientation="vertical", command=canvas.yview, fg_color=color_principal)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame = ctk.CTkFrame(canvas, fg_color=color_principal)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    actualizar_cartelera(scrollable_frame)

    canvas.bind("<Configure>", lambda event: canvas.config(scrollregion=canvas.bbox("all")))

def agregar_pelicula():
    global imagen_path, imagen_mostrar, entrada_titulo, entrada_descripcion, entrada_trailer

    root = ctk.CTkToplevel()
    root.geometry("1000x500")
    root.title("Agregar pelicula")
    root.configure(fg_color=color_principal)

    fuente_textos, fuente_titulos_subtitulos, fuente_sinopsi = init_fonts(root)

    crear_ventana_agregar_editar_pelicula(root)

    agregar_button = ctk.CTkButton(root, text="Agregar Película", fg_color=color_principal, hover_color=color_botones, font=fuente_titulos_subtitulos,
                                   command=lambda: agregar_actualizar_pelicula(root))
    agregar_button.grid(row=4, column=0, columnspan=2, pady=15)

def editar_pelicula(index):
    global imagen_path, imagen_mostrar, entrada_titulo, entrada_descripcion, entrada_trailer
    
    root = ctk.CTkToplevel()
    root.geometry("1000x500")
    root.title("Editar pelicula")
    root.configure(fg_color=color_principal)  

    fuente_textos, fuente_titulos_subtitulos, fuente_sinopsi = init_fonts(root)

    pelicula = peliculas[index]
    crear_ventana_agregar_editar_pelicula(root, pelicula)

    actualizar_button = ctk.CTkButton(root, text="Actualizar Película", fg_color=color_principal, hover_color=color_botones, font=fuente_titulos_subtitulos,
                                      command=lambda: agregar_actualizar_pelicula(root, index))
    actualizar_button.grid(row=4, column=0, columnspan=2, pady=15)

def crear_ventana_agregar_editar_pelicula(root, pelicula=None):
    global imagen_path, imagen_mostrar, entrada_titulo, entrada_descripcion, entrada_trailer
    
    fuente_textos, fuente_titulos_subtitulos, fuente_sinopsi = init_fonts(root)

    titulo = ctk.CTkLabel(root, text="Título:", font=fuente_titulos_subtitulos, fg_color=color_principal)
    titulo.grid(row=0, column=0, padx=5, pady=5)
    entrada_titulo = ctk.CTkEntry(root, width=200, font=fuente_textos, fg_color=color_principal)
    entrada_titulo.grid(row=0, column=1, padx=5, pady=5)
    if pelicula:
        entrada_titulo.insert(0, pelicula["titulo"])

    descripcion_pelicula = ctk.CTkLabel(root, text="Descripción:", font=fuente_titulos_subtitulos, fg_color=color_principal)
    descripcion_pelicula.grid(row=1, column=0, padx=5, pady=5)
    entrada_descripcion = ctk.CTkTextbox(root, width=200, font=fuente_textos, fg_color=color_principal)
    entrada_descripcion.grid(row=1, column=1, padx=5, pady=5)
    if pelicula:
        entrada_descripcion.insert("1.0", pelicula["descripcion"])

    trailer_pelicula = ctk.CTkLabel(root, text="Enlace del Trailer:", font=fuente_titulos_subtitulos, fg_color=color_principal)
    trailer_pelicula.grid(row=2, column=0, padx=5, pady=5)
    entrada_trailer = ctk.CTkEntry(root, width=200, font=fuente_textos, fg_color=color_principal)
    entrada_trailer.grid(row=2, column=1, padx=5, pady=5)
    if pelicula:
        entrada_trailer.insert(0, pelicula["trailer"])

    imagen_path = tk.StringVar()
    imagen_pelicula_boton = ctk.CTkButton(root, text="Seleccionar Imagen", font=fuente_titulos_subtitulos, command=lambda: seleccionar_imagen(imagen_path, imagen_mostrar), fg_color=color_principal)
    imagen_pelicula_boton.grid(row=3, column=0, padx=10, pady=10)
    imagen_mostrar = ctk.CTkLabel(root, text=" ", fg_color=color_principal)
    imagen_mostrar.grid(row=3, column=1, padx=5, pady=5)
    if pelicula:
        imagen_path.set(pelicula["imagen_path"])
        imagen = cargar_imagen(pelicula["imagen_path"])
        imagen_mostrar.configure(image=imagen)
        imagen_mostrar.image = imagen

def agregar_actualizar_pelicula(root, index=None):
    global scrollable_frame, peliculas

    titulo = entrada_titulo.get()
    descripcion = entrada_descripcion.get("1.0", "end").strip()
    trailer = entrada_trailer.get()
    imagen_path_val = imagen_path.get()

    if not (titulo and descripcion and trailer and imagen_path_val):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    imagen = cargar_imagen(imagen_path_val)

    if index is None:
        peliculas.append({"titulo": titulo, "descripcion": descripcion, "trailer": trailer, "imagen": imagen, "imagen_path": imagen_path_val})
    else:
        peliculas[index] = {"titulo": titulo, "descripcion": descripcion, "trailer": trailer, "imagen": imagen, "imagen_path": imagen_path_val}

    limpiar_campos()
    actualizar_cartelera(scrollable_frame)
    guardar_datos(peliculas)  # Pasar la lista de peliculas
    root.destroy()

def limpiar_campos():
    entrada_titulo.delete(0, 'end')
    entrada_descripcion.delete("1.0", "end")
    entrada_trailer.delete(0, 'end')
    imagen_path.set("")
    imagen_mostrar.configure(image=None)
    imagen_mostrar.image = None

def actualizar_cartelera(frame_peliculas):
    for widget in frame_peliculas.winfo_children():
        widget.destroy()

    cols = 5
    for i, pelicula in enumerate(peliculas):
        col = i % cols
        row = i // cols

        contenedor = ctk.CTkFrame(frame_peliculas, border_color="White", border_width=2, fg_color=color_principal)
        contenedor.grid(row=row * 5, column=col, padx=10, pady=10, sticky='nsew')

        imagen_tk = pelicula["imagen"]
        label_imagen = ctk.CTkLabel(contenedor, image=imagen_tk, text="", fg_color=color_principal)
        label_imagen.image = imagen_tk
        label_imagen.grid(row=row * 4, column=col, padx=14, pady=10)

        boton = ctk.CTkButton(contenedor, text=pelicula["titulo"], width=100, height=25, corner_radius=25, 
                              command=lambda nombre_pelicula=pelicula["titulo"]: admin_seleccionar_horario_sala(frame_peliculas, nombre_pelicula), fg_color=color_principal, hover_color=color_botones)
        boton.grid(row=row * 4 + 1, column=col, padx=14, pady=10, sticky='nsew')

        eliminar_button = ctk.CTkButton(contenedor, text="Eliminar", width=100, height=25, corner_radius=25, 
                                        command=lambda idx=i: eliminar_pelicula(idx, frame_peliculas), fg_color=color_principal, hover_color=color_botones)
        eliminar_button.grid(row=row * 4 + 2, column=col, padx=14, pady=10, sticky='nsew')

        editar_button = ctk.CTkButton(contenedor, text="Editar", width=100, height=25, corner_radius=25, 
                                      command=lambda idx=i: editar_pelicula(idx), fg_color=color_principal, hover_color=color_botones)
        editar_button.grid(row=row * 4 + 3, column=col, padx=14, pady=10, sticky='nsew')

def eliminar_pelicula(index, frame_peliculas):
    global peliculas
    del peliculas[index]
    actualizar_cartelera(frame_peliculas)
    guardar_datos(peliculas)


