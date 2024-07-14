import os
import json
from modulos.admin.cargar_imagenes import cargar_imagen

DATA_FILE = 'peliculas.json'

def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file: #lee el archivo
            peliculas = json.load(file)
            for pelicula in peliculas:
                pelicula['imagen'] = cargar_imagen(pelicula['imagen_path'])
            return peliculas
    return []

def guardar_datos(peliculas):
    with open(DATA_FILE, 'w') as file: #Escribir datos en el archivo json
        data = [pelicula.copy() for pelicula in peliculas]
        for pelicula in data:
            pelicula['imagen'] = None
        json.dump(data, file, indent=4)
