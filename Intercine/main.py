import customtkinter as ctk
from PIL import Image, ImageTk
from modulos.cliente.login_register_gui import login_register
from modulos.cliente.gui import quienes_somos, salir
from modulos.cliente.perfil import perfil
from modulos.cliente.cartelera import cartelera
from modulos.admin.ver_peliculas import mostrar_peliculas
from modulos.admin.admin_horarios import gestion_hora
from modulos.admin.admin_salas import gestion_sala
from modulos.utilidades import color_principal, color_botones

#funcion principal que inicia la apliacion 
def main():
    root = ctk.CTk()
    root.geometry("1000x700")
    root.title("InterCine")
    
    #frame-contenedor donde estara los botoens de navegacion
    navegacion = ctk.CTkFrame(root, fg_color=color_principal, height=49)
    navegacion.pack(side="top", fill="x")
    #Contenedor donde estara las funciones de cada boto
    contenido_principal = ctk.CTkFrame(root, fg_color=color_principal)
    contenido_principal.pack(fill="both", expand=True)

    def login_exitoso_usuario(username):
        mostrar_botones_laterales_usuario(username)  
        
    def login_exitoso_administrador(username):
        mostrar_botones_laterales_administrador(username)  
        
    #llama a la funcion para mostrar la interfaz de login-register
    login_register(contenido_principal, login_exitoso_usuario, login_exitoso_administrador)
    
    #Muestra los botones para el usuario cliente
    def mostrar_botones_laterales_usuario(username):
        
        imagen = Image.open(r"SegundoSemestre\Intercine\imagenes\intercine.png") #cambiar direccion
        imagen = imagen.resize((100, 80))
        imagen_tk = ImageTk.PhotoImage(imagen)
        label_imagen = ctk.CTkLabel(navegacion, image=imagen_tk, text="")
        label_imagen.pack(side="left", padx=20, pady=10)
        
        ctk.CTkButton(navegacion, text="Salir", fg_color=color_principal, hover_color=color_botones, 
                      command=lambda: salir(root)).pack(side="right", padx=10, pady=10)
        ctk.CTkButton(navegacion, text="Sobre nosotros", fg_color=color_principal, hover_color=color_botones,
                      command=lambda: quienes_somos(contenido_principal)).pack(side="right", padx=10, pady=10)
        ctk.CTkButton(navegacion, text="Perfil", fg_color=color_principal, hover_color=color_botones, 
                      command=lambda: perfil(contenido_principal, username)).pack(side="right", padx=10, pady=10)
        ctk.CTkButton(navegacion, text="Cartelera", fg_color=color_principal, hover_color=color_botones, 
                      command=lambda: cartelera(contenido_principal)).pack(side="right", padx=10, pady=10)
        perfil(contenido_principal, username) 
        
    #Muestra los botones para el usuario administrador
    def mostrar_botones_laterales_administrador(username):
        imagen = Image.open(r"SegundoSemestre\Intercine\imagenes\intercine.png")
        imagen = imagen.resize((100, 80))
        imagen_tk = ImageTk.PhotoImage(imagen)
        label_imagen = ctk.CTkLabel(navegacion, image=imagen_tk, text="")
        label_imagen.pack(side="left", padx=20, pady=10)
        
        # ctk.CTkButton(navegacion, text="Gestionar salas", command=lambda: agregar_eliminar_sala(contenido_principal)).pack(pady=10, padx=10)
        ctk.CTkButton(navegacion, text="Salir", fg_color=color_principal, hover_color=color_botones, 
                      command=lambda: salir(root)).pack(side="right", padx=10, pady=10)
        ctk.CTkButton(navegacion, text="Perfil", fg_color=color_principal, hover_color=color_botones, 
                      command=lambda: perfil(contenido_principal, username)).pack(side="right", padx=10, pady=10)
        ctk.CTkButton(navegacion, text="Gestionar horarios", fg_color=color_principal, hover_color=color_botones, 
                      command=lambda: gestion_hora(contenido_principal)).pack(side="right", padx=10, pady=10)
        ctk.CTkButton(navegacion, text="Gestionar Salas", fg_color=color_principal, hover_color=color_botones, 
                      command=lambda: gestion_sala(contenido_principal)).pack(side="right", padx=10, pady=10)
        ctk.CTkButton(navegacion, text="Gestionar peliculas", fg_color=color_principal, hover_color=color_botones, 
                      command=lambda: mostrar_peliculas(contenido_principal)).pack(side="right", padx=10, pady=10)

        perfil(contenido_principal, username) 

    root.mainloop()

main()
