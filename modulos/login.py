import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
from login_fun import login

# Configuración de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")



window = ctk.CTk()
window.title("Menu")
window.geometry("1080x720")

login(window)


window.mainloop()