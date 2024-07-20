import json
import customtkinter as ctk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from tkinter import messagebox
from PIL import Image, ImageTk
from modulos.utilidades import init_fonts, color_principal

estado_asientos = {}
asientos_seleccionados = []

# Función para guardar el estado de los asientos en un archivo JSON
def guardar_estado_asientos():
    with open("estado_asientos.json", "w") as archivo:
        json.dump(estado_asientos, archivo)

def cargar_estado_asientos():
    global estado_asientos
    try:
        #Lee los archivos
        with open("estado_asientos.json", "r") as archivo:
            estado_asientos = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        estado_asientos = {}

cargar_estado_asientos()

def mostrar_asientos(contenido_principal, pelicula, horario, sala_numero, imagen):
    for widget in contenido_principal.winfo_children():
        widget.destroy()

    fuente_textos, fuente_titulos_subtitulos, fuente_sinopsi = init_fonts(contenido_principal)

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

    ctk.CTkLabel(frame_asientos, text="").grid(row=0, column=0)
    for j in range(8):
        #Agrega los numeros en la primera fila

        ctk.CTkLabel(frame_asientos, text=str(j + 1)).grid(row=0, column=j + 1, padx=5, pady=5)

    botones = []
    for i in range(6):
        ctk.CTkLabel(frame_asientos, text=chr(65 + i)).grid(row=i + 1, column=0, padx=5, pady=5)
        fila_botones = []
        for j in range(8):
            estado = estado_asientos[clave][i][j]
            texto = "O" if estado == "O" else "S" if estado == "S" else "L"
            color = "#FF0050" if estado == "O" else "green" if estado == "S" else "gray"
            boton = ctk.CTkButton(frame_asientos, text=texto, width=75, height=50, fg_color=color)
            boton.grid(row=i + 1, column=j + 1, padx=5, pady=5)
            fila_botones.append(boton)
            boton.configure(command=lambda fila=i, col=j: seleccionar_asiento(fila, col, clave, botones))
        botones.append(fila_botones)

    ctk.CTkLabel(frame_derecha, image=linea_pantalla, text="").pack(pady=10)
    ctk.CTkButton(frame_derecha, text="Confirmar selección", font=fuente_titulos_subtitulos,
                  command=lambda: confirmar_seleccion_asientos(clave, botones)).pack(pady=10)
    ctk.CTkButton(frame_derecha, text="Resaltar Asientos Disponibles", font=fuente_titulos_subtitulos,
                  command=lambda: resaltar_asientos_disponibles(sala_numero, horario, pelicula, botones)).pack(pady=10)

def seleccionar_asiento(fila, col, clave, botones):
    estado_actual = estado_asientos[clave][fila][col]
    if estado_actual == "O":
        messagebox.showwarning("Asiento ocupado", "Este asiento ya está ocupado.")
        return
    elif estado_actual == "S":
        estado_asientos[clave][fila][col] = None
        botones[fila][col].configure(text="L", fg_color="gray")
        if (clave, fila, col) in asientos_seleccionados:
            asientos_seleccionados.remove((clave, fila, col))
    else:
        estado_asientos[clave][fila][col] = "S"
        botones[fila][col].configure(text="S", fg_color="green")
        asientos_seleccionados.append((clave, fila, col))

def resaltar_asientos_disponibles(sala_numero, horario, pelicula, botones):
    fila_del_medio = 2
    fila_siguiente = fila_del_medio + 1
    clave = f"{pelicula}_{horario}_{sala_numero}"
    fila_completamente_ocupada = all(estado_asientos[clave][fila_del_medio][j] == "O" for j in range(8))

    for i in range(6):
        for j in range(8):
            if fila_completamente_ocupada and i == fila_siguiente:
                if estado_asientos[clave][i][j] is None:
                    botones[i][j].configure(fg_color="#D7B82B")
            elif not fila_completamente_ocupada and i == fila_del_medio:
                if estado_asientos[clave][i][j] is None:
                    botones[i][j].configure(fg_color="#D7B82B")
                elif estado_asientos[clave][i][j] is not None:
                    botones[i + 1][j].configure(fg_color="#D7B82B")
                    if estado_asientos[clave][i + 1][j] == "S":
                        botones[i + 1][j].configure(fg_color="green")
                    elif estado_asientos[clave][i + 1][j] == "O":
                        botones[i + 1][j].configure(fg_color="#FF0050")

def confirmar_seleccion_asientos(clave, botones):
    seleccionados_ahora = []
    for i in range(6):
        for j in range(8):
            if estado_asientos[clave][i][j] == "S":
                estado_asientos[clave][i][j] = "O"
                botones[i][j].configure(text="O", fg_color="#FF0050")
                seleccionados_ahora.append((i, j))
    guardar_estado_asientos()
    crear_pdf_asientos_confirmados(clave, seleccionados_ahora)
    messagebox.showinfo("Reserva", "Asientos reservados con éxito!")



def crear_pdf_asientos_confirmados(clave, seleccionados_ahora):
    pelicula, horario, sala_numero = clave.split('_')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"asientos_confirmados_{timestamp}.pdf"
    pdf = canvas.Canvas(pdf_filename, pagesize=letter)
    pdf.setFont("Helvetica", 15)
    
    # Centrar horizontalmente
    text_width = pdf.stringWidth("Asientos Confirmados", "Helvetica", 15)
    pdf.drawCentredString(letter[0] / 2, 700, "Asientos Confirmados")
    pdf.drawString(letter[0] / 2 - text_width / 2, 650, f"Película: {pelicula}")
    pdf.drawString(letter[0] / 2 - text_width / 2, 635, f"Horario: {horario}")
    pdf.drawString(letter[0] / 2 - text_width / 2, 620, f"Sala: {sala_numero}")
    pdf.drawString(letter[0] / 2 - text_width / 2, 605, "Asientos Confirmados:")
    
    # Agrega el QR
    pdf.drawImage("SegundoSemestre/Intercine/iconos/qr.png", letter[0] / 2 - 75, 500, width=150, height=150)

    # Centrar verticalmente
    text_height = 20  # Altura de cada línea de texto
    y_position = 450
    for fila, col in seleccionados_ahora:
        asiento = f"Fila {chr(65 + fila)}, Asiento {col + 1}"
        pdf.drawString(letter[0] / 2 - pdf.stringWidth(asiento, "Helvetica", 15) / 2, y_position, asiento)
        y_position -= text_height
    
    pdf.save()

