import customtkinter as ctk
import tkinter as tk

# Function to create the toolbar menu
def menubar(window):
    
    

    poppins12bold = ("Poppins", 12)

    
    fg="#202020"
    fg2="#d10000"
    # Crear el marco superior que simula el menubar
    menubar_frame = ctk.CTkFrame(window, height=30, corner_radius=0, fg_color=fg)
    menubar_frame.pack(fill="x", side="top")

    # Botón "Menu"
    menu_button = ctk.CTkButton(
        menubar_frame,
        text="Menu",
        font= poppins12bold,
        width=100,
        fg_color=fg,
        hover_color="gray",
        text_color="white",
        command=lambda: print("Menu clicked")
    )
    menu_button.pack(side="left", padx=5, pady=5)

    # Botón "Configuracion"
    config_button = ctk.CTkButton(
        menubar_frame,
        text="Configuracion",
        font= poppins12bold,
        width=120,
        fg_color=fg,
        hover_color="gray",
        text_color="white",
        command=lambda: print("Configuracion clicked")
    )
    config_button.pack(side="left", padx=5, pady=5)

    # Botón "Soporte"
    support_button = ctk.CTkButton(
        menubar_frame,
        text="Soporte",
        font= poppins12bold,
        width=100,
        fg_color=fg,
        hover_color="gray",
        text_color="white",
        command=lambda: print("Soporte clicked")
    )
    support_button.pack(side="left", padx=5, pady=5)

    # Botón "Salir"
    exit_button = ctk.CTkButton(
        menubar_frame,
        text="Cerrar sesión",
        font= poppins12bold,
        width=100,
        fg_color=fg,
        hover_color="darkred",
        text_color="white",
        command= lambda: logout(window)
    )
    exit_button.pack(side="right", padx=5, pady=5)
    

def logout(window):
    from modulos.login_fun import login
    login(window)