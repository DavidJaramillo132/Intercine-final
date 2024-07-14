import json
import customtkinter as ctk
from tkinter import messagebox
from modulos.utilidades import init_fonts, color_principal, color_botones

FILE_PATH = 'salas.json'

# Función para cargar las salas desde el archivo JSON
def cargar_salas():
    with open(FILE_PATH, 'r') as file:
        data = json.load(file)
    return data['salas']

# Función para guardar las salas en el archivo JSON
def guardar_salas(salas):
    with open(FILE_PATH, 'w') as file:
        json.dump({'salas': salas}, file, indent=4)

# Función para crear botones de selección de salas
def crear_boton_seleccion(frame, texto, command, row, col, contenido_principal):
    fuente_textos, fuente_titulos_subtitulos, fuente_sinopsi = init_fonts(contenido_principal)

    boton = ctk.CTkButton(frame, text=texto, command=command, font=fuente_sinopsi, fg_color=color_principal, hover_color=color_botones)
    boton.grid(row=row, column=col, padx=5, pady=5)
    return boton

# Función para agregar una nueva sala
def agregar_sala(frame_salas, contenido_principal):
    nombre = ctk.CTkInputDialog(text="Nombre de la nueva sala:", title="Input").get_input()
    if nombre:
        salas = cargar_salas()  # Recargar las salas desde el archivo JSON
        nueva_sala = {'nombre': nombre}
        salas.append(nueva_sala)
        guardar_salas(salas)
        actualizar_gui(salas, frame_salas, contenido_principal)

# Función para eliminar una sala seleccionada
def eliminar_sala(salas, frame_salas, sala_nombre, contenido_principal):
    # Eliminar la sala de la lista
    nuevas_salas = [sala for sala in salas if sala['nombre'] != sala_nombre]
    # Guardar la lista actualizada en el archivo JSON
    guardar_salas(nuevas_salas)
    # Actualizar la GUI
    actualizar_gui(nuevas_salas, frame_salas, contenido_principal)

# Función para actualizar la GUI con las salas actuales
def actualizar_gui(salas, frame_salas, contenido_principal):
    for widget in frame_salas.winfo_children():
        widget.destroy()
    #el orden en que ponen las salas
    for idx, sala in enumerate(salas):
        row = idx // 4
        col = idx % 4
        crear_boton_seleccion(frame_salas, sala['nombre'], lambda s=sala: eliminar_sala(salas, frame_salas, s['nombre'], contenido_principal), row, col, contenido_principal)

def mostrar_sala(sala):
    messagebox.showinfo("Sala seleccionada", f"Has seleccionado: {sala['nombre']}")

# Inicialización de la interfaz gráfica
def gestion_sala(contenido_principal):
    for widget in contenido_principal.winfo_children():
        widget.destroy()

    fuente_textos, fuente_titulos_subtitulos, fuente_sinopsi = init_fonts(contenido_principal)

    # Frame para los botones de control
    frame_controles = ctk.CTkFrame(contenido_principal, fg_color="#0D1822")  # Cambia el color de fondo aquí
    frame_controles.pack(side="left", padx=10, pady=20)

    # Frame para la lista de salas
    frame_salas = ctk.CTkFrame(contenido_principal, fg_color="#0D1822")  # Cambia el color de fondo aquí también
    frame_salas.pack(side="right", padx=10, pady=20)

    salas = cargar_salas()
    actualizar_gui(salas, frame_salas, contenido_principal)

    # Botón para agregar sala
    boton_agregar = ctk.CTkButton(frame_controles, text="Agregar Sala", font=fuente_sinopsi, fg_color=color_principal, hover_color=color_botones, 
                                  command=lambda: agregar_sala(frame_salas, contenido_principal))
    boton_agregar.pack(padx=5, pady=10)
