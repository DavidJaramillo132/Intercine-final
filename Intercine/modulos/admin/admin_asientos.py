import json
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
from modulos.utilidades import init_fonts, color_principal

# Inicializar estado de asientos
estado_asientos = {}

# Función para guardar el estado de los asientos en un archivo JSON
def guardar_estado_asientos():
    with open("estado_asientos.json", "w") as archivo:
        json.dump(estado_asientos, archivo)

# Función para cargar el estado de los asientos desde un archivo JSON
def cargar_estado_asientos():
    global estado_asientos
    try:
        with open("estado_asientos.json", "r") as archivo:
            estado_asientos = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        estado_asientos = {}

# Llamada inicial para cargar el estado de los asientos
cargar_estado_asientos()

# Función para mostrar la disposición de asientos
def mostrar_asientos(contenido_principal, pelicula, horario, sala_numero, imagen):
    for widget in contenido_principal.winfo_children():
        widget.destroy()

    fuente_textos, fuente_titulos_subtitulos, fuente_sinopsi = init_fonts(contenido_principal)

    # Crear frames para la organización
    frame_izquierda = ctk.CTkFrame(contenido_principal, fg_color=color_principal)
    frame_izquierda.pack(side="left", fill="y", padx=10, pady=10)
    frame_derecha = ctk.CTkFrame(contenido_principal, fg_color=color_principal)
    frame_derecha.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(frame_izquierda, text=pelicula, text_color="white", font=fuente_titulos_subtitulos).pack(pady=10)
    label_imagen = ctk.CTkLabel(frame_izquierda, image=imagen, text="")
    label_imagen.pack(pady=10)

    ctk.CTkLabel(frame_izquierda, text=f"Horario: {horario}", text_color="white", font=fuente_titulos_subtitulos).pack(pady=10)
    ctk.CTkLabel(frame_izquierda, text=f"Sala: {sala_numero}", text_color="white", font=fuente_titulos_subtitulos).pack(pady=10)

    imagen = Image.open(r"SegundoSemestre\Intercine\imagenes\linea.png")
    imagen = imagen.resize((600, 50))
    linea_pantalla = ImageTk.PhotoImage(imagen)
    ctk.CTkLabel(frame_derecha, text="Seleccione los asientos que desea ocupar:", font=fuente_titulos_subtitulos).pack(pady=10)
    clave = f"{pelicula}_{horario}_{sala_numero}"
    if clave not in estado_asientos:
        estado_asientos[clave] = [[None for _ in range(8)] for _ in range(6)]
    frame_asientos = ctk.CTkFrame(frame_derecha, fg_color="transparent")
    frame_asientos.pack()

    # Agregar etiquetas de números de columna
    ctk.CTkLabel(frame_asientos, text="").grid(row=0, column=0)  
    for j in range(8):
        #Agrega los numeros en la primera fila
        ctk.CTkLabel(frame_asientos, text=str(j + 1)).grid(row=0, column=j + 1, padx=5, pady=5)

    botones = []
    for i in range(6):
        # Etiqueta de letra columna
        ctk.CTkLabel(frame_asientos, text=chr(65 + i)).grid(row=i + 1, column=0, padx=5, pady=5)
        fila_botones = []
        for j in range(8):
            estado = estado_asientos[clave][i][j]
            #Determinar el texto y color del botón basado en el estado del asiento
            texto = "O" if estado == "O" else "S" if estado == "S" else "L"
            color = "#FF0050" if estado == "O" else "green" if estado == "S" else "gray"
            #Crear el botón del asiento con el texto y color apropiados
            boton = ctk.CTkButton(frame_asientos, text=texto, width=75, height=50, fg_color=color)
            boton.grid(row=i + 1, column=j + 1, padx=5, pady=5)
            fila_botones.append(boton)
            boton.configure(command=lambda fila=i, col=j: seleccionar_asiento(fila, col, clave, botones))
        botones.append(fila_botones)

    ctk.CTkLabel(frame_derecha, image=linea_pantalla, text="").pack(pady=10)
    ctk.CTkButton(frame_derecha, text="Confirmar cambios", font=fuente_titulos_subtitulos,
                  command=lambda: confirmar_seleccion_asientos(clave, botones)).pack(pady=10)
    ctk.CTkButton(frame_derecha, text="Liberar todos los asientos Ocupados", font=fuente_titulos_subtitulos,
                  command=lambda: liberar_asientos_ocupados(clave, botones)).pack(pady=10)

# Función para quitar asiento
def seleccionar_asiento(fila, col, clave, botones):
    estado_actual = estado_asientos[clave][fila][col]
    if estado_actual == "O":
        estado_asientos[clave][fila][col] = None
        botones[fila][col].configure(text="L", fg_color="gray")

def liberar_asientos_ocupados(clave, botones):
    for i in range(6):  # filas
        for j in range(8):  # columnas
            if estado_asientos[clave][i][j] == "O":
                estado_asientos[clave][i][j] = None
                botones[i][j].configure(text="L", fg_color="gray")
    guardar_estado_asientos()
    messagebox.showinfo("Liberación", "Asientos liberados con éxito!")

# Función para confirmar la selección de asientos
def confirmar_seleccion_asientos(clave, botones):
    for i in range(6):  # filas
        for j in range(8):  # columnas
            if estado_asientos[clave][i][j] == "S":
                estado_asientos[clave][i][j] = "O"
                botones[i][j].configure(text="O", fg_color="#FF0050")
    guardar_estado_asientos()
    messagebox.showinfo("Cambios", "Cambios realizados con éxito!")

