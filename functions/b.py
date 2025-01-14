import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
from menu import menu


def login(window):
    
    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20)
    poppins16bold = ("Poppins", 16, "bold")
    poppins12 = ("Poppins", 12)
   # Cargar la imagen

    background_image = Image.open("login.png")
    background_photo = ImageTk.PhotoImage(background_image)

    # Crear un Label para la imagen de fondo
    background_label = tk.Label(window, image=background_photo)
    background_label.place(relwidth=1, relheight=1)  # Ocupa toda la ventana

    #frame principal
    left_frame = ctk.CTkFrame(window, width=500)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)
    
    
 
    text = ctk.CTkLabel(left_frame, text="¡Bienvenido!", font=poppins30bold)
    text.place(x=155, y=150)

    text2 = ctk.CTkLabel(left_frame, text="¿Cómo desea ingresar?", font=poppins20bold)
    text2.place(x=130, y=250)
    
    text3 = ctk.CTkLabel(left_frame, text="o", font=poppins20bold)
    text3.place(x=250, y=370)


    admin= ctk.CTkButton(left_frame, text="Administrador", command=lambda: loginadmin(left_frame, window), width=200, font=poppins16bold)
    admin.place(x=150, y=320)
    
    
    usuario= ctk.CTkButton(left_frame, text="Usuario", command=lambda: print(":v"), width=200, font=poppins16bold)
    usuario.place(x=150, y=420)
    

def loginadmin(left_frame, window):
    
    
    for widget in left_frame.winfo_children():
        widget.destroy()
    
    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20)
    poppins16bold = ("Poppins", 16, "bold")
    poppins12 = ("Poppins", 12)
   # Cargar la imagen

    window=window

    
 
    text = ctk.CTkLabel(left_frame, text="¡Bienvenido administrador!", font=poppins30bold)
    text.place(x=40, y=150)

    
    contrasena = ctk.CTkEntry(left_frame, placeholder_text="Ingrese Contraseña",show="*", font=poppins16bold, width=250)
    contrasena.place(x=125, y=300)

    inicio= ctk.CTkButton(left_frame, text="Iniciar Sesión", command=lambda: check(contrasena, left_frame), width=200, font=poppins16bold)
    inicio.place(x=150, y=370)
    

    





def check(entry, window):
    
    
    poppins30bold = ("Poppins", 30, "bold")
    poppins20bold = ("Poppins", 20)
    poppins16bold = ("Poppins", 16, "bold")
    poppins12 = ("Poppins", 12)
    
    contr="1234"
    if entry.get()==contr:
        for widget in window.winfo_children():
            widget.destroy()
            
        menu(window)
        
    else:
        print("secs")
    
    
    
    
    


    
    
    



