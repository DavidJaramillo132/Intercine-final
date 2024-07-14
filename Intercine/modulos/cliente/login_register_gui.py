import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from modulos.cliente.operaciones_sqlite import verify_login, register_user
from modulos.utilidades import color_principal, color_botones, init_fonts

def login_register(contenido_principal, usuario_cliente, usuario_admin):
    
    fuente_textos, fuente_titulos_subtitulos, fuente_sinopsi = init_fonts(contenido_principal)

    # Sección principal donde estarán login y register
    frame_principal = ctk.CTkFrame(contenido_principal, fg_color="#0D1822")
    frame_principal.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)
    
    #carga las imagenes para despues colocarlas mas adelante
    imagen_login = Image.open(r"SegundoSemestre\Intercine\iconos\login.png")
    imagen_login = imagen_login.resize((180, 160))
    imagen_ctk_login = ImageTk.PhotoImage(imagen_login)
    
    imagen_register = Image.open(r"SegundoSemestre\Intercine\iconos\iregister.png")
    imagen_register = imagen_register.resize((180, 160))
    imagen_ctk_register = ImageTk.PhotoImage(imagen_register)
    
    # Sección de login, en la parte izquierda
    frame_login = ctk.CTkFrame(frame_principal, fg_color=color_principal)
    frame_login.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=10, pady=10)
    
    label_imagen_izquierdo = ctk.CTkLabel(frame_login, image=imagen_ctk_login, text="")
    label_imagen_izquierdo.pack(pady=40)

    label_login = ctk.CTkLabel(frame_login, text="Iniciar Sesión", font=fuente_titulos_subtitulos)
    label_login.pack(pady=10)

    label_username = ctk.CTkLabel(frame_login, text="Usuario:", font=fuente_textos)
    label_username.pack(pady=10)

    entry_username = ctk.CTkEntry(frame_login, height=50, width=200, fg_color=color_principal, border_width=10, border_color="#0D1822")
    entry_username.pack(pady=10)

    label_password = ctk.CTkLabel(frame_login, text="Contraseña:", font=fuente_textos)
    label_password.pack(pady=10)

    entry_password = ctk.CTkEntry(frame_login, show="*", height=50, width=200, fg_color=color_principal, border_width=10, border_color="#0D1822")
    entry_password.pack(pady=10)

    button_login = ctk.CTkButton(frame_login, text="Iniciar Sesión", font=fuente_textos, fg_color=color_principal, hover_color=color_botones, 
                                 command=lambda: verify_login(entry_username, entry_password, usuario_cliente, usuario_admin))
    button_login.pack(pady=20)

    # Sección de registro, en la parte derecha
    frame_registro = ctk.CTkFrame(frame_principal,  fg_color=color_principal)
    frame_registro.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=10, pady=10)
    
    label_imagen_derecho = ctk.CTkLabel(frame_registro, image=imagen_ctk_register, text="")
    label_imagen_derecho.pack(pady=40)

    label_register = ctk.CTkLabel(frame_registro, text="Registrar Nuevo Usuario", font=("Playfair Display", 20, "bold"))
    label_register.pack(pady=10)

    label_new_username = ctk.CTkLabel(frame_registro, text="Nuevo Usuario:", font=fuente_textos)
    label_new_username.pack(pady=10)

    entry_new_username = ctk.CTkEntry(frame_registro, height=50, width=200, fg_color=color_principal, border_width=10, border_color="#0D1822")
    entry_new_username.pack(pady=10)

    label_new_password = ctk.CTkLabel(frame_registro, text="Nueva Contraseña:", font=fuente_textos)
    label_new_password.pack(pady=10)

    entry_new_password = ctk.CTkEntry(frame_registro, show="*", height=50, width=200, fg_color=color_principal, border_width=10,  border_color="#0D1822")
    entry_new_password.pack(pady=10)

    button_register = ctk.CTkButton(frame_registro, text="Registrar", font=fuente_textos, fg_color=color_principal, hover_color=color_botones,
                                    command=lambda: register_user(entry_new_username, entry_new_password, usuario_cliente))
    button_register.pack(pady=20)
