from PIL import Image, ImageTk
from tkinter import filedialog

def cargar_imagen(path):
    if path: #verifica el lugar de donde esta el archivo
        img = Image.open(path)#caraga imagen desde esa direccion
        img = img.resize((320, 350))
        return ImageTk.PhotoImage(img)
    return None

def seleccionar_imagen(imagen_path_var, imagen_mostrar):
    # Abre un diálogo para seleccionar un archivo de imagen
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        imagen_path_var.set(file_path)
        imagen = cargar_imagen(file_path)
        imagen_mostrar.configure(image=imagen)
        imagen_mostrar.image = imagen
