import json
import customtkinter as ctk
from tkinter import messagebox
from modulos.utilidades import init_fonts, color_botones, color_principal

# Ruta del archivo JSON
FILE_PATH = 'horarios.json'

def leer_horas():
    try:
        with open(FILE_PATH, 'r') as file:
            return json.load(file) #Carga y devuelve la lista de horas
    except FileNotFoundError:
        return [] #Si el archivo no existe, devuelve una lista vacía

def guardar_horas(horas):
    with open(FILE_PATH, 'w') as file: #w para escrbir en el archivo json
        json.dump(horas, file, indent=4) #Guarda la lista de horas en formato JSON

# Función para agregar una hora a la lista
def agregar_hora(hora):
    horas = leer_horas()# Lee la lista de horas
    if hora not in horas:# Verifica si la hora no está en la lista
        horas.append(hora)# Agrega la hora a la lista
        guardar_horas(horas)# Guarda la lista actualizada
        messagebox.showinfo("Información", f"Hora {hora} agregada.")#Muestra un mensaje de confirmación
        actualizar_lista_horas()#Actualiza la interfaz con la nueva lista de horas
    else:
        messagebox.showwarning("Advertencia", f"La hora {hora} ya existe.")

def eliminar_hora(hora):
    horas = leer_horas()# Lee la lista de horas
    if hora in horas:# Verifica si la hora está en la lista
        horas.remove(hora)# Elimina la hora de la lista
        guardar_horas(horas)# Guarda la lista actualizada
        messagebox.showinfo("Información", f"Hora {hora} eliminada.")
        actualizar_lista_horas()
    else:
        messagebox.showwarning("Advertencia", f"La hora {hora} no se encontró.")

# Función para agregar una hora desde la entrada de texto
def agregar_hora_desde_entrada():
    hora = entry_hora.get()  # Obtiene la hora ingresada por el usuario
    if validar_hora(hora):  # Valida el formato de la hora
        agregar_hora(hora)  # Agrega la hora si es válida
        entry_hora.delete(0, ctk.END)  # Limpia la entrada de texto
    else:
        messagebox.showerror("Error", "Formato de hora inválido. Use un formato válido como '14' o '2 PM'.")  # Muestra un error si el formato no es válido

def eliminar_hora_desde_entrada():
    hora = entry_hora.get()
    if validar_hora(hora):
        eliminar_hora(hora)
        entry_hora.delete(0, ctk.END)
    else:
        messagebox.showerror("Error", "Formato de hora inválido. Use un formato válido como '14' o '2 PM'.")

def validar_hora(hora):
    try:
        int(hora)#Intenta convertir la hora a un entero (formato 24 horas)
        return True
    except ValueError:
        if 'AM' in hora.upper() or 'PM' in hora.upper():  #Verifica si la hora tiene formato AM/PM
            partes = hora.split()
            if len(partes) == 2 and partes[0].isdigit() and partes[1].upper() in ['AM', 'PM']: # Verifica que el formato sea correcto
                return True 
    return False# Devuelve False si el formato no es válido

def actualizar_lista_horas():
    # Limpiar todos los botones actuales
    for widget in frame_botones.winfo_children():
        widget.destroy()

    # Crear botones para cada hora
    horas = leer_horas()
    for hora in horas:
        btn_hora = ctk.CTkButton(frame_botones, text=hora, command=lambda h=hora: eliminar_hora(h))
        btn_hora.pack(side=ctk.TOP, padx=10, pady=5, fill=ctk.X)

def gestion_hora(contenido_principal):
    for widget in contenido_principal.winfo_children():
        widget.destroy()
        
    global frame_botones, entry_hora
    
    fuente_textos, fuente_titulos_subtitulos, fuente_sinopsi = init_fonts(contenido_principal)

    frame_horas = ctk.CTkFrame(contenido_principal,fg_color=color_principal)
    frame_horas.pack(pady=10, fill=ctk.BOTH, expand=True)

    frame_botones = ctk.CTkFrame(contenido_principal,fg_color=color_principal)
    frame_botones.pack(pady=10, fill=ctk.BOTH, expand=True)
    #El admin puede escribnir el horario
    entry_hora = ctk.CTkEntry(frame_horas, placeholder_text="ej. 2 PM", font=fuente_sinopsi, fg_color=color_principal)
    entry_hora.pack(pady=10)

    btn_agregar = ctk.CTkButton(frame_horas, text="Agregar Hora", fg_color=color_principal, hover_color=color_botones, 
                                command=agregar_hora_desde_entrada)
    btn_agregar.pack(pady=5)
    
    ctk.CTkLabel(frame_horas, text="Selecciona la hora que desea eliminar", font=fuente_sinopsi, bg_color=color_principal, text_color="white").pack(pady=10)

    
    # Inicializar la lista de horas al finalizar la configuración de la ventana
    actualizar_lista_horas()