import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog


# Frame de contenido principal
contenido_principal = None

# Estado de los asientos en las salas
estado_asientos = {}

# Asientos seleccionados
asientos_seleccionados = []

# Colores
color_principal = "#111317"
color_botones = "#0E4A6B"


# Fuentes
def init_fonts(root):
    # Definir las fuentes
    fuente_textos = ctk.CTkFont(family="Arial", size=18)
    fuente_titulos_subtitulos = ctk.CTkFont(family="Playfair Display", size=30, weight="bold")
    fuente_sinopsi = ctk.CTkFont(family="Arial", size=24)
    
    return fuente_textos, fuente_titulos_subtitulos, fuente_sinopsi


def cargar_imagen(path):
    if path:
        img = Image.open(path)
        img = img.resize((230, 250))
        return ImageTk.PhotoImage(img)
    return None

def seleccionar_imagen():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    return file_path

def crear_frame(root):
    frame = ctk.CTkFrame(master=root, fg_color=color_principal)
    frame.pack(padx=20, pady=20, fill="both", expand=True )
    return frame