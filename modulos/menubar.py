import customtkinter as ctk
import tkinter as tk
from modulos.transitions import transition_to_next_ui
from config.config_temas import open_config_window
import json

def set_menu_bar_color(menubar_frame, mode, menu_button, config_button, support_button, exit_button, window):
    if mode == "light":
        
        menubar_frame.configure(fg_color="#f3f3f3")  # Color blanco para modo claro
        menu_button.configure(fg_color="#f3f3f3", text_color="black")
        config_button.configure(fg_color="#f3f3f3", text_color="black")
        support_button.configure(fg_color="#f3f3f3", text_color="black")
        exit_button.configure(fg_color="#f3f3f3", text_color="black")
    else:
        menubar_frame.configure(fg_color="#202020")  # Color oscuro para otros modos
        menu_button.configure(fg_color="#202020", text_color="white")
        config_button.configure(fg_color="#202020", text_color="white")
        support_button.configure(fg_color="#202020", text_color="white")
        exit_button.configure(fg_color="#202020", text_color="white")

def get_mode_from_config():
    with open('config/config.json', 'r') as file:
        config = json.load(file)
        theme = config.get("theme", "Dark")
        if theme.lower() == "light":
            return "light"
        else:
            return "dark"

# Function to create the toolbar menu
def menubar(window):
    poppins12bold = ("Poppins", 12, "bold")
    fg = "#202020"
    fg2 = "#d10000"

    # Obtener el modo del archivo de configuración
    mode = get_mode_from_config()

    # Crear el marco superior que simula el menubar
    menubar_frame = ctk.CTkFrame(window, height=30, corner_radius=0, fg_color=fg)
    menubar_frame.pack(fill="x", side="top")

    # Botón "Menu"
    menu_button = ctk.CTkButton(menubar_frame, text="Menu", font=poppins12bold, width=100, hover_color="gray", command=lambda: print("Menu clicked"))
    menu_button.pack(side="left", padx=5, pady=5)

    # Botón "Configuracion"
    config_button = ctk.CTkButton(menubar_frame, text="Configuracion", font=poppins12bold, width=120, hover_color="gray",  command=lambda: open_config_window(window))
    config_button.pack(side="left", padx=5, pady=5)

    # Botón "Soporte"
    support_button = ctk.CTkButton(menubar_frame, text="Soporte", font=poppins12bold, width=100, hover_color="gray", command=lambda: print("Soporte clicked"))
    support_button.pack(side="left", padx=5, pady=5)

    # Botón "Salir"
    exit_button = ctk.CTkButton(menubar_frame, text="Cerrar sesión", font=poppins12bold, width=100, hover_color="darkred",  command=lambda: window.quit())
    exit_button.pack(side="right", padx=5, pady=5)

    # Ajustar el color del menubar según el modo
    set_menu_bar_color(menubar_frame, mode, menu_button, config_button, support_button, exit_button, window)

    #def logout(window):
    #    from modulos.login_fun import login
    #    transition_to_next_ui(window, None, login, duration=4000)